import requests
import pprint
import json
import xmltodict
import xml.etree.ElementTree as ET
import sys
import pandas as pd
from pandas.io.json import json_normalize
from sfquery import *

def get_reliablecollections_list(client, app, svc):
	cluster = Cluster(client)
	service = cluster.get_application(app).get_service(svc)
	for dictionary in service.get_dictionaries():
		print(dictionary.name)

def get_reliablecollections_schema(client, app, svc, rc):
	cluster = Cluster(client)
	dictionary = cluster.get_application(app).get_service(svc).get_dictionary(rc)
	print(json.dumps(dictionary.get_information(), indent=4))
	
def get_reliablecollections_type(client, app, svc, rc, type_name):
	cluster = Cluster(client)
	dictionary = cluster.get_application(app).get_service(svc).get_dictionary(rc)
	print(json.dumps(dictionary.get_complex_type(type_name), indent=4))

def query_reliablecollections(client, app, svc, rc, query_string='$top=1', lookup=None, partition=None, filename=None):
	cluster = Cluster(client)
	dictionary = cluster.get_application(app).get_service(svc).get_dictionary(rc)
	
	result = json.dumps(dictionary.query(query_string, lookup, partition).get("value"),indent=4)
	
	if (filename == None):
		print(result)
	else:
		with open(filename, "a") as output:
			output.write(result)
		print("Output written to: " + filename)
	
def execute_reliablecollections(client, application_name, service_name, input_file, partition_id=-1):
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
  
