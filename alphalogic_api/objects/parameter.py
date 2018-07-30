# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from alphalogic_api.protocol import rpc_pb2

from alphalogic_api.attributes import Visible, Access
from alphalogic_api.multistub import MultiStub
from alphalogic_api import utils
from alphalogic_api.logger import log
from alphalogic_api.utils import Exit


class AbstractParameter(object):

    def _call(self, func_name, *args, **kwargs):
        return self.multi_stub.parameter_call(func_name, id=self.id, *args, **kwargs)

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
        answer = self._call('set_display_name', display_name=display_name)

    def set_desc(self, desc):
        answer = self._call('set_desc', desc=desc)

    def is_string(self):
        answer = self._call('is_string')
        return answer.yes

    def is_int(self):
        answer = self._call('is_int')
        return answer.yes

    def is_double(self):
        answer = self._call('is_double')
        return answer.yes

    def is_datetime(self):
        answer = self._call('is_datetime')
        return answer.yes

    def is_bool(self):
        answer = self._call('is_bool')
        return answer.yes

    def is_runtime(self):
        answer = self._call('is_runtime')
        return answer.yes

    def is_setup(self):
        answer = self._call('is_setup')
        return answer.yes

    def is_hidden(self):
        answer = self._call('is_hidden')
        return answer.yes

    def is_common(self):
        answer = self._call('is_common')
        return answer.yes

    def set_runtime(self):
        answer = self._call('set_runtime')

    def set_setup(self):
        answer = self._call('set_setup')

    def set_hidden(self):
        answer = self._call('set_hidden')

    def set_common(self):
        answer = self._call('set_common')

    def is_read_only(self):
        answer = self._call('is_read_only')
        return answer.yes

    def is_read_write(self):
        answer = self._call('is_read_write')
        return answer.yes

    def set_read_only(self):
        answer = self._call('set_read_only')

    def set_read_write(self):
        answer = self._call('set_read_write')

    def is_licensed(self):
        answer = self._call('is_licensed')
        return answer.yes

    def set_licensed(self):
        answer = self._call('set_licensed')

    def clear(self):
        answer = self._call('clear')

    def get(self):
        answer = self._call('get')
        return utils.value_from_rpc(answer.value)

    def set(self, value):
        value_rpc = utils.get_rpc_value(self.value_type, value)
        self._call('set', value=value_rpc)

    def enums(self):
        answer = self._call('enums')
        value_type_proto = utils.value_type_field_definer(self.value_type)
        return [(getattr(answer.enums[key], value_type_proto), key) for key in answer.enums]

    def set_enum(self, value, enum_name):
        value_type_proto = utils.value_type_field_definer(self.value_type)
        value_rpc = rpc_pb2.Value()
        setattr(value_rpc, value_type_proto, value)
        answer = self._call('set_enum', enum_name=enum_name, value=value_rpc)

    def set_enums(self, values):
        value_type = self.value_type
        req = rpc_pb2.ParameterRequest(id=self.id)
        attr_type = utils.value_type_field_definer(value_type)
        for val in values:
            if isinstance(val, tuple):
                setattr(req.enums[str(val[1])], attr_type, val[0])
            else:
                setattr(req.enums[str(val)], attr_type, val)

        self.multi_stub.call_helper('set_enums', fun_set=MultiStub.parameter_fun_set, request=req,
                                    stub=self.multi_stub.stub_parameter)

    def has_enum(self, enum_name):
        answer = self._call('has_enum', enum_name=enum_name)
        return answer.yes

    def owner(self):
        answer = self._call('owner')
        return answer.owner


class Parameter(AbstractParameter):
    index_number = 0

    def __init__(self, *args, **kwargs):
        self.index_number = Parameter.index_number
        Parameter.index_number += 1

        for arg in kwargs:
            self.__dict__[arg] = kwargs[arg]

        self.visible = kwargs.get('visible', Visible.runtime)
        self.access = kwargs.get('access', Access.read_write)
        self.callback = kwargs.get('callback', None)

        if 'value_type' not in kwargs:
            raise Exception('value_type not found in Parameter')

        if kwargs['value_type'] not in [bool, int, long, float, datetime.datetime, unicode]:
            raise Exception('value_type={0} is unknown'.format(kwargs['value_type']))

        self.default = kwargs.get('default')
        self.choices = kwargs.get('choices', None)

    def set_multi_stub(self, multi_stub):
        self.multi_stub = multi_stub

    def __getattr__(self, item):
        if item == 'val':
            return self.get()

        if item in self.__dict__:
            return self.__dict__[item]

    def __setattr__(self, attr, value):
        if attr == 'val' and self.parameter_name.lower() == 'name':  # exclude change 'name' value
            log.error('Attempt to change name of device')
            raise Exit

        if attr == 'val':
            if value is not None:
                self.set(value)
        elif attr in ['value_type', 'visible', 'access', 'default', 'choices', 'multi_stub', 'id',
                      'parameter_name', 'callback', 'index_number']:
            self.__dict__[attr] = value
        return self

    def set_choices(self):
        if isinstance(self.choices, tuple):
            self.clear()
            self.set_enums(self.choices)

    def get_copy(self):
        return Parameter(value_type=self.value_type, default=self.default, visible=self.visible,
                         access=self.access, callback=self.callback, choices=self.choices)


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

