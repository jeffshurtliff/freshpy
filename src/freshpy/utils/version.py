# -*- coding: utf-8 -*-
"""
:Module:            freshpy.utils.version
:Synopsis:          This simple script contains the package version
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Jan 2022
"""

from . import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)

# Define special and global variables
__version__ = "1.0.0.post1"


def get_full_version():
    """This function returns the current full version of the freshpy package.

    .. versionadded:: 1.0.0
    """
    return __version__
