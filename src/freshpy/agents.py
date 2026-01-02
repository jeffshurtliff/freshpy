# -*- coding: utf-8 -*-
"""
:Module:            freshpy.agents
:Synopsis:          Functions for interacting with Freshservice agents
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Jan 2026
"""

from . import api, errors
from .api import DEFAULT_SSL_VERIFY
from .utils import core_utils, log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def get_user_info(freshpy_object, lookup_value, verify_ssl=True):
    """This function retrieves user data for a specific agent.

    .. version-added:: 2.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param lookup_value: An Agent ID or email address with which to look up the user
    :tyype lookup_value: str, int
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: JSON data with the agent user data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`,
             :py:exc:`freshpy.errors.exceptions.InvalidFieldError`
    """
    # Identify the lookup value and retrieve the data
    if isinstance(lookup_value, str) and '@' in lookup_value:
        agent_data = _get_user_info_by_email(freshpy_object, lookup_value, verify_ssl)
        agent_data = agent_data['agents'][0]
    elif isinstance(lookup_value, int) or (isinstance(lookup_value, str) and lookup_value.isdigit()):
        uri = f'agents/{lookup_value}'
        agent_data = api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)
        agent_data = agent_data['agent'] if 'agent' in agent_data else agent_data
    else:
        raise errors.exceptions.InvalidFieldError('An invalid Agent ID or email address was provided.')

    # Return the agent user data
    return agent_data


def _get_user_info_by_email(_freshpy_object, _email, _verify_ssl=True):
    """This function retrieves data for an agent using its email address as a query filter.

    .. version-added:: 2.0.0

    :param _freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type _freshpy_object: class[freshpy.FreshPy]
    :param _email: The email address to be used in the query filter
    :type _email: str
    :param _verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type _verify_ssl: bool
    :returns: JSON data with the agent user data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`,
             :py:exc:`freshpy.errors.exceptions.InvalidFieldError`
    """
    # Validate the provided email address
    if not isinstance(_email, str) or '@' not in _email:
        raise errors.exceptions.InvalidFieldError('An invalid email address was provided.')

    # Retrieve the agent data based on the email address
    _uri = f'agents?email={core_utils.url_encode(_email)}'
    return api.get_request_with_retries(_freshpy_object, _uri, verify_ssl=_verify_ssl)


def get_all_agents(freshpy_object, only_active=None, only_inactive=None, verify_ssl=True):
    """This function returns data for all agents with an optional filters for active or inactive users.

    .. version-added:: 2.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param only_active: Filters for only active agents when ``True``
    :type only_active: bool, None
    :param only_inactive: Filters for only inactive agents when ``True``
    :type only_inactive: bool, None
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: JSON data with user data for all agents
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    # Define the filter string if necessary
    filter_string = ''
    if only_active is not None or only_inactive is not None:
        if only_active is True and only_inactive is True:
            exc_msg = 'You cannot use both the only_active and only_inactive filters in the same call.'
            raise errors.exceptions.InvalidFilterError(exc_msg)
        elif only_active:
            filter_string = '?active=true'
        elif only_inactive is True:
            filter_string = '?active=false'

    # Construct the URI and perform the API call
    uri = 'agents' + filter_string
    return api.get_request_with_retries(freshpy_object, uri, verify_ssl=verify_ssl)


def get_agent_id(freshpy_object, email, verify_ssl=True):
    """This function retrieves the Agent ID value for a specific agent.

    .. version-added:: 2.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param email: The email address of the agent
    :type email: str
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: The Agent ID of the agent as an integer
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`,
             :py:exc:`freshpy.errors.exceptions.NotFoundResponseError`,
             :py:exc:`freshpy.errors.exceptions.InvalidFieldError`
    """
    # Retrieve the agent data based on the email address
    agent_data = _get_user_info_by_email(freshpy_object, email, verify_ssl)

    # Raise an exception if no data was found for the user (API response was 404)
    if 'status_code' in agent_data and agent_data['status_code'] == 404:
        raise errors.exceptions.NotFoundResponseError('An agent ID was not found for the provided email address.')

    # Parse the retrieved data to obtain and return the agent ID
    try:
        agent_data = agent_data['agents'][0]['id']
    except IndexError:
        raise errors.exceptions.NotFoundResponseError('An agent ID was not found for the provided email address.')
    return agent_data


def get_assignment_history(freshpy_object, lookup_value, verify_ssl=True):
    """This function retrieves the user assignment history for a specific agent.

    .. version-added:: 2.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param lookup_value: An Agent ID or email address with which to look up the user
    :tyype lookup_value: str, int
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: JSON data for the assignment history for the agent
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`,
             :py:exc:`freshpy.errors.exceptions.NotFoundResponseError`,
             :py:exc:`freshpy.errors.exceptions.InvalidFieldError`
    """
    # Identify the agent ID for the user
    if isinstance(lookup_value, int) or (isinstance(lookup_value, str) and lookup_value.isdigit()):
        agent_id = lookup_value
    elif isinstance(lookup_value, str) and '@' in lookup_value:
        agent_id = get_agent_id(freshpy_object, lookup_value, verify_ssl)
    else:
        raise errors.exceptions.InvalidFieldError('An invalid Agent ID or email address was provided.')

    # Construct the URI and perform the API call
    uri = f'users/{agent_id}/assignment-history'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)


def get_agent_role(freshpy_object, role_id, verify_ssl=DEFAULT_SSL_VERIFY):
    """This function returns data for a specific agent role.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param role_id: The numeric ID of the agent role
    :type role_id: str, int
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: A JSON-formatted dictionary with the agent role data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    core_utils.validate_numeric_value(role_id, 'role_id')
    uri = f'roles/{role_id}'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)


def get_all_agent_roles(freshpy_object, verify_ssl=DEFAULT_SSL_VERIFY):
    """This function returns data for all agent roles.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: A JSON-formatted dictionary with the agent role data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    uri = 'roles'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)


def get_agent_group(freshpy_object, group_id, verify_ssl=DEFAULT_SSL_VERIFY):
    """This function returns data for a specific agent group.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param group_id: The numeric ID of the agent group
    :type group_id: str, int
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: A JSON-formatted dictionary with the agent group data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    core_utils.validate_numeric_value(group_id, 'group_id')
    uri = f'groups/{group_id}'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)


def get_all_agent_groups(freshpy_object, verify_ssl=DEFAULT_SSL_VERIFY):
    """This function returns data for all agent groups.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: A JSON-formatted dictionary with the agent group data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    uri = 'groups'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)
