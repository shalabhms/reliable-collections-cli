# SFQuery.py
# author: t-anmen@microsoft.com

import requests
import xml.etree.ElementTree as et # To parse/view XML
import json

class Cluster(object):
    
    _namespace = '{http://schemas.microsoft.com/2011/01/fabric}'
    _api_version = '6.0'
    _url = None

    def __init__(self, url=None):
        self._url = url

    def get_applications(self):
        application_list = []
        r = requests.get(self._url + '/Applications?api-version=' + self._api_version).json()
        for application in r.get('Items'):
            application_list.append(Application(self, application.get('Id')))
        return application_list

    def get_application(self, name):
        return Application(self, name)
    
    def _get_httpapplicationgatewayendpoint(self):
        r = requests.get(self._url + '/$/GetClusterManifest?api-version=' + self._api_version).json()
        root = et.fromstring(r.get("Manifest"))
        endpoints = root.find(
            './/' + self._namespace + "HttpApplicationGatewayEndpoint")
        return endpoints.get("Port")
    
    def get_manifest(self):
        r = requests.get(self._url + '/$/GetClusterManifest?api-version=' + self._api_version).json()
        return et.fromstring(r.get("Manifest"))

    def get_health(self):
        r = requests.get(self._url + '/$/GetClusterHealth?api-version=' + self._api_version).json()

class Application(object):
    
    name = None 
    cluster = None
    
    _api_version = '6.0'

    def __init__(self, cluster, name):
        self.cluster = cluster
        self.name = name
    
    def get_services(self):
        
        r = requests.get(
            self.cluster._url + '/Applications/' + 
            self.name + '/$/GetServices?api-version=' + 
            self._api_version).json()
        
        service_list = []
        for service in r.get('Items'):
            service_list.append(Service(self, service.get('Id').rsplit('~', 1)[-1]))
        return service_list

    def get_service(self, name):
        return Service(self, name)
    
    def get_information(self):
        return requests.get(self.cluster._url + '/Applications/' + self.name + '?api-version=' + self._api_version).json()


class Service(object):

    application = None
    name = None
    
    _namespace = '{http://schemas.microsoft.com/ado/2009/11/edm}'
    _api_version = '6.0'
    _url = None

    def __init__(self, application, name):
        self.application = application
        self.name = name
        port = application.cluster._get_httpapplicationgatewayendpoint()
        self._url = self.application.cluster._url.rsplit(':', 1)[0] + ':' + port + '/' + self.application.name + '/' + name
       
    def get_information(self):
        r = requests.get(
            self.application.cluster._url + '/Applications/' + 
            self.application.name + '/$/GetServices?api-version=' + 
            self._api_version).json()
        for service in r.get('Items'):
            if (service.get('Id') == (self.application.name + '~' + self.name)):
                return service
            
        return None # error condition

    def get_dictionaries(self):

        dictionary_list = []
        r = requests.get(self._url + "/$query/$metadata")
        print(r.status_code) # remove
        root = et.fromstring(r.text)

        for dictionarymeta in root.findall('.//' + self._namespace + 'EntitySet'):
            dictionary_list.append(Dictionary(self, dictionarymeta.get('Name')))
        return dictionary_list 
    
    def _get_partitions(self):
        partition_list = []
        r = requests.get('{}/{}/Services/{}~{}/$/GetPartitions?{}'.format(self.application.cluster._url,self.application.name, self.application.name, self.name, self._api_version))
        print(r)
        
    def get_dictionary(self, name):
        return Dictionary(self, name)

#TODO: refactor to add Collection which dictionary inherits from     
    
class Dictionary(object):
    
    service = None
    name = None
    
    _namespace = '{http://schemas.microsoft.com/ado/2009/11/edm}'
    _api_version = '6.0'
    
    def __init__(self, service, name):
        self.service = service
        self.name = name

    def get_partition_ids(self):
        
        partitions_list = []
        r = requests.get('{}/Services/{}~{}/$/GetPartitions?api-version={}'.format(
            self.service.application.cluster._url,
            self.service.application.name,
            self.service.name,
            self._api_version)).json()
        
        for item in r.get("Items"):
            partitions_list.append(item.get('PartitionInformation').get('Id'))
        return partitions_list
    
    def get_partitions(self):
        
        partitions_list = []
        r = requests.get('{}/Services/{}~{}/$/GetPartitions?api-version={}'.format(
            self.service.application.cluster._url,
            self.service.application.name,
            self.service.name,
            self._api_version)).json()
        
        for item in r.get("Items"):
            partitions_list.append(item)
        return partitions_list
        
    def get_information(self):
        r = requests.get(self.service._url + "/$query/$metadata")
        root = et.fromstring(r.text)

        for dictionarymeta in root.findall('.//' + self._namespace + 'EntitySet'):
            if (dictionarymeta.get('Name') == self.name):
                entity_type = dictionarymeta.get("EntityType").rsplit('.', 1)[-1]
                dictionary = root.find(".//*[@Name='" + entity_type + "']")
                return dictionary
        return None
    
    # returns guid corresponding to that key
    def _resolve_partition(self, key):
        r = requests.get('{}/Services/{}~{}/$/GetPartitions?api-version={}'.format(
            self.service.application.cluster._url,
            self.service.application.name,
            self.service.name,
            self._api_version)).json()
        
        for partition in r.get('Items'):
            partition_kind = partition.get('PartitionInformation').get('ServicePartitionKind')
            if partition_kind == 'Singleton':
                return partition.get('PartitionInformation').get('Id')
            elif partition_kind == 'Int64Range':
                lowkey = partition.get('PartitionInformation').get('LowKey')
                highkey = partition.get('PartitionInformation').get('HighKey')
                if key >= lowkey and key <= highkey:
                    return partition.get('PartitionInformation').get('Id')
            else:
                #todo: support Named Partitions
                raise NotImplementedError('Currently only Singleton and Int64Range are supported')
        raise KeyError('Could not find key')
        
    # query(string): queries all partitions
    # query(string, id, "id"): queries partition with id
    # query(string, key, "key"): queries parition with key
    def query(self, querystring, partition = None, param = None):
        
        if partition is None:
            r = requests.get('{}/$query/{}?{}'.format(self.service._url, self.name, querystring)).json()
        else:
            if param == 'id':
                r = requests.get('{}/$query/{}/{}?{}'.format(self.service._url, partition, self.name, querystring)).json()
            elif param == 'key':
                guid = self._resolve_partition(partition)
                r = requests.get('{}/$query/{}/{}?{}'.format(self.service._url, guid, self.name, querystring)).json()
            else:
                raise ValueError('If partition information is passed in, whether \'key\' or \'guid\' was passed in must be specified as a third argument')
        return r.get('value')
    
    # should be of form: Namespace.TypeName
    def get_complex_type(self, typeask):
        
        r = requests.get(self.service._url + "/$query/$metadata")
        root = et.fromstring(r.text)

        schema_name = typeask.rsplit('.', 1)[0] # Namespace
        type_name = typeask.rsplit('.', 1)[1] # Name

        schema = root.find(".//*[@Namespace='" + schema_name + "']")
        mytype = schema.find("*[@Name='" + type_name + "']")
        return mytype
        
