# -*- coding: utf-8 -*-
"""
:Module:            freshpy.utils.core_utils
:Synopsis:          Collection of supporting utilities and functions to complement the primary modules
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Jan 2026
"""

import urllib.parse

from . import log_utils
from .. import errors

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def construct_query_string(existing_query=None, appendage=None):
    """This function assists in constructing query strings for URIs to ensure they follow the appropriate format.

    .. version-added:: 1.0.0

    :param existing_query: The existing query string (if any)
    :type existing_query: str, None
    :param appendage: The new addition to the query string to be appended (if any)
    :type appendage: str, None
    :returns: The constructed query string
    """
    combined_query = '' if existing_query is None else existing_query
    if appendage:
        if existing_query == '?':
            combined_query = f'?{appendage}'
        elif existing_query:
            combined_query = existing_query + f'&{appendage}'
        elif appendage.startswith('?'):
            combined_query = appendage
        else:
            combined_query = f'?{appendage}'
    return combined_query


def url_encode(raw_string):
    """This function encodes a string for use in URLs.

    .. version-added:: 1.0.0

    :param raw_string: The raw string to be encoded
    :type raw_string: str
    :returns: The encoded string
    """
    return urllib.parse.quote_plus(raw_string)


def url_decode(encoded_string):
    """This function decodes a url-encoded string.

    .. version-added:: 1.0.0

    :param encoded_string: The url-encoded string
    :type encoded_string: str
    :returns: The unencoded string
    """
    return urllib.parse.unquote_plus(encoded_string)


def validate_numeric_value(value, param_name=None):
    """This function checks a parameter value to ensure that it is an integer or a numeric string.

    .. version-added:: 3.0.0

    :param value: The parameter value to be validated
    :param param_name: The name of the parameter being validated (optional)
    :type param_name: str, None
    :returns: None
    :raises: :py:exc:`freshpy.errors.exceptions.InvalidDataTypeError`
    """
    # Specify the parameter name in the exception message when provided
    param_str_segment = f"'{param_name}' value" if param_name else 'value'

    # Define an exception message when necessary
    if not any((isinstance(value, str), isinstance(value, int))):
        data_type = type(value).__name__
        exc_msg = f"The {param_str_segment} has a(n) '{data_type}' type but must be an integer or numeric string"
    elif isinstance(value, str) and not value.isdigit():
        exc_msg = f'The {param_str_segment} must be a whole number (integer) if provided as a string'
    else:
        exc_msg = None

    # Log the error and raise an exception if an exception message has been defined
    if exc_msg:
        logger.error(exc_msg)
        raise errors.exceptions.InvalidDataTypeError(exc_msg)
