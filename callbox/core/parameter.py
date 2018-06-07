# -*- coding: utf-8 -*-

from callbox.core.type_attributes import VisibleType, ValueType, AccessType

class Parameter(object):
    def __init__(self, *args, **kwargs):
        #self.name = name
        for arg in filter(lambda arg : callable(arg) , args):
            self.__dict__[arg()[0]] = arg()[1] # пр. ["ValueType", "STRING"]

        if not('VisibleType' in self.__dict__):
            self.VisibleType = VisibleType.RUNTIME()[1]
        if not('AccessType' in self.__dict__):
            self.AccessType = AccessType.READ_WRITE()[1]
        #if not ('ValueType' in self.__dict__):
            #raise Exception('ValueType not found in Parameter')

        if 'Value' in kwargs:
            self.Value = kwargs['Value']


class ParameterBool(Parameter):
    def __init__(self, *args, **kwargs):
        self.ValueType = ValueType.BOOL()[1]
        super(ParameterBool, self).__init__(*args, **kwargs)


class ParameterInt64(Parameter):
    def __init__(self, *args, **kwargs):
        self.ValueType = ValueType.INT64()[1]
        super(ParameterInt64, self).__init__(*args, **kwargs)


class ParameterDouble(Parameter):
    def __init__(self, *args, **kwargs):
        self.ValueType = ValueType.DOUBLE()[1]
        super(ParameterDouble, self).__init__(*args, **kwargs)


class ParameterDatetime(Parameter):
    def __init__(self, *args, **kwargs):
        self.ValueType = ValueType.DATETIME()[1]
        super(ParameterDatetime, self).__init__(*args, **kwargs)

class ParameterString(Parameter):
    def __init__(self, *args, **kwargs):
        self.ValueType = ValueType.STRING()[1]
        super(ParameterString, self).__init__(*args, **kwargs)

PARAMETER_LIST = [Parameter, ParameterBool, ParameterInt64, ParameterDouble, ParameterDatetime, ParameterString]