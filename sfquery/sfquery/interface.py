from ipywidgets import widgets
import json
import time
from .sfquery import PartitionLookup
import warnings

warnings.filterwarnings("ignore", message="Accept header absent and forced to application/json")

class Interface(object):
    
    cluster = None;
    app = None;
    service = None;
    dictionary = None;

    def __init__(self, cluster):
        self.cluster = cluster;
        applications = self.cluster.get_applications()
        name_list = []
        for application in applications:
            name_list.append(application.get_information().name.replace('fabric:/',''))

        self.application_selector = widgets.Dropdown(
            options = name_list,
            description='Application:',
            disabled=False)
        
        self.service_selector = widgets.Dropdown(
            description='Service:',
            disabled=False)
        
        self.dictionary_selector = widgets.Dropdown(
            description='Dictionary:',
            disabled=False)
        
        self.partition_key_entry = widgets.Text(
            placeholder='Partition A',
            description='Optional Key',
            disabled=False
        )
        self.partition_guid_entry = widgets.Text(
            placeholder='00000000-0000-0000-0000-000000000000',
            description='Optional ID:',
            disabled=False
        )
        self.query_entry = widgets.Text(
            placeholder='$top=1',
            description='Query:',
            disabled=False
        )
        
        self.query_button = widgets.Button(
            description='Query',
            disabled=False,
            button_style='success', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Query',
            icon='check'
        )
        self.query_button.on_click(self.try_query)
        self.query_results = widgets.Output(layout={'border': '1px solid black'})
        self.application_selector.observe(self.create_application)
        self.service_selector.observe(self.create_service)
        self.dictionary_selector.observe(self.create_dictionary)

        
        display(self.application_selector)
        display(self.service_selector)
        display(self.dictionary_selector)
        
        print('Query your dictionary')
        display(self.partition_key_entry)
        display(self.partition_guid_entry)
        display(self.query_entry)
        display(self.query_button)
        display(self.query_results)
        
        if (len(name_list) > 0):
            self.create_application(self.application_selector)   
        
    def create_application(self, sender):
        self.service_selector.unobserve(self.create_service)
        self.app = self.cluster.get_application(self.application_selector.value)
        services = self.app.get_services()
        name_list = []
        
        for service in services:
            name_list.append(service.get_information().name.replace('fabric:/','').replace(self.application_selector.value + '/',''))

        with self.service_selector.hold_trait_notifications():
            self.service_selector.options = name_list
        if len(name_list) > 0:
            self.service_selector.observe(self.create_service)
            self.service_selector.value = self.service_selector.options[0]
            self.create_service(self.service_selector)
        else:
            self.service_selector.value = None

    def create_service(self, sender):  
        self.dictionary_selector.unobserve(self.create_dictionary)
        self.service = self.app.get_service(self.service_selector.value)
        name_list = []
        
        for dictionary in self.service.get_dictionaries():
            name_list.append(dictionary.name)
            
        with self.dictionary_selector.hold_trait_notifications():    
            self.dictionary_selector.options = name_list
        if len(name_list) > 0:
            self.dictionary_selector.observe(self.create_dictionary)
            self.dictionary_selector.value = self.dictionary_selector.options[0]
            self.create_dictionary(self.dictionary_selector)
        else:
            self.dictionary_selector.value = None
        
    def create_dictionary(self, sender):
        dictionaries = self.service.get_dictionaries()
        for dictionary in dictionaries:
            if dictionary.name == self.dictionary_selector.value:
                self.dictionary = dictionary
        
    def try_query(self, sender):   
        self.query_results.clear_output(True)
        
        if (self.application_selector.value == None or self.service_selector.value == None or self.dictionary_selector.value == None):
            with self.query_results:
                print("Please choose an Application/Service/Dictionary to query")
            return
        if (self.query_entry.value == ''):
            with self.query_results:
                print('Please enter a valid query')
            return
        
        start = time.time()

        if(self.partition_key_entry.value != ''):
            with self.query_results:
                print(json.dumps(self.dictionary.query(self.query_entry.value, PartitionLookup.KEY, self.partition_key_entry.value), indent=4))
                print('Query took ' + str(time.time()-start) + ' sec')
        elif(self.partition_guid_entry.value != ''):
            with self.query_results:
                print(json.dumps(self.dictionary.query(self.query_entry.value, PartitionLookup.ID, self.partition_guid_entry.value), indent=4))
                print('Query took ' + str(time.time()-start) + ' sec')
        else:
            with self.query_results:
                print(json.dumps(self.dictionary.query(self.query_entry.value), indent=4))
                print('Query took ' + str(time.time()-start) + ' sec')
        
        