# -*- coding: utf-8 -*-
"""
:Module:            freshpy.utils.version
:Synopsis:          This simple script retrieves and defines the package version
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     31 Dec 2025
"""

from importlib.metadata import version, PackageNotFoundError

from . import log_utils

# Initialize logging
logger = log_utils.initialize_logging(__name__)


def get_full_version() -> str:
    """This function returns the current full version of the ``freshpy`` package.

    .. version-changed:: 1.4.0
       The function now retrieves the version from the package metadata,
       rather than from the ``__version__`` special variable.

    Retrieves the package version from the installed package metadata, which is
    populated from the ``version`` field in ``pyproject.toml``.
    """
    try:
        return version('freshpy')
    except PackageNotFoundError:
        # This can happen if the package is not installed in the environment.
        # (e.g. running from a source checkout without an editable install)
        logger.warning("freshpy is not installed; falling back to '0.0.0' as version")
        return '0.0.0'


def get_major_minor_version() -> str:
    """Return the current major.minor (i.e., X.Y) version of the package.

    .. version-changed:: 1.4.0
       The function utilizes the :py:func:`freshpy.utils.version.get_full_version`
       function to get the package version rather than using ``__version__``.
    """
    full_version = get_full_version()
    parts = full_version.split(".")
    if len(parts) >= 2:
        return ".".join(parts[:2])
    return full_version


# Define __version__ for backward compatibility and to utilize as needed
__version__ = get_full_version()
