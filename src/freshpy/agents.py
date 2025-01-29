# -*- coding: utf-8 -*-
"""
:Module:            freshpy.agents
:Synopsis:          Functions for interacting with Freshservice agents
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     29 Jan 2025
"""

from . import api, errors
from .utils import core_utils, log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def get_user_info(freshpy_object, agent_id, verify_ssl=True):
    """This function retrieves user data for a specific agent.

    .. versionadded:: 2.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param agent_id: The numeric ID for the agent for which to retrieve data
    :tyype agent_id: str, int
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: JSON data with the agent user data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`
    """
    # Construct the URI and perform the API call
    uri = f'agents/{agent_id}'
    return api.get_request_with_retries(freshpy_object, uri, verify_ssl=verify_ssl)


def get_all_agents(freshpy_object, only_active=None, only_inactive=None, verify_ssl=True):
    """This function returns data for all agents with an optional filters for active or inactive users.

    .. versionadded:: 2.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param only_active: Filters for only active agents when ``True``
    :type only_active: bool, None
    :param only_inactive: Filters for only inactive agents when ``True``
    :type only_inactive: bool, None
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: JSON data with user data for all agents
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`
    """
    # Define the filter string if necessary
    filter_string = ''
    if only_active is not None or only_inactive is not None:
        if only_active is True and only_inactive is True:
            exc_msg = 'You cannot use both the only_active and only_inactive filters in the same call.'
            raise errors.exceptions.InvalidFilterError(exc_msg)
        elif only_active is True:
            filter_string = '?active=true'
        elif only_inactive is True:
            filter_string = '?active=false'

    # Construct the URI and perform the API call
    uri = 'agents' + filter_string
    return api.get_request_with_retries(freshpy_object, uri, verify_ssl=verify_ssl)
