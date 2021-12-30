# freshpy
A Python toolset for utilizing the Freshservice API

## Installation
The package can be installed via pip using the syntax below.

```sh
pip install freshpy --upgrade
```

You may also clone the repository and install from source using below.

```sh
git clone git://github.com/jeffshurtliff/freshpy.git
cd khoros/
python setup.py install
```

## Usage
This section provides basic usage instructions for the package.

### Importing the package
Rather than importing the base package, it is recommended that you import the primary `FreshPy` class using the syntax
below.

```python
from freshpy import FreshPy
```

### Initializing a Khoros object instance
The primary `FreshPy` object serves many purposes, the most important being to establish a connection to the 
Freshservice environment with which you intend to interact. As such, when initializing an instance of the `FreshPy` 
object, you will need to pass it the Freshservice URL (e.g. `example.freshservice.com`) and the API key it will use 
to authenticate so that the connection can be established.

#### Passing the information directly into the object
The domain and API key can be passed directly into the `FreshPy` object when initializing it, as
demonstrated in the example below.

```python
fresh = FreshPy(domain='example.freshservice.com', api_key='abc123DEF456')
```

### Interacting with the Freshservice API
Once the `FreshPy` object instance has been initialized, it can be leveraged to interact with a Freshservice
environment in many ways, which is fully documented in the official
[documentation](https://api.freshservice.com/). The example below demonstrates how information for a specific incident 
ticket can be retrieved in JSON format.

```python
ticket_data = fresh.tickets.get_ticket(1299)
```

## License
[MIT License](https://github.com/jeffshurtliff/freshpy/blob/master/LICENSE)

## Reporting Issues
Issues can be reported within the [GitHub repository](https://github.com/jeffshurtliff/freshpy/issues).

## Additional Resources
Additional resources for leveraging the Freshservice API can be found in the official
[Freshservice API Reference Documentation](https://api.freshservice.com/s).

## Donations
If you would like to donate to this project then you can do so using 
[this PayPal link](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=XDZ8M6UV6EFK6&item_name=FreshPy&currency_code=USD).

## Disclaimer
This package is considered unofficial and is in no way endorsed or supported by 
[Freshservice](https://www.freshservice.com).

