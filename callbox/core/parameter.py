# -*- coding: utf-8 -*-

from callbox.core.type_attributes import VisibleType, ValueType, AccessType
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub


class AbstractParameter(object):
    def get_name(self):
        answer = self.multi_stub.parameter_call('name', id=self.id)
        return answer.name

    def display_name(self):
        answer = self.multi_stub.parameter_call('display_name', id=self.id)
        return answer.display_name

    def desc(self):
        answer = self.multi_stub.parameter_call('desc', id=self.id)
        return answer.desc

    def set_display_name(self, display_name):
        answer = self.multi_stub.parameter_call('set_display_name', id=self.id, display_name=display_name)

    def set_desc(self, desc):
        answer = self.multi_stub.parameter_call('set_desc', id=self.id, desc=desc)

    def is_string(self):
        answer = self.multi_stub.parameter_call('is_string', id=self.id)
        return answer.yes

    def is_int(self):
        answer = self.multi_stub.parameter_call('is_int', id=self.id)
        return answer.yes

    def is_double(self):
        answer = self.multi_stub.parameter_call('is_double', id=self.id)
        return answer.yes

    def is_datetime(self):
        answer = self.multi_stub.parameter_call('is_datetime', id=self.id)
        return answer.yes

    def is_bool(self):
        answer = self.multi_stub.parameter_call('is_bool', id=self.id)
        return answer.yes

    def is_runtime(self):
        answer = self.multi_stub.parameter_call('is_runtime', id=self.id)
        return answer.yes

    def is_setup(self):
        answer = self.multi_stub.parameter_call('is_setup', id=self.id)
        return answer.yes

    def is_hidden(self):
        answer = self.multi_stub.parameter_call('is_hidden', id=self.id)
        return answer.yes

    def is_common(self):
        answer = self.multi_stub.parameter_call('is_common', id=self.id)
        return answer.yes

    def set_runtime(self):
        answer = self.multi_stub.parameter_call('set_runtime', id=self.id)

    def set_setup(self):
        answer = self.multi_stub.parameter_call('set_setup', id=self.id)

    def set_hidden(self):
        answer = self.multi_stub.parameter_call('set_hidden', id=self.id)

    def set_common(self):
        answer = self.multi_stub.parameter_call('set_common', id=self.id)

    def is_read_only(self):
        answer = self.multi_stub.parameter_call('is_read_only', id=self.id)
        return answer.yes

    def is_read_write(self):
        answer = self.multi_stub.parameter_call('is_read_write', id=self.id)
        return answer.yes

    def set_read_only(self):
        answer = self.multi_stub.parameter_call('set_read_only', id=self.id)

    def set_read_write(self):
        answer = self.multi_stub.parameter_call('set_read_write', id=self.id)

    def is_licensed(self):
        answer = self.multi_stub.parameter_call('is_licensed', id=self.id)
        return answer.yes

    def set_licensed(self):
        answer = self.multi_stub.parameter_call('set_licensed', id=self.id)

    def clear(self):
        answer = self.multi_stub.parameter_call('clear', id=self.id)

    def get(self):
        answer = self.multi_stub.parameter_call('get', id=self.id)
        value_type_proto = ValueType.set_value_type[self.ValueType]('').keys()[0]
        return getattr(answer.value, value_type_proto)

    def set(self, value):
        value_type_proto = ValueType.set_value_type[self.ValueType]('').keys()[0]
        value_rpc = rpc_pb2.Value()
        setattr(value_rpc, value_type_proto, value)
        answer = self.multi_stub.parameter_call('set', id=self.id, value=value_rpc)

    def enums(self):
        answer = self.multi_stub.parameter_call('enums', id=self.id)
        value_type_proto = ValueType.set_value_type[self.ValueType]('').keys()[0]
        return [(key, getattr(answer.enums[key], value_type_proto)) for key in answer.enums]

    def set_enum(self, value, enum_name):
        value_type_proto = ValueType.set_value_type[self.ValueType]('').keys()[0]
        value_rpc = rpc_pb2.Value()
        setattr(value_rpc, value_type_proto, value)
        answer = self.multi_stub.parameter_call('set_enum', id=self.id, enum_name=enum_name, value=value_rpc)

    def set_enums(self, values):
        value_type = self.ValueType
        req = rpc_pb2.ParameterRequest(id=self.id)
        attr_type = ValueType.set_value_type[value_type]('').keys()[0]
        for val in values:
            if isinstance(val, dict):  # два поля в листе
                setattr(req.enums[val.keys()[0]], attr_type, val.values()[0])  # проверить
            else:
                setattr(req.enums[str(val)], attr_type, val)

        self.multi_stub.call_helper('set_enums', fun_set=MultiStub.parameter_fun_set, request=req,
                                    stub=self.multi_stub.stub_parameter)

    def has_enum(self, enum_name):
        answer = self.multi_stub.parameter_call('has_enum', id=self.id, enum_name=enum_name)
        return answer.yes

    def owner(self):
        answer = self.multi_stub.parameter_call('owner', id=self.id)
        return answer.owner


class Parameter(AbstractParameter):
    def __init__(self, *args, **kwargs):
        for arg in filter(lambda arg : callable(arg) , args):
            self.__dict__[arg()[0]] = arg()[1] # example: ["ValueType", "STRING"], ["VisibleType" , "RUNTIME"]

        if not('VisibleType' in self.__dict__):
            self.VisibleType = VisibleType.RUNTIME()[1]
        if not('AccessType' in self.__dict__):
            self.AccessType = AccessType.READ_WRITE()[1]
        if not ('ValueType' in self.__dict__):
            raise Exception('ValueType not found in Parameter')

        if 'Value' in kwargs:
            self.Value = kwargs['Value']

    def set_multi_stub(self, multi_stub):
        self.multi_stub = multi_stub

    def __getattr__(self, item):
        if (item == 'Value'):
            return None

        if (item == 'val'):
            return self.get()

    def __setattr__(self, attr, value):
        if attr in ['ValueType', 'VisibleType', 'AccessType', 'Value', 'name', 'multi_stub', 'id']:
            self.__dict__[attr] = value
        elif attr == 'val':
            if value is not None:
                if not (isinstance(value, list)):  # для одного значения
                    self.set(value)
                else:  # для списков
                    self.set_enums(value)
            return self


class ParameterBool(Parameter):
    def __new__(cls, *args, **kwargs):
        return Parameter(ValueType.BOOL, *args, **kwargs)


class ParameterInt64(Parameter):
    def __new__(cls, *args, **kwargs):
        return Parameter(ValueType.INT64, *args, **kwargs)


class ParameterDouble(Parameter):
    def __new__(cls, *args, **kwargs):
        return Parameter(ValueType.DOUBLE, *args, **kwargs)


class ParameterDatetime(Parameter):
    def __new__(cls, *args, **kwargs):
        return Parameter(ValueType.DATETIME, *args, **kwargs)


class ParameterString(Parameter):
    def __new__(cls, *args, **kwargs):
        return Parameter(ValueType.STRING, *args, **kwargs)

