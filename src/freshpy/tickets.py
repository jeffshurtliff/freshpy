# -*- coding: utf-8 -*-
"""
:Module:            freshpy.tickets
:Synopsis:          Functions for interacting with Freshservice tickets
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     01 Jan 2022
"""

from . import api, errors
from .utils import core_utils, log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)

# Define constants
VALID_PREDEFINED_FILTERS = ['new_and_my_open', 'watching', 'spam', 'deleted']
SUPPORTED_FILTER_FIELDS = ['agent_id', 'group_id', 'priority', 'status', 'impact', 'urgency', 'tag', 'due_by',
                           'fr_due_by', 'created_at']
FILTER_LOGIC_OPERATORS = ['AND', 'OR']


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
    uri += _parse_constraints(_include=include)
    return api.get_request_with_retries(freshpy_object, uri)


def get_tickets(freshpy_object, include=None, predefined_filter=None, filters=None, filter_logic='AND',
                requester_id=None, requester_email=None, ticket_type=None, updated_since=None, ascending=None,
                descending=None, per_page=None, page=None):
    """This function returns a sequence of tickets with optional filters.

    .. versionadded:: 1.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param include: A string or iterable of `embedding <https://api.freshservice.com/#view_a_ticket>`_ options
    :type include: str, tuple, list, set, None
    :param predefined_filter: One of the predefined filters ('new_and_my_open', 'watching', 'spam', 'deleted')
    :type predefined_filter: str, None
    :param filters: Query filter(s) in the form of a structured query string or a dictionary of values
    :type filters: str, dict, None
    :param filter_logic: Defines the logic to use as necessary in a filter query string (default is ``AND``)
    :param requester_id: The numeric ID of a requester
    :type requester_id: str, int, None
    :param requester_email: The email address of a requester
    :type requester_email: str, None
    :param ticket_type: The type of ticket (e.g. ``Incident``, ``Service Request``, etc.)
    :type ticket_type: str, None
    :param updated_since: A date or timestamp (in UTC format) to be a threshold for when the ticket was last updated
    :type updated_since: str, None
    :param ascending: Determines if the tickets should be sorted in *ascending* order
    :type ascending: bool, None
    :param descending: Determines if the tickets should be sorted in *descending* order (default)
    :type descending: bool, None
    :param per_page: Displays a certain number of results per query
    :type per_page: str, int, None
    :param page: Returns a specific page number (used for paginated results)
    :type page: str, int, None
    :returns: A list of JSON objects for tickets
    :raises: :py:exc:`freshpy.errors.exceptions.InvalidPredefinedFilterError`,
             :py:exc:`freshpy.errors.exceptions.APIConnectionError`
    """
    uri = 'tickets'
    if filters:
        uri += _parse_filters(filters, filter_logic)
    else:
        uri += _parse_constraints(_include=include, _predefined_filter=predefined_filter, _requester_id=requester_id,
                                  _requester_email=requester_email, _ticket_type=ticket_type,
                                  _updated_since=updated_since, _ascending=ascending, _descending=descending,
                                  _per_page=per_page, _page=page)
    return api.get_request_with_retries(freshpy_object, uri)


def _parse_filters(_filters=None, _logic='AND'):
    _filters = {} if not _filters else _filters
    if _logic.upper() not in FILTER_LOGIC_OPERATORS:
        raise errors.exceptions.InvalidFilterLogicError(value=_logic)
    if isinstance(_filters, str):
        _filters = core_utils.url_encode(_filters)
        _uri_segment = f'/filter?query="{_filters}"'
    else:
        _uri_segment = f'/filter?query='
        _filter = ''
        for _idx, (_field, _value) in enumerate(_filters.items()):
            _filter += f'{_field}:{_value}'
            if _idx < (len(_filters) - 1):
                _filter += f' {_logic.upper()} '
        _filter = core_utils.url_encode(_filter)
        _uri_segment += f'"{_filter}"'
    return _uri_segment


def _parse_constraints(_include=None, _predefined_filter=None, _requester_id=None, _requester_email=None,
                       _ticket_type=None, _updated_since=None, _ascending=None, _descending=None, _per_page=None,
                       _page=None):
    """This function parses any constraints into a properly constructed query string.

    .. versionadded:: 1.0.0

    :param _include: A string or iterable of `embedding <https://api.freshservice.com/#view_a_ticket>`_ options
    :type _include: str, tuple, list, set, None
    :param _predefined_filter: One of the predefined filters ('new_and_my_open', 'watching', 'spam', 'deleted')
    :type _predefined_filter: str, None
    :param _requester_id: The numeric ID of a requester
    :type _requester_id: str, int, None
    :param _requester_email: The email address of a requester
    :type _requester_email: str, None
    :param _ticket_type: The type of ticket (e.g. ``Incident``, ``Service Request``, etc.)
    :type _ticket_type: str, None
    :param _updated_since: A date or timestamp (in UTC format) to be a threshold for when the ticket was last updated
    :type _updated_since: str, None
    :param _ascending: Determines if the tickets should be sorted in *ascending* order
    :type _ascending: bool, None
    :param _descending: Determines if the tickets should be sorted in *descending* order (default)
    :type _descending: bool, None
    :param _per_page: Displays a certain number of results per query
    :type _per_page: str, int, None
    :param _page: Returns a specific page number (used for paginated results)
    :type _page: str, int, None
    :returns: The fully constructed query string
    :raises: :py:exc:`freshpy.errors.exceptions.InvalidPredefinedFilterError`
    """
    _constraints = ''
    if _include:
        # TODO: Perform a check to verify support for the provided include value(s)
        if not isinstance(_include, str):
            _include = ','.join(_include)
        _constraints = core_utils.construct_query_string(_constraints, f'include={_include}')
    if _predefined_filter:
        if _predefined_filter not in VALID_PREDEFINED_FILTERS:
            if isinstance(_predefined_filter, str):
                raise errors.exceptions.InvalidPredefinedFilterError(value=_predefined_filter)
            raise errors.exceptions.InvalidPredefinedFilterError()
        _constraints = core_utils.construct_query_string(_constraints, f'filter={_predefined_filter}')
    if _requester_id:
        _constraints = core_utils.construct_query_string(_constraints, f'requester_id={_requester_id}')
    if _requester_email:
        _requester_email = core_utils.url_encode(_requester_email)
        _constraints = core_utils.construct_query_string(_constraints, f'requester_email={_requester_email}')
    if _ticket_type:
        _ticket_type = _ticket_type.replace(' ', '+')
        _constraints = core_utils.construct_query_string(_constraints, f'type={_ticket_type}')
    if _updated_since:
        _constraints = core_utils.construct_query_string(_constraints, f'updated_since={_updated_since}')
    if _ascending:
        _constraints = core_utils.construct_query_string(_constraints, 'order_type=asc')
    if _descending:
        _constraints = core_utils.construct_query_string(_constraints, 'order_type=desc')
    if _per_page:
        _constraints = core_utils.construct_query_string(_constraints, f'per_page={_per_page}')
    if _page:
        _constraints = core_utils.construct_query_string(_constraints, f'page={_page}')
    return _constraints

