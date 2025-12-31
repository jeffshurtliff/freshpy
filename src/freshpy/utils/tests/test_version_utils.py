# -*- coding: utf-8 -*-
# bandit: skip=B101
"""
:Module:         freshpy.utils.tests.test_version_utils
:Synopsis:       Test functions to verify the functionality in the ``version.py`` module
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  31 Dec 2025
"""

import importlib
import importlib.metadata as importlib_metadata

from freshpy.utils import version as version_utils


def test_get_full_version_returns_metadata(monkeypatch):
    """This function tests get_full_version returns the package metadata.

    .. version-added:: 1.4.0
    """
    expected_version = "1.2.3"
    monkeypatch.setattr(
        version_utils, "version", lambda package: expected_version
    )

    assert version_utils.get_full_version() == expected_version


def test_get_full_version_handles_missing_package(monkeypatch, caplog):
    """This function tests get_full_version fallback when package is missing.

    .. version-added:: 1.4.0
    """
    def raise_not_found(_package):
        raise version_utils.PackageNotFoundError("freshpy")

    monkeypatch.setattr(version_utils, "version", raise_not_found)

    with caplog.at_level("WARNING"):
        version_string = version_utils.get_full_version()

    assert version_string == "0.0.0"
    assert any("falling back to '0.0.0'" in message for message in caplog.messages)


def test_get_major_minor_version_returns_two_components(monkeypatch):
    """This function tests extracting the major.minor version components.

    .. version-added:: 1.4.0
    """
    monkeypatch.setattr(
        version_utils, "get_full_version", lambda: "2.3.4"
    )

    assert version_utils.get_major_minor_version() == "2.3"


def test_get_major_minor_version_returns_full_when_missing_minor(monkeypatch):
    """This function tests get_major_minor_version with a single-part version.

    .. version-added:: 1.4.0
    """
    monkeypatch.setattr(version_utils, "get_full_version", lambda: "7")

    assert version_utils.get_major_minor_version() == "7"


def test_dunder_version_matches_full_version(monkeypatch):
    """This function tests __version__ initialization uses get_full_version.

    .. version-added:: 1.4.0
    """
    real_version_function = importlib_metadata.version
    expected_version = "9.8.7"
    monkeypatch.setattr(
        importlib_metadata, "version", lambda package: expected_version
    )

    reloaded_module = importlib.reload(version_utils)
    assert reloaded_module.__version__ == expected_version
    assert reloaded_module.get_full_version() == expected_version

    importlib_metadata.version = real_version_function
    importlib.reload(version_utils)
