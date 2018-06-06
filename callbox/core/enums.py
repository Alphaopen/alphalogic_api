# -*- coding: utf-8 -*-

from enum import Enum

class VisibleType(Enum):
    RUNTIME = 0
    SETUP = 1
    HIDDEN = 2
    COMMON = 3


class ValueType(Enum):
    STRING = 0
    INT64 = 1
    DOUBLE = 2
    DATETIME = 3
    BOOL = 4
    BYTES = 5
    MAP = 6


class AccessType(Enum):
    READ_ONLY = 0
    READ_WRITE = 1


class UserType(Enum):
    LICENSED = 0


class EventPriority(Enum):
    TRIVIAL = 0
    MINOR = 1
    MAJOR = 2
    CRITICAL = 3
    BLOCKER = 4