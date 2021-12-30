# -*- coding: utf-8 -*-
"""
:Package:           freshpy
:Synopsis:          This is the ``__init__`` module for the freshpy package
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     30 Dec 2021
"""

from .core import FreshPy
from .utils import version

__all__ = ['core', 'FreshPy', 'api', 'tickets']

# Define the package version by pulling from the freshpy.utils.version module
__version__ = version.get_full_version()

