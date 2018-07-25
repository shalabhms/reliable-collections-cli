import requests
import pprint
import json
import xmltodict
import xml.etree.ElementTree as ET
import sys
import time
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
    cluster = Cluster.from_sfclient(client)
    service = cluster.get_application(application_name).get_service(service_name)
    for dictionary in service.get_dictionaries():
        print(dictionary.name)

def get_reliablecollections_schema(client, application_name, service_name, collection_name, output_file=None):
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
    cluster = Cluster.from_sfclient(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(collection_name)
    
    result = json.dumps(dictionary.get_information(), indent=4)
    
    if (output_file == None):
        output_file = "{}-{}-{}-schema-output.json".format(application_name, service_name, collection_name)
    
    with open(output_file, "w") as output:
        output.write(result)
    print('Printed schema information to: ' + output_file)
    print(result)
    
def get_reliablecollections_type(client, application_name, service_name, collection_name, type_name, output_file=None):
    """Query complex type information existing reliable collections for given application and service. Make sure to provide entire namespace for your type if necessary.

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
    cluster = Cluster.from_sfclient(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(collection_name)
    result = json.dumps(dictionary.get_complex_type(type_name), indent=4)
    
    if (output_file == None):
        output_file = "{}-{}-{}-{}-type-output.json".format(application_name, service_name, collection_name, type_name)
    
    with open(output_file, "w") as output:
        output.write(result)
    print('Printed schema information to: ' + output_file)
    print(result)

def query_reliablecollections(client, application_name, service_name, collection_name, query_string, partition_key=None, partition_id=None, output_file=None):
    """Query existing reliable collections.

    Query existing reliable collections for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param collection_name: Name of the reliable collection.
    :type collection_name: str
    :param query_string: An OData query string. For example $top=10. Check https://www.odata.org/documentation/ for more information.
    :type query_string: str
    :param partition_key: Optional partition key of the desired partition, either a string if named schema or int if Int64 schema
    :type partition_id: str
    :param partition_id: Optional partition GUID of the owning reliable collection.
    :type partition_id: str
    :param output_file: Optional file to save the schema.
    """
    cluster = Cluster.from_sfclient(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(collection_name)
    
    
    start = time.time()
    if (partition_id != None):
        result = dictionary.query(query_string, PartitionLookup.ID, partition_id)
    elif (partition_key != None):
        result = dictionary.query(query_string, PartitionLookup.KEY, partition_key)
    else:
        result = dictionary.query(query_string)
    
    if type(result) is str:
        print(result)
        return
    else:
        result = json.dumps(result.get("value"), indent=4)
    
    print("Query took " + str(time.time() - start) + " seconds")
    
    if (output_file == None):
        output_file = "{}-{}-{}-query-output.json".format(application_name, service_name, collection_name)
    
    with open(output_file, "w") as output:
        output.write(result)
    print()
    print('Printed output to: ' + output_file)
    print(result)
    
def execute_reliablecollections(client, application_name, service_name, input_file, partition_id=-1):
    """Execute create, update, delete operations on existing reliable collections.

    carry out create, update and delete operations on existing reliable collections for given application and service.

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
  
