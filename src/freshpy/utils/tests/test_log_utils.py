# -*- coding: utf-8 -*-
# bandit: skip=B101
"""
:Module:         freshpy.utils.tests.test_log_utils
:Synopsis:       This module is used by pytest to test the logging functionality
:Created By:     Jeff Shurtliff
:Last Modified:  Jeff Shurtliff
:Modified Date:  31 Dec 2025
"""

import logging
import sys

import pytest

from freshpy.utils import log_utils


def _cleanup_logger(logger: logging.Logger) -> None:
    """This function removes and closes handlers for a logger.

    .. version-added:: 1.4.0

    :param logger: The logger instance to clean up
    :type logger: class[logging.Logger]
    :returns: None
    """
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()


def test_initialize_logging_defaults_to_info_level() -> None:
    """This function verifies that initialize_logging() defaults logger level to INFO.

    .. version-added:: 1.4.0

    :returns: None
    """
    logger_name = "freshpy.test.default.info"
    logger = log_utils.initialize_logging(logger_name)
    try:
        assert logger.level == logging.INFO
    finally:
        _cleanup_logger(logger)


def test_initialize_logging_applies_default_level_to_console_handler(caplog: pytest.LogCaptureFixture) -> None:
    """This function ensures console handlers inherit the default INFO level.

    .. version-added:: 1.4.0

    :param caplog: Pytest fixture capturing log records for assertions
    :type caplog: class[pytest.LogCaptureFixture]
    :returns: None
    """
    logger_name = "freshpy.test.console.default"
    logger = log_utils.initialize_logging(logger_name, console_output=True)
    message = "default info message"
    try:
        with caplog.at_level(logging.INFO, logger=logger_name):
            logger.info(message)

        stdout_handlers = [
            handler
            for handler in logger.handlers
            if isinstance(handler, logging.StreamHandler)
            and getattr(handler, "stream", None) is sys.stdout
        ]
        assert stdout_handlers
        for handler in stdout_handlers:
            assert handler.level == logging.INFO

        assert any(
            record.levelno == logging.INFO and record.message == message
            for record in caplog.records
        )
    finally:
        _cleanup_logger(logger)
