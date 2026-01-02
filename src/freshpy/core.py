# -*- coding: utf-8 -*-
"""
:Module:            freshpy.core
:Synopsis:          Defines the core freshpy object used to interface with the Freshservice API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Dec 2026
"""

import os
import inspect

import freshpy.errors.exceptions
from . import api, errors
from . import agents as agents_module
from . import tickets as tickets_module
from . import workspaces as workspaces_module
from .utils import log_utils, version

# Initialize logging
logger = log_utils.initialize_logging(__name__)


class FreshPy(object):
    """This is the class for the core object leveraged in this library."""
    def __init__(self, domain=None, api_key=None, env_variables=None, verify_ssl=None):
        """This method instantiates the core FreshPy object.

        .. version-changed:: 3.0.0
           Made multiple improvements to the object class and methods. (See changelog for full details)

        .. version-added:: 1.0.0
        """
        # Define the default settings
        self.version = version.get_full_version()
        self._env_variables = {}

        # Check for custom environment variable names
        if env_variables:
            if not isinstance(env_variables, dict):
                logger.error("The 'env_variables' parameter must be a dictionary and will be ignored.")
            else:
                self._env_variable_names = self._get_env_variable_names(env_variables)
        else:
            self._env_variable_names = self._get_env_variable_names()

        # Check for any defined environment variables
        self._env_variables = self._get_env_variables()

        # Ensure the domain was supplied as it is required and raise an exception if not
        if domain:
            logger.debug('The domain value was defined via parameter when instantiating the core object')
        elif 'domain' in self._env_variables and self._env_variables.get('domain'):
            domain = self._env_variables.get('domain')
            logger.debug('The domain value was defined as an environment variable')
        else:
            logger.critical('The domain value could not be defined and the object cannot be instantiated')
            raise errors.exceptions.MissingRequiredDataError('init', argument='domain')

        # Ensure the API key was supplied as it is required and raise an exception if not
        if api_key:
            logger.debug('The api_key value was defined via parameter when instantiating the core object')
        elif 'api_key' in self._env_variables and self._env_variables.get('api_key'):
            api_key = self._env_variables.get('api_key')
            logger.debug('The api_key value was defined as an environment variable')
        else:
            logger.critical('The api_key value could not be defined and the object cannot be instantiated')
            raise errors.exceptions.MissingRequiredDataError('init', argument='api_key')

        # Define the domain
        domain = f'https://{domain}' if domain and not domain.startswith('http') else domain
        domain = domain[:-1] if domain.endswith('/') else domain
        self.domain = domain

        # Define the base URL
        self.base_url = f'{domain}/api/v2/'

        # Define the API key
        self.api_key = api_key

        # Determine if SSL verification should occur at the object level (True by default)
        self.verify_ssl = True if not verify_ssl else verify_ssl
        self.verify_ssl = True if not isinstance(self.verify_ssl, bool) else self.verify_ssl

        # Import inner object classes so their methods can be called from the primary object
        self.agents = self._import_agents_class()
        self.tickets = self._import_tickets_class()
        self.workspaces = self._import_workspaces_class()

    def _import_agents_class(self):
        """This method allows the :py:class:`freshpy.core.FreshPy.Agents` class to be utilized in the core object.

        .. version-added:: 2.0.0
        """
        return FreshPy.Agents(self)

    def _import_tickets_class(self):
        """This method allows the :py:class:`freshpy.core.FreshPy.Tickets` class to be utilized in the core object.

        .. version-added:: 1.0.0
        """
        return FreshPy.Tickets(self)

    def _import_workspaces_class(self):
        """This method allows the :py:class:`freshpy.core.FreshPy.Workspaces` class to be utilized in the core object.

        .. version-added:: 3.0.0
        """
        return FreshPy.Workspaces(self)

    def _determine_ssl_verification(self, param_value=None):
        """This method checks to determine if SSL verification is enabled at the object or function/method level.

        .. version-added:: 3.0.0

        :param param_value: Value of the ``verify_ssl`` parameter from a parent function/method
        :type param_value: bool, None
        :returns: Boolean value indicating whether SSL verification is enabled
        """
        # Define the variable that will ultimately be returned
        ssl_verification = None

        # Get the name of the parent function or method that called this method
        frame = inspect.currentframe()
        try:
            caller = frame.f_back
            parent_name = caller.f_code.co_name
        except Exception as exc:
            parent_name = 'parent_function_or_method'
            exc_type = type(exc).__name__
            logger.error(f'Failed to identify parent function or method due to {exc_type} exception')
        finally:
            # Prevent reference cycles
            del frame

        # Check if the SSL verification was set explicitly by the parent function/method
        if param_value is not None:
            if isinstance(param_value, bool):
                ssl_verification = param_value
                if not ssl_verification:
                    logger.warning(f'SSL verification was disabled explicitly by {parent_name} for API calls')
            else:
                logger.error(f'The verify_ssl parameter from {parent_name} is not a Boolean and will be ignored')

        # Leverage the object-level setting if defined
        if ssl_verification is None and self.verify_ssl is not None and isinstance(self.verify_ssl, bool):
            ssl_verification = self.verify_ssl

        elif ssl_verification is None:
            # Force SSL verification by default
            ssl_verification = True
            logger.debug('SSL verification will be enabled by default as the setting has not been defined')

        # Return the final Boolean value indicating if SSL verification should occur
        return ssl_verification

    @staticmethod
    def _get_env_variable_names(_custom_dict=None):
        """This function returns the environment variable names to use when checking the OS for environment variables.

        .. version-added:: 3.0.0

        :param _custom_dict: Custom environment variable names to use instead of the defaults (from ``env_variables``
                             parameter when instantiating the core object)
        :type _custom_dict: dict, None
        :returns: Dictionary containing the settings and their associated environment variable names
        :raises: :py:exc:`freshpy.errors.exceptions.DataMismatchError`
        """
        # Define the dictionary with the default environment variable names
        _env_variable_names = {
            'domain': 'FRESHPY_DOMAIN',
            'api_key': 'FRESHPY_API_KEY',
            'verify_ssl': 'FRESHPY_VERIFY_SSL',
        }

        # Update the dictionary to use any defined custom names instead of the default names
        _custom_dict = {} if _custom_dict is None else _custom_dict
        if not isinstance(_custom_dict, dict):
            exc_msg = "Cannot parse custom environment variable names as 'env_variables' parameter is not a dictionary."
            logger.critical(exc_msg)
            raise freshpy.errors.exceptions.DataMismatchError(exc_msg)
        if _custom_dict:
            for _name_key, _name_value in _custom_dict.items():
                if _name_key in _env_variable_names:
                    _env_variable_names.update({_name_key: _name_value})

        # Return the finalized dictionary with the mapped environment variable names
        return _env_variable_names

    def _get_env_variables(self):
        """This function retrieves any defined environment variables to use with the instantiated core object.

        .. version-added:: 3.0.0

        :returns: Dictionary containing the environment variables and their respective values
        """
        _env_variables = {}
        for _config_name, _var_name in self._env_variable_names.items():
            _var_value = os.getenv(_var_name)                               # Returns None if not found
            _env_variables.update({_config_name: _var_value})
        return _env_variables

    def get(self, uri, headers=None, return_json=True, verify_ssl=None):
        """This method performs a GET request against the Freshservice API with multiple retries on failure.

        .. version-changed:: 3.0.0
           Changed the default ``verify_ssl`` parameter to be ``None`` and called method to check SSL verification

        .. version-changed:: 1.1.0
           Added the ability to disable SSL verification on API calls.

        .. version-added:: 1.0.0

        :param uri: The URI to query
        :type uri: string
        :param headers: The HTTP headers to utilize in the REST API call
        :type headers: dict, None
        :param return_json: Determines if JSON data should be returned
        :type return_json: bool
        :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
        :type verify_ssl: bool
        :returns: The JSON data from the response or the raw :py:mod:`requests` response.
        :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
                 :py:exc:`freshpy.errors.exceptions.DataMismatchError`
        """
        verify_ssl = self._determine_ssl_verification(verify_ssl)
        return api.get_request_with_retries(self, uri, headers, return_json, verify_ssl=verify_ssl)

    class Agents(object):
        """This class includes methods associated with Freshservice agents."""
        def __init__(self, freshpy_object):
            """This method initializes the :py:class:`freshpy.core.freshpy.Tickets` inner class object.

            .. version-added:: 2.0.0

            :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
            :type freshpy_object: class[freshpy.FreshPy]
            """
            self.freshpy_object = freshpy_object

        def get_user_info(self, lookup_value, verify_ssl=None):
            """This function retrieves user data for a specific agent.

            .. version-changed:: 3.0.0
               Changed the default ``verify_ssl`` parameter to be ``None`` and called method to check SSL verification

            .. version-added:: 2.0.0

            :param lookup_value: An Agent ID or email address with which to look up the user
            :tyype lookup_value: str, int
            :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
            :type verify_ssl: bool
            :returns: JSON data with the agent user data
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
                     :py:exc:`freshpy.errors.exceptions.InvalidFieldError`,
                     :py:exc:`freshpy.errors.exceptions.DataMismatchError`
            """
            verify_ssl = self.freshpy_object._determine_ssl_verification(verify_ssl)
            return agents_module.get_user_info(self.freshpy_object, lookup_value=lookup_value, verify_ssl=verify_ssl)

        def get_all_agents(self, only_active=None, only_inactive=None, verify_ssl=None):
            """This function returns data for all agents with an optional filters for active or inactive users.

            .. version-changed:: 3.0.0
               Changed the default ``verify_ssl`` parameter to be ``None`` and called method to check SSL verification

            .. version-added:: 2.0.0

            :param only_active: Filters for only active agents when ``True``
            :type only_active: bool, None
            :param only_inactive: Filters for only inactive agents when ``True``
            :type only_inactive: bool, None
            :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
            :type verify_ssl: bool
            :returns: JSON data with user data for all agents
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
                     :py:exc:`freshpy.errors.exceptions.DataMismatchError`
            """
            verify_ssl = self.freshpy_object._determine_ssl_verification(verify_ssl)
            return agents_module.get_all_agents(self.freshpy_object, only_active=only_active,
                                                only_inactive=only_inactive, verify_ssl=verify_ssl)

        def get_agent_id(self, email, verify_ssl=None):
            """This function retrieves the Agent ID value for a specific agent.

            .. version-changed:: 3.0.0
               Changed the default ``verify_ssl`` parameter to be ``None`` and called method to check SSL verification

            .. version-added:: 2.0.0

            :param email: The email address of the agent
            :type email: str
            :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
            :type verify_ssl: bool
            :returns: The Agent ID of the agent as an integer
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
                     :py:exc:`freshpy.errors.exceptions.NotFoundResponseError`,
                     :py:exc:`freshpy.errors.exceptions.InvalidFieldError`,
                     :py:exc:`freshpy.errors.exceptions.DataMismatchError`
            """
            verify_ssl = self.freshpy_object._determine_ssl_verification(verify_ssl)
            return agents_module.get_agent_id(self.freshpy_object, email=email, verify_ssl=verify_ssl)

        def get_assignment_history(self, lookup_value, verify_ssl=None):
            """This function retrieves the user assignment history for a specific agent.

            .. version-changed:: 3.0.0
               Changed the default ``verify_ssl`` parameter to be ``None`` and called method to check SSL verification

            .. version-added:: 2.0.0

            :param lookup_value: An Agent ID or email address with which to look up the user
            :tyype lookup_value: str, int
            :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
            :type verify_ssl: bool
            :returns: JSON data for the assignment history for the agent
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
                     :py:exc:`freshpy.errors.exceptions.NotFoundResponseError`,
                     :py:exc:`freshpy.errors.exceptions.InvalidFieldError`,
                     :py:exc:`freshpy.errors.exceptions.DataMismatchError`
            """
            verify_ssl = self.freshpy_object._determine_ssl_verification(verify_ssl)
            return agents_module.get_assignment_history(self.freshpy_object, lookup_value=lookup_value,
                                                        verify_ssl=verify_ssl)

    class Tickets(object):
        """This class includes methods associated with Freshservice tickets."""
        def __init__(self, freshpy_object):
            """This method initializes the :py:class:`freshpy.core.freshpy.Tickets` inner class object.

            .. version-added:: 1.0.0

            :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
            :type freshpy_object: class[freshpy.FreshPy]
            """
            self.freshpy_object = freshpy_object

        def get_ticket(self, ticket_number, include=None, verify_ssl=None):
            """This method returns the data for a specific ticket.

            .. version-changed:: 3.0.0
               Changed the default ``verify_ssl`` parameter to be ``None`` and called method to check SSL verification

            .. version-changed:: 2.0.0
               Updated the function call to use keyword arguments.

            .. version-changed:: 1.1.0
               Added the ability to disable SSL verification on API calls.

            .. version-added:: 1.0.0

            :param ticket_number: The ticket number for which to return data
            :type ticket_number: str, int
            :param include: A string or iterable of `embedding <https://api.freshservice.com/#view_a_ticket>`_ options
            :type include: str, tuple, list, set, None
            :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
            :type verify_ssl: bool
            :returns: JSON data for the given ticket
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
                     :py:exc:`freshpy.errors.exceptions.DataMismatchError`
            """
            verify_ssl = self.freshpy_object._determine_ssl_verification(verify_ssl)
            return tickets_module.get_ticket(self.freshpy_object, ticket_number=ticket_number, include=include,
                                             verify_ssl=verify_ssl)

        def get_tickets(self, include=None, predefined_filter=None, filters=None, filter_logic='AND', requester_id=None,
                        requester_email=None, ticket_type=None, updated_since=None, ascending=None, descending=None,
                        per_page=None, page=None, verify_ssl=None):
            """This method returns a sequence of tickets with optional filters.

            .. version-changed:: 3.0.0
               Changed the default ``verify_ssl`` parameter to be ``None`` and called method to check SSL verification

            .. version-changed:: 1.1.0
               Added the ability to disable SSL verification on API calls.

            .. version-added:: 1.0.0

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
            :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
            :type verify_ssl: bool
            :returns: A list of JSON objects for tickets
            :raises: :py:exc:`freshpy.errors.exceptions.InvalidPredefinedFilterError`,
                     :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
                     :py:exc:`freshpy.errors.exceptions.DataMismatchError`
            """
            verify_ssl = self.freshpy_object._determine_ssl_verification(verify_ssl)
            return tickets_module.get_tickets(self.freshpy_object, include=include, predefined_filter=predefined_filter,
                                              filters=filters, filter_logic=filter_logic, requester_id=requester_id,
                                              per_page=per_page, page=page, requester_email=requester_email,
                                              ticket_type=ticket_type, updated_since=updated_since, ascending=ascending,
                                              descending=descending, verify_ssl=verify_ssl)

        def get_ticket_fields(self, verify_ssl=None):
            """This method retrieves the standard and custom fields that exist for tickets.

            .. version-added:: 3.0.0

            :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
            :type verify_ssl: bool
            :returns: Dictionary (JSON) with the ticket field data
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
                     :py:exc:`freshpy.errors.exceptions.DataMismatchError`
            """
            verify_ssl = self.freshpy_object._determine_ssl_verification(verify_ssl)
            return tickets_module.get_ticket_fields(self.freshpy_object, verify_ssl=verify_ssl)

    class Workspaces(object):
        """This class includes methods associated with Freshservice workspaces/clients."""
        def __init__(self, freshpy_object):
            """This method initializes the :py:class:`freshpy.core.freshpy.Workspaces` inner class object.

            .. version-added:: 3.0.0

            :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
            :type freshpy_object: class[freshpy.FreshPy]
            """
            self.freshpy_object = freshpy_object

        def get_workspace(self, workspace_id, verify_ssl=None):
            """This method returns data for a specific workspace.

            .. version-added:: 3.0.0

            :param workspace_id: The ID value of the workspace
            :type workspace_id: str, int
            :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
            :type verify_ssl: bool
            :returns: Dictionary (JSON) with the workspace data
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`
            """
            verify_ssl = self.freshpy_object._determine_ssl_verification(verify_ssl)
            return workspaces_module.get_workspace(self.freshpy_object, workspace_id, verify_ssl=verify_ssl)

        def get_all_workspaces(self, verify_ssl=None):
            """This method returns data on all workspaces.

            .. version-added:: 3.0.0

            :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
            :type verify_ssl: bool
            :returns: Dictionary (JSON) with the workspace data
            :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
                     :py:exc:`freshpy.errors.exceptions.DataMismatchError`
            """
            verify_ssl = self.freshpy_object._determine_ssl_verification(verify_ssl)
            return workspaces_module.get_all_workspaces(self.freshpy_object, verify_ssl=verify_ssl)

    def __del__(self):
        """This method fully destroys the instance.

        .. version-added:: 1.0.0
        """
        self.close()

    def close(self):
        """This core method destroys the instance.

        .. version-added:: 1.0.0
        """
