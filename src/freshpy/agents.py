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
    uri = f'agents/{agent_id}'
    return api.get_request_with_retries(freshpy_object, uri, verify_ssl=verify_ssl)

