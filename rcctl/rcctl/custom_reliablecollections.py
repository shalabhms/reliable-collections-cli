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

def get_reliabledictionary_list(client, application_name, service_name):
    """List existing reliable dictionaries.

    List existing reliable dictionaries and respective schema for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    """
    cluster = Cluster.from_sfclient(client)
    service = cluster.get_application(application_name).get_service(service_name)
    for dictionary in service.get_dictionaries():
        print(dictionary.name)

def get_reliabledictionary_schema(client, application_name, service_name, dictionary_name, output_file=None):
    """Query Schema information for existing reliable dictionaries.

    Query Schema information existing reliable dictionaries for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param dictionary: Name of the reliable dictionary.
    :type dictionary: str
    :param output_file: Optional file to save the schema.
    """
    cluster = Cluster.from_sfclient(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(dictionary_name)
    
    result = json.dumps(dictionary.get_information(), indent=4)
    
    if (output_file == None):
        output_file = "{}-{}-{}-schema-output.json".format(application_name, service_name, dictionary_name)
    
    with open(output_file, "w") as output:
        output.write(result)
    print('Printed schema information to: ' + output_file)
    print(result)
    
def get_reliabledictionary_type_schema(client, application_name, service_name, dictionary_name, type_name, output_file=None):
    """Query complex type information existing reliable dictionaries for given application and service. Make sure to provide entire namespace for your type if necessary.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param dictionary_name: Name of the reliable dictionary.
    :type dictionary_name: str
    :param type_name: Name of the complex type.
    :type type_name: str
    :param output_file: Optional file to save the schema.
    """
    cluster = Cluster.from_sfclient(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(dictionary_name)
    result = json.dumps(dictionary.get_complex_type(type_name), indent=4)
    
    if (output_file == None):
        output_file = "{}-{}-{}-{}-type-output.json".format(application_name, service_name, dictionary_name, type_name)
    
    with open(output_file, "w") as output:
        output.write(result)
    print('Printed schema information to: ' + output_file)
    print(result)

def query_reliabledictionary(client, application_name, service_name, dictionary_name, query_string, partition_key=None, partition_id=None, output_file=None):
    """Query existing reliable dictionary.

    Query existing reliable dictionaries for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param dictionary_name: Name of the reliable dictionary.
    :type dictionary_name: str
    :param query_string: An OData query string. For example $top=10. Check https://www.odata.org/documentation/ for more information.
    :type query_string: str
    :param partition_key: Optional partition key of the desired partition, either a string if named schema or int if Int64 schema
    :type partition_id: str
    :param partition_id: Optional partition GUID of the owning reliable dictionary.
    :type partition_id: str
    :param output_file: Optional file to save the schema.
    """
    cluster = Cluster.from_sfclient(client)
    dictionary = cluster.get_application(application_name).get_service(service_name).get_dictionary(dictionary_name)
    
    
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
        output_file = "{}-{}-{}-query-output.json".format(application_name, service_name, dictionary_name)
    
    with open(output_file, "w") as output:
        output.write(result)
    print()
    print('Printed output to: ' + output_file)
    print(result)
    
def execute_reliabledictionary(client, application_name, service_name, input_file):
    """Execute create, update, delete operations on existing reliable dictionaries.

    carry out create, update and delete operations on existing reliable dictionaries for given application and service.

    :param application_name: Name of the application.
    :type application_name: str
    :param service_name: Name of the service.
    :type service_name: str
    :param output_file: input file with list of json to provide the operation information for reliable dictionaries.
    """

    cluster = Cluster.from_sfclient(client)
    service = cluster.get_application(application_name).get_service(service_name)

    # call get service with headers and params
    with open(input_file) as json_file:
        json_data = json.load(json_file)
        service.execute(json_data)
    return
