# -*- coding: utf-8 -*-
"""
:Module:            freshpy.workspaces
:Synopsis:          Functions for interacting with Freshservice workspaces (aka clients)
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 Jan 2026
"""

from . import api, errors
from .utils import core_utils, log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def get_workspace(freshpy_object, workspace_id, verify_ssl=True):
    """This function returns data for a specific workspace.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param workspace_id: The ID value of the workspace
    :type workspace_id: str, int
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: Dictionary (JSON) with the workspace data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    core_utils.validate_numeric_value(workspace_id, 'workspace_id')
    uri = f'workspaces/{workspace_id}'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)


def get_all_workspaces(freshpy_object, verify_ssl=True):
    """This function returns data on all workspaces.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: Dictionary (JSON) with the workspace data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    uri = 'workspaces'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)
