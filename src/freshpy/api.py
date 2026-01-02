# -*- coding: utf-8 -*-
"""
:Module:            freshpy.api
:Synopsis:          This module handles interactions with the Freshservice REST API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Jan 2026
"""

import requests

from . import errors
from .utils import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)

# Define constants
DEFAULT_TIMEOUT_SECONDS = 30
DEFAULT_SSL_VERIFY = True


def define_headers():
    """This function defines the headers to use in API calls.

    .. version-added:: 1.0.0

    :returns: Dictionary defining the minimum required header keys and values for API calls
    """
    headers = {'Content-Type': 'application/json'}
    return headers


def define_auth(api_key):
    """This function defines the authentication dictionary to use in API calls.

    .. version-added:: 1.0.0

    :returns: Tuple in the appropriate format to be used as API credentials
    """
    credentials = (api_key, 'X')
    return credentials


def get_request_with_retries(freshpy_object, uri, headers=None, return_json=True, verify_ssl=DEFAULT_SSL_VERIFY):
    """This function performs a GET request and will retry several times if a failure occurs.

    .. version-changed:: 3.0.0
       Several improvements were introduced to promote scalability and reliability with GET requests.

    .. version-added:: 1.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
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
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    # Define headers if not supplied
    headers = define_headers() if not headers else headers

    # Construct the credentials dictionary
    credentials = define_auth(freshpy_object.api_key)

    # Construct the query URL
    query_url = freshpy_object.base_url + uri

    # Perform the API call
    retries, response = 0, None
    while retries <= 5:
        try:
            response = requests.get(query_url, headers=headers, auth=credentials, verify=verify_ssl)
            break
        except Exception as exc_msg:
            _report_failed_attempt(exc_msg, 'get', retries)
            retries += 1
    if retries == 6:
        _raise_exception_for_repeated_timeouts()
    if return_json:
        if response.status_code == 404:
            response = {
                'status': 'error',
                'status_code': 404,
                'error_message': 'Data not found',
            }
        else:
            try:
                response = response.json()
            except Exception as exc:
                # response = {
                #     'status': 'exception',
                #     'status_code': None,
                #     'exception_type': errors.handlers.get_exception_type(exc),
                #     'error_message': f'{exc}',
                # }
                exc_type = errors.handlers.get_exception_type(exc)
                logger.error(f'Failed to convert the API response to JSON format due to the following {exc_type} '
                             f'exception and the full Response object will be returned: {exc}')
    return response


def api_call_with_payload(freshpy_object, method, uri, payload, params=None, headers=None,
                          timeout=DEFAULT_TIMEOUT_SECONDS, show_full_error=True, return_json=True,
                          verify_ssl=DEFAULT_SSL_VERIFY):
    """This method performs an API call (POST, PUT, or PATCH) that includes a JSON-formatted payload.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param method: The API method (``post``, ``put``, or ``patch``)
    :type method: str
    :param uri: The API endpoint to query
    :type uri: str
    :param payload: The payload to leverage in the API call
    :type payload: dict
    :param params: The query parameters (where applicable)
    :type params: dict, None
    :param headers: Specific API headers to use when performing the API call
    :type headers: dict, None
    :param timeout: The timeout period in seconds (defaults to ``30``)
    :type timeout: int, str, None
    :param show_full_error: Determines if the full error message should be displayed (``True`` by default)
    :type show_full_error: bool
    :param return_json: Determines if the response should be returned in JSON format (``True`` by default)
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: The API response in JSON format or as a ``requests`` response object
    :raises: :py:exc:`freshpy.errors.exceptions.DELETERequestError`,
             :py:exc:`freshpy.errors.exceptions.PATCHRequestError`,
             :py:exc:`freshpy.errors.exceptions.POSTRequestError`,
             :py:exc:`freshpy.errors.exceptions.PUTRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIConnectionError`
    """
    # Define the parameters as an empty dictionary if none are provided
    params = {} if params is None else params

    # Define headers if not supplied
    headers = define_headers() if not headers else headers

    # Construct the credentials dictionary
    credentials = define_auth(freshpy_object.api_key)

    # Construct the query URL
    query_url = freshpy_object.base_url + uri

    # Perform the API call
    retries, response = 0, None
    while retries <= 5:
        try:
            if method.lower() == 'post':
                response = requests.post(query_url, json=payload, headers=headers, auth=credentials, params=params,
                                         timeout=timeout, verify=verify_ssl)
            elif method.lower() == 'patch':
                response = requests.patch(query_url, json=payload, headers=headers, auth=credentials, params=params,
                                          timeout=timeout, verify=verify_ssl)
            elif method.lower() == 'put':
                response = requests.put(query_url, json=payload, headers=headers, auth=credentials, params=params,
                                        timeout=timeout, verify=verify_ssl)
            elif method.lower() == 'delete':
                response = requests.delete(query_url, json=payload, headers=headers, auth=credentials, params=params,
                                           timeout=timeout, verify=verify_ssl)
            break
        except Exception as exc_msg:
            _report_failed_attempt(exc_msg, method.lower(), retries)
            retries += 1
    if retries == 6:
        _raise_exception_for_repeated_timeouts()

    # Examine and return the response
    if response.status_code >= 300:
        error_msg = f'The {method.upper()} request failed with a {response.status_code} status code.'
        error_msg += f'\n{response.text}' if show_full_error else error_msg
        _raise_exception_for_api_method(method.lower(), error_msg)
    if return_json:
        try:
            response = response.json()
        except Exception as exc:
            exc_type = errors.handlers.get_exception_type(exc)
            logger.error(f'Failed to convert the API response to JSON format due to the following {exc_type} '
                         f'exception and the full Response object will be returned: {exc}')
    return response


def _report_failed_attempt(_exc_msg, _request_type, _retries, _log_exception=True):
    """This function reports a failed API call that will be retried.

    .. version-changed:: 3.0.0
       This function now leverages the logging functionality rather than printing the error to stderr.
       It also uses more specific exception classes based on the API request type.

    .. version-changed:: 2.0.0
       The generic py:exc:`Exception` exception was replaced with a py:exc:`RuntimeError` exception.

    .. version-added:: 1.0.0

    :param _exc_msg: The exception that was raised within a try/except clause
    :param _request_type: The type of API request (e.g. ``get``, ``post``, ``put``, etc.)
    :type _request_type: str
    :param _retries: The attempt number for the API request
    :type _retries: int
    :param _log_exception: Determines if a log entry should be created prior to raising the exception
                           (``True`` by default)
    :type _log_exception: bool
    :returns: None
    :raises: :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.DELETERequestError`,
             :py:exc:`freshpy.errors.exceptions.PATCHRequestError`,
             :py:exc:`freshpy.errors.exceptions.POSTRequestError`,
             :py:exc:`freshpy.errors.exceptions.PUTRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    _exc_name = type(_exc_msg).__name__
    if 'connect' not in _exc_name.lower():
        _raise_exception_for_api_method(_request_type, f'{_exc_name}: {_exc_msg}', _log_exception)
    _current_attempt = f"(Attempt {_retries} of 5)"
    _error_msg = f"The {_request_type.upper()} request has failed with the following exception: " + \
                 f"{_exc_name}: {_exc_msg} {_current_attempt}"
    # errors.handlers.eprint(f"{_error_msg}\n{_exc_name}: {_exc_msg}\n")
    logger.error(_error_msg)


def _raise_exception_for_api_method(_method=None, _exc_msg=None, _log_exception=True):
    """This function raises an exception with a specific exception class based on the API method.

    .. version-added:: 3.0.0

    :param _method: The API method associated with the exception (e.g. ``get``, ``post``, ``put``, etc.)
    :type _method: str, None
    :param _exc_msg: A custom exception message to use instead of the default message
    :type _exc_msg: str, None
    :param _log_exception: Determines if a log entry should be created prior to raising the exception
                           (``True`` by default)
    :type _log_exception: bool
    :returns: None
    :raises: :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.DELETERequestError`,
             :py:exc:`freshpy.errors.exceptions.PATCHRequestError`,
             :py:exc:`freshpy.errors.exceptions.POSTRequestError`,
             :py:exc:`freshpy.errors.exceptions.PUTRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    if _exc_msg and _log_exception:
        logger.critical(_exc_msg)
    if _method.lower() == 'get':
        raise errors.exceptions.GETRequestError(_exc_msg)
    elif _method.lower() == 'delete':
        raise errors.exceptions.DELETERequestError(_exc_msg)
    elif _method.lower() == 'patch':
        raise errors.exceptions.PATCHRequestError(_exc_msg)
    elif _method.lower() == 'post':
        raise errors.exceptions.POSTRequestError(_exc_msg)
    elif _method.lower() == 'put':
        raise errors.exceptions.PUTRequestError(_exc_msg)
    else:
        raise errors.exceptions.APIRequestError(_exc_msg)


def _raise_exception_for_repeated_timeouts():
    """This function raises an exception when all API attempts (including) retries resulted in a timeout.

    .. version-changed:: 3.0.0
       A log entry is now created prior to raising the exception.

    .. version-added:: 1.0.0

    :returns: None
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`
    """
    _failure_msg = "The script was unable to complete successfully after five consecutive API timeouts. " + \
                   "Please run the script again or contact Freshservice Support for further assistance."
    logger.critical(_failure_msg)
    raise errors.exceptions.APIConnectionError(_failure_msg)
