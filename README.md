
# Query your reliable collections using `rcctl`
### `rcctl` is an easy-to-consume python package that allows you to interact with your query-enabled Service Fabric service using command line or python. 

**`rcctl` only works for query-enabled services. To add querying capabilities to your service visit the [service-fabric-queryable](https://github.com/jessebenson/service-fabric-queryable) repository.**

## Installing
To install and start using `rcctl`, make sure you have [python](https://www.python.org/getit/) <= 3.6 and [pip](https://pip.pypa.io/en/stable/installing/) installed (pip may have came with your python distro). Then, install `rcctl` using
```
pip install rcctl
```

## Using `rcctl`
To get started, simply open a command prompt window and enter
```
rcctl -h
```
If your cluster is not an a local endpoint, you must connect to it using `rcctl cluster select` before being able to interact with your service. [Connecting to a cluster in `rcctl` works the same way as it does in `sfctl`.](https://docs.microsoft.com/en-us/azure/service-fabric/service-fabric-cli#select-a-cluster)

Once you have connected, you can use `rcctl collections` to `list` your reliable collections, find out about the `schema` of a reliable collection, and then find out more about any complex `type` in that schema. You can then `query` against any collection in your query-enabled service, and `execute` updates to that collection.

Queries against service-fabric-querying are written in the [OData format](https://www.odata.org/documentation/odata-version-2-0/uri-conventions/). `Querying` supports the following commands, which can be thought of like SQL:

| SQL | OData |
| --- | ---- |
| SELECT | $select |
| LIMIT | $top |
| WHERE | $filter |
| ORDER BY | $orderby |

`Querying` supports all the *logical operators* provided by the [OData convention](http://docs.oasis-open.org/odata/odata/v4.01/cs01/part2-url-conventions/odata-v4.01-cs01-part2-url-conventions.html#sec_LogicalOperators).

## Using the `sfquery` interface
`rcctl` is the command line wrapper of its underlying package `sfquery`. If instead of command line, you would like to use the `sfquery interface`, you can do so in a Jupyter notebook. Jupyter notebooks are local, web-based python kernels that offer widgets and interaction.

To open the `sfquery interface`, open a new jupyter notebook by entering in command line
```
jupyter notebook
```
That should open up a web browser. You can then make a new `python3` notebook and enter the following:
```python
from sfquery import *
cluster = Cluster(Authentication(), 'http://localhost:19080/')
interface = Interface(cluster)
```
- If your cluster is deployed, replace `http://localhost:19080/` with your cluster's endpoint
- If your cluster is cert-authenticated, instead of `Authentication()` use
```python
ClientCertAuthentication(r"C:\path\to\your\unencrypted.pem", None, True)
# secondary arguments are your certificate authority and whether you want to not verify your cluster's cert
```
At this point, you should see this interface. Feel free to fiddle with it and try some OData queries.

![jupyter interface](../master/img/jupyter_interface.png)

If your jupyter notebook says it cannot find `sfquery`, your notebook's python kernel may be different than the one your computer is using. You can install `sfquery` to your jupyter notebook from your notebook using:
```
!pip install sfquery
```

## Using the `sfquery` API
For more advanced usage, you may want to use the `sfquery` python package directly. You can find the API documentation [here](../master/sfquery/api.md).

## Contributing

Contributions are welcome on this project. See [Contributing.md](../master/Contributing.md) for information on how to go about contributing to this project.
