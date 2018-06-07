# -*- coding: utf-8 -*-

class ValueType(object):
    BOOL = staticmethod(lambda: ["ValueType", "BOOL"])
    INT64 = staticmethod(lambda :  ["ValueType", "INT64"])
    DOUBLE = staticmethod(lambda  : ["ValueType", "DOUBLE"])
    DATETIME = staticmethod(lambda  : ["ValueType", "DATETIME"])
    STRING = staticmethod(lambda: ["ValueType", "STRING"])
    #BYTES = staticmethod(lambda  : ["ValueType", "BYTES"])
    #MAP = staticmethod(lambda  : ["ValueType", "MAP"])

class VisibleType(object):
    RUNTIME = staticmethod(lambda  : ["VisibleType", "RUNTIME"])
    SETUP = staticmethod(lambda  : ["VisibleType", "SETUP"])
    HIDDEN = staticmethod(lambda  : ["VisibleType", "HIDDEN"])
    COMMON =  staticmethod(lambda  : ["VisibleType", "COMMON"])

class AccessType(object):
    READ_ONLY = staticmethod(lambda  : ["AccessType", "READ_ONLY"])
    READ_WRITE = staticmethod(lambda  : ["AccessType", "READ_WRITE"])