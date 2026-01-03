# -*- coding: utf-8 -*-
"""
:Module:            freshpy.objects
:Synopsis:          Functions for interacting with Freshservice custom objects
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     03 Jan 2026
"""

from . import api, errors
from .utils import core_utils, log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def get_custom_object(freshpy_object, object_id, verify_ssl=True):
    """This function retrieves a specific custom object.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param object_id: The ID of the custom object
    :type object_id: str, int
    :param verify_ssl:Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: Dictionary (JSON) with the custom object data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    core_utils.validate_numeric_value(object_id, 'object_id')
    uri = f'objects/{object_id}'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)


def get_all_custom_objects(freshpy_object, workspace_id=None, verify_ssl=True):
    """This function retrieves the custom objects associated with a Freshservice instance.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param workspace_id: The ID value of the workspace (defaults to primary workspace)
    :type workspace_id: str, int, None
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: Dictionary (JSON) with the custom object data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    uri = 'objects'
    if workspace_id:
        core_utils.validate_numeric_value(workspace_id, 'workspace_id')
        uri += f'?workspace_id={workspace_id}'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)
