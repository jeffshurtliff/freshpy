# -*- coding: utf-8 -*-
"""
:Module:            freshpy.core
:Synopsis:          Defines the core freshpy object used to interface with the Freshservice API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     30 Dec 2021
"""

from . import api
from . import tickets as tickets_module
from .utils import log_utils, version

# Initialize logging
logger = log_utils.initialize_logging(__name__)


class FreshPy(object):
    """This is the class for the core object leveraged in this library."""
    # Define the function that initializes the object instance (i.e. instantiates the object)
    def __init__(self, domain=None, api_key=None):
        """This method instantiates the core Fresh object.

        .. versionadded:: 1.0.0
        """
        # Define the current version
        self.version = version.get_full_version()

        # Define the domain
        domain = f'https://{domain}' if domain and not domain.startswith('http') else domain
        domain = domain[:-1] if domain.endswith('/') else domain
        self.domain = domain

        # Define the base URL
        self.base_url = f'{domain}/api/v2/'

        # Define the API key
        self.api_key = api_key

        # Import inner object classes so their methods can be called from the primary object
        self.tickets = self._import_tickets_class()

    def _import_tickets_class(self):
        """This method allows the :py:class:`freshpy.core.FreshPy.Tickets` class to be utilized in the core object.

        .. versionadded:: 1.0.0
        """
        return FreshPy.Tickets(self)

    def get(self, uri, headers=None, return_json=True):
        """This method performs a GET request against the Freshservice API with multiple retries on failure.

        .. versionadded:: 1.0.0

        :param uri: The URI to query
        :type uri: string
        :param headers: The HTTP headers to utilize in the REST API call
        :type headers: dict, None
        :param return_json: Determines if JSON data should be returned
        :type return_json: bool
        :returns: The JSON data from the response or the raw :py:mod:`requests` response.
        :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`
        """
        return api.get_request_with_retries(self, uri, headers, return_json)

    class Tickets(object):
        """This class includes methods associated with Freshservice tickets."""
        def __init__(self, freshpy_object):
            """This method initializes the :py:class:`freshpy.core.freshpy.Tickets` inner class object.

            .. versionadded:: 1.0.0

            :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
            :type freshpy_object: class[freshpy.FreshPy]
            """
            self.freshpy_object = freshpy_object

        def get_ticket(self, ticket_number, include=None):
            """This function returns the data for a specific ticket.

            .. versionadded:: 1.0.0

            :param ticket_number: The ticket number for which to return data
            :type ticket_number: str, int
            :param include: A string or iterable of `embedding <https://api.freshservice.com/#view_a_ticket>`_ options
            :type include: str, tuple, list, set, None
            :returns: JSON data for the given ticket
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`
            """
            return tickets_module.get_ticket(self.freshpy_object, ticket_number, include)

    def __del__(self):
        """This method fully destroys the instance.

        .. versionadded:: 1.0.0
        """
        self.close()

    def close(self):
        """This core method destroys the instance.

        .. versionadded:: 1.0.0
        """
