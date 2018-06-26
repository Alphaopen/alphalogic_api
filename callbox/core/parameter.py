# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import callbox.protocol.rpc_pb2 as rpc_pb2

from callbox.core.type_attributes import runtime, setup, hidden, common, read_only, read_write
from callbox.core.multistub import MultiStub
from callbox.core import utils


class AbstractParameter(object):

    def _call(name, *args, **kwargs):
        return self.multi_stub.parameter_call(name, id=self.id, *args, **kwargs)

    def name(self):
        answer = self._call('name')
        return answer.name

    def display_name(self):
        answer = self._call('display_name')
        return answer.display_name

    def desc(self):
        answer = self._call('desc')
        return answer.desc

    def set_display_name(self, display_name):
        answer = self._call('set_display_name', display_name=display_name)  # и так далее...

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
        value_type_proto = utils.value_type_field_definer(self.value_type)
        return getattr(answer.value, value_type_proto)

    def set(self, value):
        value_type_proto = utils.value_type_field_definer(self.value_type)
        value_rpc = rpc_pb2.Value()
        setattr(value_rpc, value_type_proto, value)
        answer = self.multi_stub.parameter_call('set', id=self.id, value=value_rpc)

    def enums(self):
        answer = self.multi_stub.parameter_call('enums', id=self.id)
        value_type_proto = utils.value_type_field_definer(self.value_type)
        return [(key, getattr(answer.enums[key], value_type_proto)) for key in answer.enums]

    def set_enum(self, value, enum_name):
        value_type_proto = utils.value_type_field_definer(self.value_type)
        value_rpc = rpc_pb2.Value()
        setattr(value_rpc, value_type_proto, value)
        answer = self.multi_stub.parameter_call('set_enum', id=self.id, enum_name=enum_name, value=value_rpc)

    def set_enums(self, values):
        value_type = self.value_type
        req = rpc_pb2.ParameterRequest(id=self.id)
        attr_type = utils.value_type_field_definer(value_type)
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
        for arg in kwargs:
            self.__dict__[arg] = kwargs[arg]

        if not('visible' in kwargs):
            self.visible = runtime
        if not('access' in kwargs):
            self.access = read_write
        if not ('value_type' in kwargs):
            raise Exception('value_type not found in Parameter')

        if kwargs['value_type'] not in [bool, int, float, datetime.datetime, unicode]:
            raise Exception('value_type={0} is unknown'.format(kwargs['value_type']))

        if 'value' in kwargs:
            self.value = kwargs['value']

        if 'default' in kwargs:
            self.value = kwargs['default']


    def set_multi_stub(self, multi_stub):
        self.multi_stub = multi_stub

    def __getattr__(self, item):
        if (item == 'value'):
            return None

        if (item == 'val'):
            return self.get()

    def __setattr__(self, attr, value):
        if attr in ['value_type', 'visible', 'access', 'value', 'name', 'multi_stub', 'id']:
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
        return Parameter(*args, value_type=bool, **kwargs)


class ParameterInt(Parameter):
    def __new__(cls, *args, **kwargs):
        return Parameter(*args, value_type=int, **kwargs)


class ParameterDouble(Parameter):
    def __new__(cls, *args, **kwargs):
        return Parameter(*args, value_type=float, **kwargs)


class ParameterDatetime(Parameter):
    def __new__(cls, *args, **kwargs):
        return Parameter(*args, value_type=datetime.datetime, **kwargs)


class ParameterString(Parameter):
    def __new__(cls, *args, **kwargs):
        return Parameter(*args, value_type=unicode, **kwargs)

