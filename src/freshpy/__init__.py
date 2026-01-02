# -*- coding: utf-8 -*-
"""
:Package:           freshpy
:Synopsis:          This is the ``__init__`` module for the freshpy package
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Jan 2026
"""

from .core import FreshPy
from .models.enums import TicketSourceType, TicketStatus, TicketPriority
from .utils import version

__all__ = ['core', 'FreshPy', 'api', 'agents', 'tickets', 'TicketSourceType', 'TicketStatus', 'TicketPriority']

# Define the package version by pulling from the freshpy.utils.version module
__version__ = version.get_full_version()
