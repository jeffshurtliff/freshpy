# -*- coding: utf-8 -*-
"""
:Module:            freshpy.tickets
:Synopsis:          Functions for interacting with Freshservice tickets
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     30 Dec 2021
"""

from . import api
from .utils import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def get_ticket(freshpy_object, ticket_number, include=None):
    """This function returns the data for a specific ticket.

    .. versionadded:: 1.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param ticket_number: The ticket number for which to return data
    :type ticket_number: str, int
    :param include: A string or iterable of `embedding <https://api.freshservice.com/#view_a_ticket>`_ options
    :type include: str, tuple, list, set, None
    :returns: JSON data for the given ticket
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`
    """
    uri = f'tickets/{ticket_number}'
    if include:
        if isinstance(include, str):
            uri += f'?include={include}'
    return api.get_request_with_retries(freshpy_object, uri)
