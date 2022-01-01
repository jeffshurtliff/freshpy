# -*- coding: utf-8 -*-
"""
:Module:            freshpy.core
:Synopsis:          Defines the core freshpy object used to interface with the Freshservice API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     01 Jan 2022
"""

from . import api, errors
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

        # Raise an exception if the domain and API key were not supplied
        if not domain or not api_key:
            raise errors.exceptions.MissingRequiredDataError('init')

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
            """This method returns the data for a specific ticket.

            .. versionadded:: 1.0.0

            :param ticket_number: The ticket number for which to return data
            :type ticket_number: str, int
            :param include: A string or iterable of `embedding <https://api.freshservice.com/#view_a_ticket>`_ options
            :type include: str, tuple, list, set, None
            :returns: JSON data for the given ticket
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`
            """
            return tickets_module.get_ticket(self.freshpy_object, ticket_number, include)

        def get_tickets(self, include=None, predefined_filter=None, filters=None, filter_logic='AND', requester_id=None,
                        requester_email=None, ticket_type=None, updated_since=None, ascending=None, descending=None,
                        per_page=None, page=None):
            """This method returns a sequence of tickets with optional filters.

            .. versionadded:: 1.0.0

            :param include: A string or iterable of `embedding <https://api.freshservice.com/#view_a_ticket>`_ options
            :type include: str, tuple, list, set, None
            :param predefined_filter: One of the predefined filters ('new_and_my_open', 'watching', 'spam', 'deleted')
            :type predefined_filter: str, None
            :param filters: Query filter(s) in the form of a structured query string or a dictionary of values
            :type filters: str, dict, None
            :param filter_logic: Defines the logic to use as necessary in a filter query string (default is ``AND``)
            :param requester_id: The numeric ID of a requester
            :param requester_id: The numeric ID of a requester
            :type requester_id: str, int, None
            :param requester_email: The email address of a requester
            :type requester_email: str, None
            :param ticket_type: The type of ticket (e.g. ``Incident``, ``Service Request``, etc.)
            :type ticket_type: str, None
            :param updated_since: A threshold date or timestamp (in UTC format) for when the ticket was last updated
            :type updated_since: str, None
            :param ascending: Determines if the tickets should be sorted in *ascending* order
            :type ascending: bool, None
            :param descending: Determines if the tickets should be sorted in *descending* order (default)
            :type descending: bool, None
            :param per_page: Displays a certain number of results per query
            :type per_page: str, int, None
            :param page: Returns a specific page number (used for paginated results)
            :type page: str, int, None
            :returns: A list of JSON objects for tickets
            :raises: :py:exc:`freshpy.errors.exceptions.InvalidPredefinedFilterError`,
                     :py:exc:`freshpy.errors.exceptions.APIConnectionError`
            """
            return tickets_module.get_tickets(self.freshpy_object, include=include, predefined_filter=predefined_filter,
                                              filters=filters, filter_logic=filter_logic, requester_id=requester_id,
                                              per_page=per_page, page=page, requester_email=requester_email,
                                              ticket_type=ticket_type, updated_since=updated_since, ascending=ascending,
                                              descending=descending)

    def __del__(self):
        """This method fully destroys the instance.

        .. versionadded:: 1.0.0
        """
        self.close()

    def close(self):
        """This core method destroys the instance.

        .. versionadded:: 1.0.0
        """
