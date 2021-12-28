# -*- coding: utf-8 -*-
"""
:Module:            freshpy.api
:Synopsis:          This module handles interactions with the Freshservice REST API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     28 Dec 2021
"""

import json

import requests

from .utils import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def define_headers():
    """This function defines the headers to use in API calls.

    .. versionadded:: 1.0.0
    """
    headers = {'Content-Type': 'application/json'}
    return headers


def define_auth(api_key):
    """This function defines the authentication dictionary to use in API calls."""
    credentials = (api_key, 'X')
    return credentials


def get_request_with_retries(fresh_object, uri, headers=None, return_json=True):
    """This function performs a GET request and will retry several times if a failure occurs.

    .. versionadded:: 1.0.0

    :param fresh_object: The instantiated :py:class:`freshpy.core.FreshPy` object.
    :param uri: The URI to query
    :type uri: string
    :param headers: The HTTP headers to utilize in the REST API call
    :type headers: dict, None
    :param return_json: Determines if JSON data should be returned
    :type return_json: bool
    :returns: The JSON data from the response or the raw :py:mod:`requests` response.
    """
    # Define headers if not supplied
    headers = define_headers() if not headers else headers

    # Construct the credentials dictionary
    credentials = define_auth(fresh_object.api_key)

    # Construct the query URL
    query_url = fresh_object.base_url + uri

    # Perform the API call
    retries, response = 0, None
    while retries <= 5:
        try:
            response = requests.get(query_url, headers=headers, auth=credentials)
            break
        except Exception as exc_msg:
            # _report_failed_attempt(exc_msg, 'get', retries)
            retries += 1
    if retries == 6:
        # _raise_exception_for_repeated_timeouts()
        pass
    if return_json:
        response = response.json()
    return response



