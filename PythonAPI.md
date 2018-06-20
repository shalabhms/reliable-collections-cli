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
