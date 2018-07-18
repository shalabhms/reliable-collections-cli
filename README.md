
# SFQuery
SFQuery is an easy-to-consume python package that allows you to take advantage of your query-enabled Service Fabric service. To add querying capabilities to your service visit the [service-fabric-queryable](https://github.com/jessebenson/service-fabric-queryable) repository.

## Installing
### Install python and packages
To install and start using `sfquery` make sure you have [python](https://www.python.org/getit/) 3.6 and [pip](https://pip.pypa.io/en/stable/installing/) installed (pip probably came with your python distro) , and install sfquery using
```
pip install sfquery
```
(since sfquery is not yet released install with:)
```
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple sfquery
```
### Install Jupyter Notebook
While you can consume sfquery any way you like, if you would like to use the sfquery interface, it is recommended you use a Jupyter notebook. Jupyter notebooks are powerful web application python kernels that offer widgets and interaction. You can install Jupyter notebooks using using `pip install jupyter` or [here](http://jupyter.org/install)

## How to use
To open the sfquery interface, open a new jupyter notebook. Run the following commands
```python
from sfquery import *
cluster = Cluster(Authentication(), 'http://localhost:19080/')
interface = Interface(cluster)
```
- If your cluster is deployed, replace `http://localhost:19080/` with your cluster's endpoint
- If your cluster is cert-authenticated, instead of `Authentication()` use
```python
ClientCertAuthentication(r'C:\path\to\your\unencrypted.pem', None, True)
# secondary arguments are your certificate authority and whether you want to not verify your cluster's cert
```

At this point, you should see this interface. Feel free to fiddle with it and try some OData queries.
If you want to use sfquery outside of Jupyter or without the interface, [there is a simple API that you can use and a tutorial on using it.](../master/sfquery/api.md)

![jupyter interface](../master/img/jupyter_interface.png)

### Issues
If your jupyter notebook says it cannot find `sfquery`, your notebook's python kernel may be different than the one your computer is using. You can install `sfquery` to your jupyter notebook from your notebook using:
```
!pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple sfquery
```

## Contributing

This project has adopted the
[Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information, see the
[Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any
additional questions or comments.
