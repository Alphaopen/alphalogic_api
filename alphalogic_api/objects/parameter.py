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
    """
    AbstractParameter implements ParameterService service(see `rpc.proto <https://github.com/Alphaopen/alphalogic_api/
    blob/master/alphalogic_api/protocol/proto/rpc.proto>`_)
    """

    def _call(self, func_name, *args, **kwargs):
        return self.multi_stub.parameter_call(func_name, id=self.id, *args, **kwargs)

    def name(self):
        """
        Return name of parameter

        :rtype: unicode
        """
        answer = self._call('name')
        return answer.name

    def display_name(self):
        """
        Return display name of parameter

        :rtype: unicode
        """
        answer = self._call('display_name')
        return answer.display_name

    def desc(self):
        """
        Return description of parameter

        :rtype: unicode
        """
        answer = self._call('desc')
        return answer.desc

    def set_display_name(self, display_name):
        """
        Set display name of parameter

        :arg display_name: unicode
        """
        answer = self._call('set_display_name', display_name=display_name)

    def set_desc(self, desc):
        """
        Set description of parameter

        :arg desc: unicode
        """
        answer = self._call('set_desc', desc=desc)

    def is_string(self):
        """
        Function return True if type of parameter is string

        :rtype: bool
        """
        answer = self._call('is_string')
        return answer.yes

    def is_long(self):
        """
        Function return True if type of parameter is long

        :rtype: bool
        """
        answer = self._call('is_long')
        return answer.yes

    def is_double(self):
        """
        Function return True if type of parameter is double

        :rtype: bool
        """
        answer = self._call('is_double')
        return answer.yes

    def is_datetime(self):
        """
        Function return True if type of parameter is datetime

        :rtype: bool
        """
        answer = self._call('is_datetime')
        return answer.yes

    def is_bool(self):
        """
        Function return True if type of parameter is bool

        :rtype: bool
        """
        answer = self._call('is_bool')
        return answer.yes

    def is_runtime(self):
        """
        Function return True if visible type of parameter is runtime

        :rtype: bool
        """
        answer = self._call('is_runtime')
        return answer.yes

    def is_setup(self):
        """
        Function return True if visible type of parameter is setup

        :rtype: bool
        """
        answer = self._call('is_setup')
        return answer.yes

    def is_hidden(self):
        """
        Function return True if visible type of parameter is hidden

        :rtype: bool
        """
        answer = self._call('is_hidden')
        return answer.yes

    def is_common(self):
        """
        Function return True if visible type of parameter is common

        :rtype: bool
        """
        answer = self._call('is_common')
        return answer.yes

    def set_runtime(self):
        """
        Set visible type of event to runtime
        """
        answer = self._call('set_runtime')

    def set_setup(self):
        """
        Set visible type of event to setup
        """
        answer = self._call('set_setup')

    def set_hidden(self):
        """
        Set visible type of event to hidden
        """
        answer = self._call('set_hidden')

    def set_common(self):
        """
        Set visible type of event to common
        """
        answer = self._call('set_common')

    def is_read_only(self):
        """
        Function return True if access type of event is read only

        :rtype: bool
        """
        answer = self._call('is_read_only')
        return answer.yes

    def is_read_write(self):
        """
        Function return True if access type of event is read write

        :rtype: bool
        """
        answer = self._call('is_read_write')
        return answer.yes

    def set_read_only(self):
        """
        Set access type of event to read only
        """
        answer = self._call('set_read_only')

    def set_read_write(self):
        """
        Set access type of event to read write
        """
        answer = self._call('set_read_write')

    def is_licensed(self):
        """
        Function return True if parameter is licensed

        :rtype: bool
        """
        answer = self._call('is_licensed')
        return answer.yes

    def set_licensed(self):
        """
        The function licenses the parameter
        """
        answer = self._call('set_licensed')

    def clear(self):
        """
        Remove predefined values list
        """
        answer = self._call('clear')

    def get(self):
        """
        Get value of parameter

        :rtype: The possible types of value: long, float, datetime, bool and unicode
        """
        answer = self._call('get')
        return utils.value_from_rpc(answer.value)

    def set(self, value):
        """
        Set value of parameter

        :arg value: The possible types of value: long, float, datetime, bool and unicode
        """
        value_rpc = utils.get_rpc_value(self.value_type, value)
        self._call('set', value=value_rpc)

    def enums(self):
        """
        Get predefined values from parameter

        :rtype: list of values (long, float, datetime, bool and unicode)
        """
        answer = self._call('enums')
        value_type_proto = utils.value_type_field_definer(self.value_type)
        return [(getattr(answer.enums[key], value_type_proto), key) for key in answer.enums]

    def set_enum(self, value, enum_name):
        """
        Add value to enum

        :param value: The possible types of value: long, float, datetime, bool and unicode
        :param enum_name: name of enum to add new value
        """
        value_type_proto = utils.value_type_field_definer(self.value_type)
        value_rpc = rpc_pb2.Value()
        setattr(value_rpc, value_type_proto, value)
        answer = self._call('set_enum', enum_name=enum_name, value=value_rpc)

    def set_enums(self, values):
        """
        Set predefined values of parameter

        :param values:
            | List of predefined values.
        """
        value_type = self.value_type
        req = rpc_pb2.ParameterRequest(id=self.id)
        attr_type = utils.value_type_field_definer(value_type)
        for val in values:
            e = req.enums.add()
            if isinstance(val, tuple):
                e.name = unicode(val[1])
                setattr(e.value, attr_type, val[0])
            else:
                e.name = unicode(val)
                setattr(e.value, attr_type, val)

        self.multi_stub.call_helper('set_enums', fun_set=MultiStub.parameter_fun_set, request=req,
                                    stub=self.multi_stub.stub_parameter)

    def has_enum(self, enum_name):
        """
        Function return True if parameter has predefined values

        :rtype: bool
        """
        answer = self._call('has_enum', enum_name=enum_name)
        return answer.yes

    def owner(self):
        """
        Function return id of parameter's owner

        :rtype: uint64
        """
        answer = self._call('owner')
        return answer.owner


class Parameter(AbstractParameter):
    """
    Parameter inherits from :class:`~alphalogic_api.objects.parameter.AbstractParameter`.
    """
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


class ParameterLong(Parameter):
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

