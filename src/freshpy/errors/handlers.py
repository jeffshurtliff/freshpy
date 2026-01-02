# -*- coding: utf-8 -*-
"""
:Module:            freshpy.errors.handlers
:Synopsis:          Functions that handle various error situations within the namespace
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Jan 2026
"""

import sys


def eprint(*args, **kwargs):
    """This function behaves the same as the ``print()`` function but is leveraged to print errors to ``sys.stderr``."""
    print(*args, file=sys.stderr, **kwargs)


def get_exception_type(exc):
    """This function returns the exception type (e.g. ``RuntimeError``, ``TypeError``, etc.) for a given exception.

    .. version-added:: 3.0.0

    :returns: The exception type as a string
    """
    return type(exc).__name__
