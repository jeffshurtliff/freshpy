# -*- coding: utf-8 -*-
"""
:Module:            freshpy.models.enums
:Synopsis:          This module defines strongly-typed, immutable enumerations for ticket-related constants
:Created By:        Jeff Shurtliff
:Last Modified:     Jeff Shurtliff
:Modified Date:     02 Jan 2026
"""

from __future__ import annotations

from enum import IntEnum


class TicketSourceType(IntEnum):
    """This class defines the standard ticket source types. (`Source <https://api.freshservice.com#create_ticket>`_)"""
    EMAIL = 1
    PORTAL = 2
    PHONE = 3
    CHAT = 4
    FEEDBACK_WIDGET = 5
    YAMMER = 6
    AWS_CLOUDWATCH = 7
    PAGERDUTY = 8
    WALKUP = 9
    SLACK = 10


class TicketStatus(IntEnum):
    """This class defines the standard ticket status levels. (`Source <https://api.freshservice.com#create_ticket>`_)"""
    OPEN = 2
    PENDING = 3
    RESOLVED = 4
    CLOSED = 5


class TicketPriority(IntEnum):
    """This class defines the standard ticket priority levels. (`Source <https://api.freshservice.com#create_ticket>`_)"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
