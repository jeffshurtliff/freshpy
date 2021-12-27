# -*- coding: utf-8 -*-
"""
:Module:            freshpy.core
:Synopsis:          Defines the core freshpy object used to interface with the Freshservice API
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     27 Dec 2021
"""

from .utils import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)
