# -*- coding: utf-8 -*-

class ValueType(object):
    BOOL = staticmethod(lambda: ["ValueType", "BOOL"])
    INT64 = staticmethod(lambda :  ["ValueType", "INT64"])
    DOUBLE = staticmethod(lambda  : ["ValueType", "DOUBLE"])
    DATETIME = staticmethod(lambda  : ["ValueType", "DATETIME"])
    STRING = staticmethod(lambda: ["ValueType", "STRING"])
    create_dict = {'BOOL': 'create_bool_parameter',
                   'INT64': 'create_int_parameter',
                   'DOUBLE': 'create_double_parameter',
                   'DATETIME': 'create_datetime_parameter',
                   'STRING': 'create_string_parameter'}
    val_dict = {'BOOL': (lambda val : {'bool_value': val}),
                'INT64': (lambda val : {'int64_value': val}),
                'DOUBLE': (lambda val : {'double_value': val}),
                'DATETIME': (lambda val : {'datetime_value': val}),
                'STRING': (lambda val : {'string_value': val})}
    #BYTES = staticmethod(lambda  : ["ValueType", "BYTES"])
    #MAP = staticmethod(lambda  : ["ValueType", "MAP"])

class VisibleType(object):
    RUNTIME = staticmethod(lambda  : ["VisibleType", "RUNTIME"])
    SETUP = staticmethod(lambda  : ["VisibleType", "SETUP"])
    HIDDEN = staticmethod(lambda  : ["VisibleType", "HIDDEN"])
    COMMON =  staticmethod(lambda  : ["VisibleType", "COMMON"])
    set_dict = {'RUNTIME': 'set_runtime',
                'SETUP': 'set_setup',
                'HIDDEN': 'set_hidden',
                'COMMON': 'set_common'}

class AccessType(object):
    READ_ONLY = staticmethod(lambda  : ["AccessType", "READ_ONLY"])
    READ_WRITE = staticmethod(lambda  : ["AccessType", "READ_WRITE"])
    set_dict = {'READ_ONLY': 'set_read_only',
                'READ_WRITE': 'set_read_write'}

