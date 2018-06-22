# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from enum import Enum
import datetime

class runtime(object):
    pass

class setup(object):
    pass

class hidden(object):
    pass

class common(object):
    pass

class read_only(object):
    pass

class read_write(object):
    pass

'''
class ValueType(object):
    bool = staticmethod(lambda: ["ValueType", "BOOL"])
    int64 = staticmethod(lambda:  ["ValueType", "INT64"])
    double = staticmethod(lambda: ["ValueType", "DOUBLE"])
    datetime = staticmethod(lambda: ["ValueType", "DATETIME"])
    string = staticmethod(lambda: ["ValueType", "STRING"])

    create_parameter = {'BOOL': 'create_bool_parameter',
                   'INT64': 'create_int_parameter',
                   'DOUBLE': 'create_double_parameter',
                   'DATETIME': 'create_datetime_parameter',
                   'STRING': 'create_string_parameter'}
    set_value_type = {'BOOL': (lambda val: {'bool_value': val}),
                'INT64': (lambda val: {'int64_value': val}),
                'DOUBLE': (lambda val: {'double_value': val}),
                'DATETIME': (lambda val: {'datetime_value': val}),
                'STRING': (lambda val: {'string_value': val})}


class VisibleType(object):
    runtime = staticmethod(lambda: ["VisibleType", "RUNTIME"])
    setup = staticmethod(lambda: ["VisibleType", "SETUP"])
    hidden = staticmethod(lambda: ["VisibleType", "HIDDEN"])
    commmon = staticmethod(lambda: ["VisibleType", "COMMON"])
    set_visible_type = {'RUNTIME': 'set_runtime',
                'SETUP': 'set_setup',
                'HIDDEN': 'set_hidden',
                'COMMON': 'set_common'}


class AccessType(object):
    read_only = staticmethod(lambda: ["AccessType", "READ_ONLY"])
    read_write = staticmethod(lambda: ["AccessType", "READ_WRITE"])
    set_access_type = {'READ_ONLY': 'set_read_only',
                'READ_WRITE': 'set_read_write'}

'''
