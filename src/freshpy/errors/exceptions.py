# -*- coding: utf-8 -*-
"""
:Module:            freshpy.errors.exceptions
:Synopsis:          Collection of exception classes relating to the freshpy library
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     28 Dec 2021
"""

#################
# Base Exception
#################


# Define base exception class
class FreshPyError(Exception):
    """This is the base class for FreshPy exceptions.

    .. versionadded:: 1.0.0
    """
    pass


############################
# Authentication Exceptions
############################


class MissingAuthDataError(FreshPyError):
    """This exception is used when authentication data is not supplied and therefore a connection cannot occur.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The authentication data was not provided and a connection cannot be established."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


#####################
# General Exceptions
#####################


class CurrentlyUnsupportedError(FreshPyError):
    """This exception is used when a feature or functionality being used is currently unsupported.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "This feature is currently unsupported at this time."
        if not (args or kwargs):
            args = (default_msg,)
        else:
            custom_msg = f"The '{args[0]}' {default_msg.split('This ')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class DataMismatchError(FreshPyError):
    """This exception is used when there is a mismatch between two data sources.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "A data mismatch was found with the data sources."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'data' in kwargs:
            multi_types = [list, tuple, set]
            if type(kwargs['data']) == str:
                custom_msg = f"{default_msg.split('data')[0]}'{kwargs['val']}'{default_msg.split('with the')[1]}"
                custom_msg = custom_msg.replace('sources', 'source')
                args = (custom_msg,)
            elif type(kwargs['data']) in multi_types and len(kwargs['data']) == 2:
                custom_section = f"'{kwargs['data'][0]}' and '{kwargs['data'][1]}'"
                custom_msg = f"{default_msg.split('data sources')[0]}{custom_section}{default_msg.split('with the')[1]}"
                args = (custom_msg,)
        super().__init__(*args)


class InvalidFieldError(FreshPyError):
    """This exception is used when an invalid field is provided.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The field that was provided is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'val' in kwargs:
            custom_msg = f"{default_msg.split('field ')[0]}'{kwargs['val']}'{default_msg.split('The')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class InvalidURLError(FreshPyError):
    """This exception is used when a provided URL is invalid.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The provided URL is invalid"
        if not (args or kwargs):
            args = (default_msg,)
        elif 'url' in kwargs:
            custom_msg = f"{default_msg.split('is')[0]}'{kwargs['url']}'{default_msg.split('URL')[1]}"
            args = (custom_msg,)
        super().__init__(*args)


class MissingRequiredDataError(FreshPyError):
    """This exception is used when a function or method is missing one or more required arguments.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "Missing one or more required parameters"
        init_msg = "The object failed to initialize as it is missing one or more required arguments."
        param_msg = "The required parameter 'PARAMETER_NAME' is not defined"
        if not (args or kwargs):
            args = (default_msg,)
        elif 'init' in args or 'initialize' in args:
            if 'object' in kwargs:
                custom_msg = f"{init_msg.split('object')[0]}'{kwargs['object']}'{init_msg.split('The')[1]}"
                args = (custom_msg,)
            else:
                args = (init_msg,)
        elif 'param' in kwargs:
            args = (param_msg.replace('PARAMETER_NAME', kwargs['param']),)
        else:
            args = (default_msg,)
        super().__init__(*args)


#########################
# Generic API Exceptions
#########################


class APIConnectionError(FreshPyError):
    """This exception is used when the API query could not be completed due to connection aborts and/or timeouts.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API query could not be completed due to connection aborts and/or timeouts."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class APIRequestError(FreshPyError):
    """This exception is used for generic API request errors when there isn't a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class DELETERequestError(FreshPyError):
    """This exception is used for generic DELETE request errors when there isn't a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The DELETE request did not return a successful response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)
        
        
class FeatureNotConfiguredError(FreshPyError):
    """This exception is used when an API request fails because a feature is not configured.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        exc_msg = "The feature is not configured."
        if 'identifier' in kwargs or 'feature' in kwargs:
            if 'identifier' in kwargs:
                exc_msg += f" Identifier: {kwargs['identifier']}"
            if 'feature' in kwargs:
                exc_msg = exc_msg.replace("feature", f"{kwargs['feature']} feature")
            args = (exc_msg,)
        elif not (args or kwargs):
            args = (exc_msg,)
        super().__init__(*args)


class GETRequestError(FreshPyError):
    """This exception is used for generic GET request errors when there is not a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The GET request did not return a successful response."
        custom_msg = "The GET request failed with the following message:"
        if 'status_code' in kwargs or 'message' in kwargs:
            if 'status_code' in kwargs:
                status_code_msg = f"returned the {kwargs['status_code']} status code"
                custom_msg = custom_msg.replace('failed', status_code_msg)
            if 'message' in kwargs:
                custom_msg = f"{custom_msg} {kwargs['message']}"
            else:
                custom_msg = custom_msg.split(' with the following')[0] + "."
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)
        
        
class InvalidPayloadValueError(FreshPyError):
    """This exception is used when an invalid value is provided for a payload field.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "An invalid payload value was provided."
        custom_msg = "The invalid payload value 'X' was provided for the 'Y' field."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'value' in kwargs:
            if 'field' in kwargs:
                custom_msg = custom_msg.replace('X', kwargs['value']).replace('Y', kwargs['field'])
            else:
                custom_msg = f"{custom_msg.replace('X', kwargs['value']).split(' for the')[0]}."
            args = (custom_msg,)
        super().__init__(*args)


class InvalidRequestTypeError(FreshPyError):
    """This exception is used when an invalid API request type is provided.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied request type for the API is not recognized. (Examples of valid " + \
                      "request types include 'POST' and 'PUT')"
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class LookupMismatchError(FreshPyError):
    """This exception is used when an a lookup value does not match the supplied lookup type.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The supplied lookup type for the API does not match the value that was provided."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class NotFoundResponseError(FreshPyError):
    """This exception is used when an API query returns a 404 response and there isn't a more specific class.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The API query returned a 404 response."
        if not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class POSTRequestError(FreshPyError):
    """This exception is used for generic POST request errors when there isn't a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The POST request did not return a successful response."
        custom_msg = "The POST request failed with the following message:"
        if 'status_code' in kwargs or 'message' in kwargs:
            if 'status_code' in kwargs:
                status_code_msg = f"returned the {kwargs['status_code']} status code"
                custom_msg = custom_msg.replace('failed', status_code_msg)
            if 'message' in kwargs:
                custom_msg = f"{custom_msg} {kwargs['message']}"
            else:
                custom_msg = custom_msg.split(' with the following')[0] + "."
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


class PUTRequestError(FreshPyError):
    """This exception is used for generic PUT request errors when there isn't a more specific exception.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "The PUT request did not return a successful response."
        custom_msg = "The PUT request failed with the following message:"
        if 'status_code' in kwargs or 'message' in kwargs:
            if 'status_code' in kwargs:
                status_code_msg = f"returned the {kwargs['status_code']} status code"
                custom_msg = custom_msg.replace('failed', status_code_msg)
            if 'message' in kwargs:
                custom_msg = f"{custom_msg} {kwargs['message']}"
            else:
                custom_msg = custom_msg.split(' with the following')[0] + "."
            args = (custom_msg,)
        elif not (args or kwargs):
            args = (default_msg,)
        super().__init__(*args)


####################
# Ticket Exceptions
####################


class InvalidFilterLogicError(FreshPyError):
    """This exception is used when an invalid filter logic operator is supplied.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "An invalid filter logic operator was provided."
        custom_msg = "The filter logic operator 'X' is invalid."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'value' in kwargs:
            custom_msg = custom_msg.replace('X', kwargs['value'])
            args = (custom_msg,)
        super().__init__(*args)


class InvalidPredefinedFilterError(FreshPyError):
    """This exception is used when the API query could not be completed due to connection aborts and/or timeouts.

    .. versionadded:: 1.0.0
    """
    def __init__(self, *args, **kwargs):
        """This method defines the default or custom message for the exception."""
        default_msg = "An invalid predefined filter was provided."
        custom_msg = "The provided filter 'X' is not a valid predefined filter."
        if not (args or kwargs):
            args = (default_msg,)
        elif 'value' in kwargs:
            custom_msg = custom_msg.replace('X', kwargs['value'])
            args = (custom_msg,)
        super().__init__(*args)
