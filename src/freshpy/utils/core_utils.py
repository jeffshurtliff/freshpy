# -*- coding: utf-8 -*-
"""
:Module:            freshpy.utils.core_utils
:Synopsis:          Collection of supporting utilities and functions to complement the primary modules
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     30 Dec 2021
"""

import urllib.parse


def construct_query_string(existing_query=None, appendage=None):
    """This function assists in constructing query strings for URIs to ensure they follow the appropriate format.

    .. versionadded:: 1.0.0

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

    .. versionadded:: 1.0.0

    :param raw_string: The raw string to be encoded
    :type raw_string: str
    :returns: The encoded string
    """
    return urllib.parse.quote_plus(raw_string)


def url_decode(encoded_string):
    """This function decodes a url-encoded string.

    .. versionadded:: 1.0.0

    :param encoded_string: The url-encoded string
    :type encoded_string: str
    :returns: The unencoded string
    """
    return urllib.parse.unquote_plus(encoded_string)