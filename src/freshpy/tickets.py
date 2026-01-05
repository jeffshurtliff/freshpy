# -*- coding: utf-8 -*-
"""
:Module:            freshpy.tickets
:Synopsis:          Functions for interacting with Freshservice tickets
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     05 Jan 2026
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


def get_ticket(freshpy_object, ticket_number, include=None, verify_ssl=True):
    """This function returns the data for a specific ticket.

    .. version-changed:: 3.0.0
       The ticket number is now validated before being used in the API call.

    .. version-changed:: 1.1.0
       Added the ability to disable SSL verification on API calls.

    .. version-added:: 1.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param ticket_number: The ticket number for which to return data
    :type ticket_number: str, int
    :param include: A string or iterable of `embedding <https://api.freshservice.com/#view_a_ticket>`_ options
    :type include: str, tuple, list, set, None
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: JSON data for the given ticket
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    core_utils.validate_numeric_value(ticket_number, 'ticket_number')
    uri = f'tickets/{ticket_number}'
    uri += _parse_constraints(_include=include)
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)


def get_tickets(freshpy_object, include=None, predefined_filter=None, filters=None, filter_logic='AND',
                requester_id=None, requester_email=None, ticket_type=None, updated_since=None, ascending=None,
                descending=None, per_page=None, page=None, verify_ssl=True):
    """This function returns a sequence of tickets with optional filters.

    .. version-changed:: 1.1.0
       Added the ability to disable SSL verification on API calls.

    .. version-added:: 1.0.0

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
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: A list of JSON objects for tickets
    :raises: :py:exc:`freshpy.errors.exceptions.InvalidPredefinedFilterError`,
             :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    uri = 'tickets'
    if filters:
        uri += _parse_filters(filters, filter_logic)
    else:
        uri += _parse_constraints(_include=include, _predefined_filter=predefined_filter, _requester_id=requester_id,
                                  _requester_email=requester_email, _ticket_type=ticket_type,
                                  _updated_since=updated_since, _ascending=ascending, _descending=descending,
                                  _per_page=per_page, _page=page)
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)


def get_ticket_fields(freshpy_object, workspace_id=None, verify_ssl=True):
    """This function retrieves the standard and custom fields that exist for tickets.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param workspace_id: The ID of a specific workspace (defaults to primary workspace if not specified)
    :type workspace_id: str, int, None
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: Dictionary (JSON) with the ticket field data
    :raises: :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    uri = 'ticket_form_fields'
    if workspace_id:
        core_utils.validate_numeric_value(workspace_id, 'workspace_id')
        uri += f'?workspace_id={workspace_id}'
    return api.get_request_with_retries(freshpy_object, uri=uri, verify_ssl=verify_ssl)


def get_ticket_field(freshpy_object, field_id=None, field_label=None, field_name=None, match_case=True,
                     ticket_data=None, workspace_id=None, verify_ssl=True):
    """This function retrieves a specific ticket field based on a provided ID, Label, and/or Name.

    .. version-added:: 3.0.0

    :param freshpy_object: The core :py:class:`freshpy.FreshPy` object
    :type freshpy_object: class[freshpy.FreshPy]
    :param field_id: The ``id`` value for the field
    :type field_id: int, str, None
    :param field_label: The ``label`` value for the field
    :type field_label: str, None
    :param field_name: The ``name`` value for the field
    :type field_name: str, None
    :param match_case: Determines if the ``label`` value should be case-sensitive (``True`` by default)
    :type match_case: bool
    :param ticket_data: Dictionary or list containing all ticket field data (optional)
    :type ticket_data: dict, list, None
    :param workspace_id: The ID of a specific workspace (defaults to primary workspace if not specified)
    :type workspace_id: str, int, None
    :param verify_ssl: Determines if SSL verification should occur (``True`` by default)
    :type verify_ssl: bool
    :returns: A JSON-formatted dictionary with the field data (or an empty dictionary if the field is not found)
    :raises: :py:exc:`freshpy.errors.exceptions.InvalidPredefinedFilterError`,
             :py:exc:`freshpy.errors.exceptions.APIConnectionError`,
             :py:exc:`freshpy.errors.exceptions.GETRequestError`,
             :py:exc:`freshpy.errors.exceptions.APIRequestError`
    """
    # Retrieve all ticket fields as there is not an endpoint to retrieve just a single field
    all_fields = None
    if ticket_data:
        if (isinstance(ticket_data, dict) and 'ticket_fields' in ticket_data) or isinstance(ticket_data, list):
            all_fields = ticket_data
        else:
            logger.error('The provided ticket_data is not in a valid format and will be ignored')
    if not all_fields:
        all_fields = get_ticket_fields(freshpy_object, workspace_id=workspace_id, verify_ssl=verify_ssl)
    all_fields = all_fields['ticket_fields'] if not isinstance(all_fields, list) else all_fields

    # Raise an exception if no lookup value was provided
    if not any((field_id, field_label, field_name)):
        error_msg = 'You must provide a lookup value (field_id, field_label, or field_name) to retrieve a ticket field'
        logger.error(error_msg)
        raise errors.exceptions.MissingRequiredDataError(error_msg)

    # Determine which lookup values are defined
    defined_lookup_values = {}
    if field_id:
        core_utils.validate_numeric_value(field_id, 'field_id')
        defined_lookup_values['id'] = int(field_id)
    if field_label:
        defined_lookup_values['label'] = field_label
    if field_name:
        defined_lookup_values['name'] = field_name

    # Find the requested field based on the lookup value provided
    requested_field = {}
    for field in all_fields:
        for lookup_key, lookup_value in defined_lookup_values.items():
            if lookup_key == 'label' and lookup_key in field and not match_case:
                if field[lookup_key].lower() == lookup_value.lower():
                    requested_field = field
                    break
            elif lookup_key in field and field[lookup_key] == lookup_value:
                requested_field = field
                break
        if requested_field:
            break

    # Return the located field data (or an empty dict if not found)
    if not requested_field:
        logger.error('Failed to find the requested ticket field based on the lookup criteria provided')
    return requested_field


def create_ticket(freshpy_object, subject=None, description=None, requester_email=None, priority=None, status=None,
                  cc_emails=None, custom_fields=None, workspace_id=None, ticket_details=None, verify_ssl=True):
    # TODO: Add docstring

    # Leverage the provided ticket details when applicable
    ticket_details = {} if not ticket_details else ticket_details
    # TODO: Allow a typed dict to optionally be provided instead of a raw dict
    if ticket_details and not isinstance(ticket_details, dict):
        logger.error('The provided ticket_details are not in a valid format and will be ignored')
        ticket_details = {}

    # TODO: Add validation (optionally?) that required fields are defined before making API call

    # Evaluate the subject and add to payload when defined
    if subject:
        core_utils.validate_data_type(subject, str, 'subject')
        ticket_details['subject'] = subject

    # Evaluate the description and add to payload when defined
    if description:
        core_utils.validate_data_type(description, str, 'description')
        ticket_details['description'] = description

    # Evaluate the requester email and add to payload when defined
    if requester_email:
        core_utils.validate_data_type(requester_email, str, 'requester_email')
        ticket_details['email'] = requester_email

    # Evaluate the priority and add to payload when defined
    if priority:
        # TODO: Add functionality to provide more than just an integer
        core_utils.validate_data_type(priority, int, 'priority')
        ticket_details['priority'] = priority

    # Evaluate the status and add to payload when defined
    if status:
        # TODO: Add functionality to provide more than just an integer
        core_utils.validate_data_type(status, int, 'status')
        ticket_details['status'] = status

    # Evaluate the CC emails and add to payload when defined
    if cc_emails:
        # Ensure the data type is correct
        if isinstance(cc_emails, str):
            cc_emails = [cc_emails]
            ticket_details['cc_emails'] = cc_emails
        elif core_utils.is_iterable(cc_emails) and core_utils.is_data_type(cc_emails, (tuple, set)):
            cc_emails = list(cc_emails)
            ticket_details['cc_emails'] = cc_emails
        elif isinstance(cc_emails, list):
            ticket_details['cc_emails'] = cc_emails
        else:
            error_msg = "The 'cc_emails' parameter is not an appropriate data type and will be ignored"
            logger.error(error_msg)

    # Add custom fields to the payload if defined and in correct format
    if custom_fields:
        core_utils.validate_data_type(custom_fields, dict, 'custom_fields')
        ticket_details['custom_fields'] = custom_fields

    # Add the workspace ID if present and in correct format
    if workspace_id:
        core_utils.validate_data_type(workspace_id, (int, str), 'workspace_id')
        if isinstance(workspace_id, str):
            core_utils.validate_numeric_value(workspace_id, 'workspace_id')
            workspace_id = int(workspace_id)
        ticket_details['workspace_id'] = workspace_id

    # Perform the API call to create the ticket
    return api.api_call_with_payload(freshpy_object, 'post', 'tickets', payload=ticket_details, verify_ssl=verify_ssl)


def _parse_filters(_filters=None, _logic='AND'):
    """This function parses any filters to be used in an API call."""
    _filters = {} if not _filters else _filters
    if _logic.upper() not in FILTER_LOGIC_OPERATORS:
        raise errors.exceptions.InvalidFilterLogicError(value=_logic)
    if isinstance(_filters, str):
        _filters = core_utils.url_encode(_filters)
        _uri_segment = f'/filter?query="{_filters}"'
    else:
        _uri_segment = '/filter?query='
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

    .. version-added:: 1.0.0

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
