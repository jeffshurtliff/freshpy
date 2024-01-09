<a href='https://pypi.org/project/freshpy/'>
    <img src="https://github.com/jeffshurtliff/freshpy/blob/main/docs/_static/freshpy-logo.png" width="100" />
</a>

# FreshPy
A Python toolset for utilizing the Freshservice API

## Usage
This section provides basic usage instructions for the package.

### Importing the package
Rather than importing the base package, it is recommended that you import the primary `FreshPy` class using the syntax
below.

```python
from freshpy import FreshPy
```

### Initializing a FreshPy object instance
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
import freshpy.tickets

ticket_id = fresh.tickets.create_ticket("email@test.org", "Subject Line", "Ticket Description", priority=4,
                                        additional={"category": "Hardware", "source": 1002})
fresh.tickets.ticket_reply(ticket_id, "Body of ticket comment")
ticket_data = fresh.tickets.get_ticket(1299)
fresh.tickets.close_ticket(ticket_id,resolution=None)
```

## Additional Resources
Additional resources for leveraging the Freshservice API can be found in the official
[Freshservice API Reference Documentation](https://api.freshservice.com/).

## Disclaimer
This package is considered unofficial and is in no way endorsed or supported by 
[Freshservice](https://www.freshservice.com).

