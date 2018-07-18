# SFQuery.py
# author: t-anmen@microsoft.com

import requests
import xml.etree.ElementTree as et # To parse/view XML
from xmljson import badgerfish as bf
import json
from azure.servicefabric.service_fabric_client_ap_is import ServiceFabricClientAPIs
from enum import Enum

class PartitionLookup(Enum):
    KEY = 1
    ID = 2

class Cluster(object):

    _fabric_client = None;
    _namespace = '{http://schemas.microsoft.com/2011/01/fabric}'
    _url = None;
    
    def __init__(self, credentials, url):
        self._url = url
        self._fabric_client = ServiceFabricClientAPIs(credentials, url)

    def get_applications(self):
        applications = []
        
        continuation_token = None;
        while True:
            paged_application_info_list = self._fabric_client.get_application_info_list(0, None, False, continuation_token)
            for application_info in paged_application_info_list.items:
                applications.append(Application(self, application_info.id))
            if paged_application_info_list.continuation_token == '':
                break
            else: 
                continuation_token = paged_application_info_list.continuation_token
        return applications

    def get_application(self, name):
        applications = self.get_applications()
        for application in applications:
            if application.name == name:
                return application
        raise ValueError("Could not find application with name: {}".format(name))
    
    def _get_httpapplicationgatewayendpoint(self):
        manifestxml = et.fromstring(self.get_manifest().manifest)
        endpoints = manifestxml.find(
            './/' + self._namespace + "HttpApplicationGatewayEndpoint")
        return endpoints.get("Port")
    
    def get_manifest(self):
        return self._fabric_client.get_cluster_manifest()

class Application(object):
    
    name = None 
    cluster = None

    def __init__(self, cluster, name):
        self.cluster = cluster
        self.name = name
    
    def get_services(self):
        services = []
        
        continuation_token = None;
        while True:
            paged_service_info_list = self.cluster._fabric_client.get_service_info_list(self.name, None, continuation_token)
            for service_info in paged_service_info_list.items:
                services.append(Service(self, service_info.id.rsplit('~', 1)[-1]))
            if paged_service_info_list.continuation_token == '':
                break
            else: 
                continuation_token = paged_service_info_list.continuation_token
        return services

    def get_service(self, name):
        services = self.get_services()
        for service in services:
            if service.name == name:
                return service
        raise ValueError("Could not find service with name: {}".format(name))
    
    def get_information(self):
        return self.cluster._fabric_client.get_application_info(self.name)


class Service(object):

    application = None
    name = None
    
    _namespace = '{http://schemas.microsoft.com/ado/2009/11/edm}'
    _url = None

    def __init__(self, application, name):
        self.application = application
        self.name = name
        port = application.cluster._get_httpapplicationgatewayendpoint()
        self._url = self.application.cluster._url.rsplit(':', 1)[0] + ':' + port + '/' + self.application.name + '/' + name
       
    def get_information(self):
        return self.application.cluster._fabric_client.get_service_info(self.application.name, '{}~{}'.format(self.application.name, self.name))

    # note: does not return filters, even though these are valid 
    # dictionaries, because querying them is an abnormal case
    def get_dictionaries(self):
        dictionary_list = []
        partitions = self._get_partition_info_list()
        
        r = ''
        
        if partitions[0].service_partition_kind == 'Int64Range':
            partition_key = int(partitions[0].high_key) - 1
            r = requests.get(self._url + "/$query/$metadata?PartitionKind=Int64Range&PartitionKey={}".format(partition_key))
        elif partitions[0].service_partition_kind == 'Named':
            partition_key = partitions[0].name
            r = requests.get(self._url + "/$query/$metadata?PartitionKind=Named&PartitionKey={}".format(partition_key))
        elif partitions[0].service_partition_kind == 'Singleton':
            r = requests.get(self._url + "/$query/$metadata")

        root = et.fromstring(r.text)

        for dictionarymeta in root.findall('.//' + self._namespace + 'EntitySet'):
            if '/filter/' not in dictionarymeta.get('Name'):
                dictionary_list.append(Dictionary(self, dictionarymeta.get('Name')))
        return dictionary_list 
    
    def _get_partition_info_list(self):
        partitions = []
        
        continuation_token = None
        while True:
            paged_partition_info_list = self.application.cluster._fabric_client.get_partition_info_list('{}~{}'.format(self.application.name, self.name), continuation_token)
            for partition_info in paged_partition_info_list.items:
                partitions.append(partition_info.partition_information)
            if paged_partition_info_list.continuation_token == '':
                break
            else: 
                continuation_token = paged_partition_info_list.continuation_token
            
        return partitions
    
    # returns guid corresponding to that key
    def _partition_key_to_id(self, key):
        partitions = self._get_partition_info_list()
        if partitions[0].service_partition_kind == 'Int64Range':
            for partition in partitions:
                if key <= partition.high_key and key >= parition.low_key:
                    return partition.id
        elif partitions[0].service_partition_kind == 'Named':
            for partition in partitions:
                if key == partition.name:
                    return partition.id
        elif partitions[0].service_partition_kind == 'Singleton':
            return partitions[0].id
        
    def get_dictionary(self, name):
        dictionaries = self.get_dictionaries()
        for dictionary in dictionaries:
            if dictionary.name == name:
                return dictionary
        raise ValueError("Could not find dictionary with name: {}".format(name))
                         
#TODO: refactor to add Collection which dictionary inherits from     
    
class Dictionary(object):
    
    service = None
    name = None
    
    _namespace = '{http://schemas.microsoft.com/ado/2009/11/edm}'
    _api_version = '6.0'
    
    def __init__(self, service, name):
        self.service = service
        self.name = name
    
        
    def get_information(self):
        r = requests.get(self.service._url + "/$query/$metadata")
        root = et.fromstring(r.text)

        for dictionarymeta in root.findall('.//' + self._namespace + 'EntitySet'):
            if (dictionarymeta.get('Name') == self.name):
                entity_type = dictionarymeta.get("EntityType").rsplit('.', 1)[-1]
                dictionary = root.find(".//*[@Name='" + entity_type + "']")
                return bf.data(dictionary)
        return None
        
    def query(self, querystring, param = None, partition_name = None):
        
        partition_key = None
        partition_id = None
        partition_type = None
        
        partitions = self.service._get_partition_info_list()
        
        if partition_name is None:
            if partitions[0].service_partition_kind == 'Int64Range':
                partition_key = int(partitions[0].high_key) - 1
                partition_type = 'Int64Range'
            elif partitions[0].service_partition_kind == 'Named':
                partition_key = partitions[0].name
                partition_type = 'Named'
            elif partitions[0].service_partition_kind == 'Singleton':
                partition_type = 'Singleton'
        elif param == PartitionLookup.KEY:
            partition_key = partition_name;
            partition_id = self.service._partition_key_to_id(partition_name)
            partition_type = partitions[0].service_partition_kind
        elif param == PartitionLookup.ID:
            partition_id = partition_name
            
            found = False
            
            for partition in partitions:
                if partition.id == partition_name:
                    if partition.service_partition_kind == 'Int64Range':
                        partition_key = int(partition.high_key) - 1
                        partition_type = 'Int64Range'
                    elif partition.service_partition_kind == 'Named':
                        partition_key = partition.name
                        partition_type = 'Named'
                    elif partition.service_partition_kind == 'Singleton':
                        partition_type = 'Singleton'
                    found = True
                    break
            
            if found == False:
                raise ValueError('Could not find that partition ID')
        else:
            raise ValueError('invalid arguments')
        
        if partition_type == 'Singleton':
            r = '{}/$query/{}?{}'.format(self.service._url, self.name, querystring)
        elif partition_id == None:
            r = '{}/$query/{}?{}&PartitionKind={}&PartitionKey={}'.format(self.service._url, self.name, querystring, partition_type, partition_key)
        else:
            r = '{}/$query/{}/{}?{}&PartitionKind={}&PartitionKey={}'.format(self.service._url, partition_id, self.name, querystring, partition_type, partition_key)
        
        return requests.get(r).json()
    
    # should be of form: Namespace.TypeName
    def get_complex_type(self, typeask):
        
        r = requests.get(self.service._url + "/$query/$metadata")
        root = et.fromstring(r.text)

        if '.' not in typeask:
            raise ValueError("Type must be in form 'Namespace.Name'")
        
        schema_name = typeask.rsplit('.', 1)[0] # Namespace
        type_name = typeask.rsplit('.', 1)[1] # Name

        schema = root.find(".//*[@Namespace='" + schema_name + "']")
        
        if schema is None:
            raise ValueError("Could not find this type")
        
        mytype = schema.find("*[@Name='" + type_name + "']")
        
        if mytype is None:
            raise ValueError("Could not find this type")
        
        return bf.data(mytype)