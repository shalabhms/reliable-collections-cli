import requests
import pprint
import json
import xmltodict
import xml.etree.ElementTree as ET
import sys
import pandas as pd
from pandas.io.json import json_normalize
from sfquery import *

def get_reliablecollections_list(client, application_name, service_name):
    """List existing reliable collections.

    List existing reliable collections and respective schema for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    """
    cluster = Cluster(client)
    service = cluster.get_application(application_name).get_service(service_name)
    for dictionary in service.get_dictionaries():
        print(dictionary.name)

def get_reliablecollections_schema(client, application_name, service_name, collection_name):
    """Query Schema information for existing reliable collections.

    Query Schema information existing reliable collections for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param collection_name: Name of the reliable collection.
    :type collection_name: str
    :param output_file: Optional file to save the schema.
    """
    cluster = Cluster(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(collection_name)
    print(json.dumps(dictionary.get_information(), indent=4))
    
def get_reliablecollections_type(client, application_name, service_name, collection_name, type_name):
    """Query complex type information for existing reliable collections.

    Query complex type information existing reliable collections for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param collection_name: Name of the reliable collection.
    :type collection_name: str
    :param type_name: Name of the complex type.
    :type type_name: str
    :param output_file: Optional file to save the schema.
    """
    cluster = Cluster(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(collection_name)
    print(json.dumps(dictionary.get_complex_type(type_name), indent=4))

def query_reliablecollections(client, application_name, service_name, collection_name, query_string='$top=1', partition_key=None, partition_id=None, output_file='output.json'):
    """Query existing reliable collections.

    Query existing reliable collections for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param collection_name: Name of the reliable collection.
    :type collection_name: str
    :param query_type: Type of query. For example $top=10.
    :type query_type: str
    :param partition_id: Partition Identifier of the owning reliable collection.
    :type partition_id: str
    """
    cluster = Cluster(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(collection_name)
    
    if (partition_id != None):
        result = json.dumps(dictionary.query(query_string, PartitionLookup.ID, partition_id).get("value"),indent=4)
    elif (partition_key != None):
        result = json.dumps(dictionary.query(query_string, PartitionLookup.KEY, partition_key).get("value"),indent=4)
    else:
        result = json.dumps(dictionary.query(query_string).get("value"),indent=4)
    
    with open(output_file, "a") as output:
        output.write(result)
    print('Printed output to: ' + output_file)
    print(result)
    
def execute_reliablecollections(client, application_name, service_name, input_file, partition_id=-1):
    """Execute create, update, delete operations on existing reliable collections.

    Execute create, update and delete operations on existing reliable collections for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param partition_id: Partition Identifier of the owning reliable collection.
    :type partition_id: str
    :param output_file: input json file to provide the operation information for reliable collections.
    """
    if partition_id is -1:
        url = 'http://localhost:19081/'+application_name+'/'+service_name+'/api/StatefulQuery/'
    else:
        url = 'http://localhost:19081/'+application_name+'/'+service_name+'/api/StatefulQuery/'+partition_id
    # call get service with headers and params
    with open(input_file) as json_file:
        json_data = json.load(json_file)
        #print json.dumps(json_data, indent=4)
        json_data2 = json.dumps(json_data, indent=4)
        response = requests.put(url, data=json_data2)
    print("-- Execute result ---\n")
    print(json.dumps(json.loads(response.text), indent=4))
  
