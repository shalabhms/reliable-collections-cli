### SFQuery

##### Cluster

    Cluster(credentials : Authentication, url : 'http://myaddress:HttpGatewayEndpoint') : Cluster
    
    get_applications() : Application list
    get_application(ApplicationName : string) : Application
    get_manifest() : Models.ClusterManifest
    
##### Application

    Application(cluster : Cluster, name : string) : Application
    name : string
    cluster : Cluster
    
    get_services() : Service List
    get_service(ServiceName : string) : Service
    get_information() : Models.ApplicationInfo
    
##### Service

    Service(application : Application, name : string) : Service
    name : string
    application : Application
    
    get_dictionaries() : Dictionary list
    get_dictionary(DictionaryName : string) : Dictionary
    get_information() : Models.ServiceInfo
    
##### Dictionary 

    Dictionary(service : Service, name : string) : Dictionary
    name : string
    service : Service
    
    get_information() : json
    get_complex_type(TypeName : 'Namespace.Name') : json
    
    query(query : string, *param : PartitionLookup, *partition_name : id or key) : json


##### Enum: PartitionLookup (used to specify query argument)
    KEY
    ID

### Examples
#### Discover a dictionary and its types
```python
# get my cluster and ask for applications
cluster = Cluster('http://localhost:19080')
applications = cluster.get_applications()

for application in applications:
    print(application.name)
    
```

> fabric:/BasicApp

```python
# get an application and ask for services
application = applications[0]
services = application.get_services()
for service in services:
    print(service.name)

```

> fabric:/BasicApp/CarSvc

> fabric:/BasicApp/ProductSvc

> fabric:/BasicApp/UserSvc

```python

# get a service and ask for its dictionaries
service = services[2]
dictionaries = service.get_dictionaries()

# print information about the dictionaries
for dictionary in dictionaries:
    info = dictionary.get_information()
    print(dictionary.name)
    for child in info:
        print('\t' + child.get('Name') + ': ' + child.get('Type'))

```

> users

	>> PartitionId: Edm.Guid
    
	>> Key: Basic.Common.UserName
    
	>> Value: Basic.Common.UserProfile
    
	>> Etag: Edm.String

```python

dictionary = dictionaries[0]

# get information about a specific type in that dictionary
info = dictionary.get_complex_type('Basic.Common.UserName')
print('Basic.Common.UserName')
for child in info:
    print('\t' + child.get('Name') + ': ' + child.get('Type'))
        
```

> Basic.Common.UserName

	>> First: Edm.String
    
	>> Last: Edm.String

#### Get a dictionary and query a specific partition
```python
dictionary = Cluster('http://localhost:19080').get_application('BasicApp').get_service('UserSvc').get_dictionary('users')

# query all the dictionaries
response = dictionary.query('$top=1')

# query based on partition id
response = dictionary.query('$top=1', 
                            '306f3bcf-eedb-4888-927d-cf5d9b118aa0', 
                            'guid')

# or
partition_id = dictionary.get_partition_ids()[0]
response = dictionary.query('$top=1', partition_id, 'id')

# query based on partition key
response = dictionary.query('$top=1', 10, 'key')
```