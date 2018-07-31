# Reliable Collections CLI Walkthrough

In this walkthrough, we have gotten a request to update the `Age` of one of our users, who has `Email` `user-0005@example.com` to `19`. This tutorial operates against the sample queryable application [BasicApp](https://github.com/jessebenson/service-fabric-queryable/tree/master/samples/Basic), which you can download and deploy to your local Service Fabric cluster to follow along.

Remember that throughout `rcctl`, you can generally shorten arguments to their single letter name. You can see the syntax by using the `-h` help flag on any function. For example: `--application-name = -a`,  `--service-name = -s`, `--output-file = -out`, etc.

## Walkthrough

### Step 1: Connect to cluster

If your application is deployed locally, you can skip this step, as `rcctl` automatically connects to `http://localhost:19080`.

It is important that when you created your cluster, you enabled Reverse Proxy. You can read more about setting up Reverse Proxy [here](https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-reverseproxy).

Since it is not recommended to expose your reverse proxy endpoint publicly, you will have to remote onto your node and use `rcctl` from there.

1. Open a remote connection to `mycluster.westus.cloudapp.azure.com:3391`. 
2. Pass the remote connection a secure cluster certificate as a PEM file. 
    - You can read about turning the PFX from your Azure Key Vault to a PEM [here](https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-cli#convert-a-certificate-from-pfx-to-pem-format). 
    - You can read about passing in files to your remote connection [here](https://help.1and1.co.uk/servers-c40665/dedicated-server-windows-c40591/organization-via-control-panel-c43542/transfer-files-to-windows-server-using-remote-desktop-a731882.html).
3. [Make sure you have installed python and `rcctl`](../master/README.md#installing)
4. Connect to your cluster using:

```shell
rcctl cluster select --endpoint https://localhost:19080 --pem ../path/to/pem
```
5. Proceed to **Step 2**

#### If you have a secure Reverse Proxy

`sfquery` assumes that Reverse Proxy does not maintain a certificate (i.e. is HTTP instead of HTTPS). If you have secured Reverse Proxy you will have to do a few things in `sfquery.py`:
- Remove the line `self._url = self._url.replace('https', 'http').replace('HTTPS', 'HTTP')` from Service
- Whenever `requests.get('url')` are called, they should be changed to `requests.get('url', verify=False)` so as to not verify the Reverse Proxy certificate you have set up.

### Step 2: See the available dictionaries in your service

```shell
rcctl dictionary list --application-name BasicApp --service-name UserSvc
```

If you unsure of the name of the application and service you want to query, you can find them in your cluster manager or by using `sfctl`.

Returns:

```shell
indexed_users
users
```

### Step 3: Understand schema of dictionary

IF you want to learn more about the types of the properties in your dictionary, `rcctl dictionary schema` and `rcctl dictionary type-schema` can help you understand what you are looking at.

```shell
rcctl dictionary schema --application-name BasicApp --service-name UserSvc --dictionary-name users
```

Returns:

```shell
{
    "{http://schemas.microsoft.com/ado/2009/11/edm}EntityType": {
        "@Name": "Entity_2OfUserName_UserProfile",
        "{http://schemas.microsoft.com/ado/2009/11/edm}Property": [
            {
                "@Name": "Value",
                "@Type": "Basic.Common.UserProfile"
            },
            {
                "@Name": "PartitionId",
                "@Type": "Edm.Guid",
                "@Nullable": false
            },
            {
                "@Name": "Key",
                "@Type": "Basic.Common.UserName"
            },
            {
                "@Name": "Etag",
                "@Type": "Edm.String"
            }
        ]
    }
}
```

Now we would like to understand more about the properties of a `Basic.Common.UserProfile`, so we can follow up with our query using:

```shell
rcctl dictionary type-schema --application-name BasicApp --service-name UserSvc --dictionary-name users --type-name Basic.Common.UserProfile
```

Returns:

```shell
{
    "{http://schemas.microsoft.com/ado/2009/11/edm}ComplexType": {
        "@Name": "UserProfile",
        "{http://schemas.microsoft.com/ado/2009/11/edm}Property": [
            {
                "@Name": "Email",
                "@Type": "Edm.String"
            },
            {
                "@Name": "Age",
                "@Type": "Edm.Int32",
                "@Nullable": false
            },
            {
                "@Name": "Name",
                "@Type": "Basic.Common.UserName"
            },
            {
                "@Name": "Address",
                "@Type": "Basic.Common.Address"
            }
        ]
    }
}
```

We see that the property we want to lookup the user on is `Value/Email` and that the property we want to update is `Value/Age`.

### Step 4: Query for the user we want

Now that we know the type structure of our dictionary, we can query for the user we need.

```shell
rcctl dictionary query --application-name BasicApp --service-name UserSvc --dictionary-name users --query-string "$filter= Value/Email eq 'user-0005@example.com'" --output-file user-5.json
```

Returns:

```shell
[
    {
        "PartitionId": "82b75748-a7c4-4ad3-8b16-fee77247bb8b",
        "Key": {
            "First": "First0005",
            "Last": "Last0005"
        },
        "Value": {
            "Email": "user-0005@example.com",
            "Age": 18,
            "Name": {
                "First": "First0005",
                "Last": "Last0005"
            },
            "Address": {
                "AddressLine1": "10005 Main St.",
                "AddressLine2": null,
                "City": "Seattle",
                "State": "WA",
                "Zipcode": 98117
            }
        },
        "Etag": "17399405945110410138"
    }
]
```

### Step 5: Update the user and execute against the dictionary

First, we open `user-5.json` file and change the Age to `19`.

Next we add, at the same level as `Key` and `Value`, two JSON paramaters `Collection: users` and `Operation: Update`

`Collection` specifies the dictionary to update on. This is specified because it is possible to do batch updates in a single execute to multiple dictionaries.

`Operation` specifies what the dictionary should do. The options are `Update`, `Add`, and  `Delete`.

- If you specify `Delete`, you should not change any of the schema's properties
- If you specify `Update`, you should ensure that the Key does not change
- If you specify `Add`, you should ensure that the given Key does not exist

Now our user looks like:

```shell
[
    {
        "Collection": "users"
        "Operation": "Update"
        "PartitionId": "82b75748-a7c4-4ad3-8b16-fee77247bb8b",
        "Key": {
            "First": "First0005",
            "Last": "Last0005"
        },
        "Value": {
            "Email": "user-0005@example.com",
            "Age": 19,
            "Name": {
                "First": "First0005",
                "Last": "Last0005"
            },
            "Address": {
                "AddressLine1": "10005 Main St.",
                "AddressLine2": null,
                "City": "Seattle",
                "State": "WA",
                "Zipcode": 98117
            }
        },
        "Etag": "17399405945110410138"
    }
]
```

And just like that, we have updated the information of a user using `rcctl`.
