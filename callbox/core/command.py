# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from callbox.core.type_attributes import runtime, setup, hidden, common
from callbox.core.type_attributes import read_only, read_write
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub

import inspect
import callbox.core.utils as utils

class AbstractCommand(object):

    def get_name(self):
        answer = self.multi_sub.command_call('name', id=self.id)
        return answer.name

    def get_display_name(self):
        answer = self.multi_sub.command_call('display_name', id=self.id)
        return answer.display_name

    def get_desc(self):
        answer = self.multi_sub.command_call('desc', id=self.id)
        return answer.desc

    def set_display_name(self, display_name):
        answer = self.multi_stub.command_call('set_display_name', id=self.id, display_name=display_name)

    def set_desc(self, desc):
        answer = self.multi_stub.command_call('set_desc', id=self.id, desc=desc)

    def is_string(self):
        answer = self.multi_sub.command_call('is_string', id=self.id)
        return answer.yes

    def is_int(self):
        answer = self.multi_sub.command_call('is_int', id=self.id)
        return answer.yes

    def is_double(self):
        answer = self.multi_sub.command_call('is_double', id=self.id)
        return answer.yes

    def is_datetime(self):
        answer = self.multi_sub.command_call('is_datetime', id=self.id)
        return answer.yes

    def is_bool(self):
        answer = self.multi_sub.command_call('is_bool', id=self.id)
        return answer.yes

    def set_result(self, value):
        value_rpc = utils.get_rpc_value(type(value), value)
        answer = self.multi_stub.command_call('set_result', id=self.id, value=value_rpc)

    def clear(self):
        answer = self.multi_stub.command_call('clear', id=self.id)

    def argument_list(self):
        answer = self.multi_stub.command_call('argument_list', id=self.id)
        return answer.names

    def argument(self, name_argument, type_argument):
        answer = self.multi_stub.command_call('argument', id=self.id, argument=name_argument)
        return getattr(answer.value, type_argument)

    def set_argument(self, name_arg, value):
        value_rpc = rpc_pb2.Value()
        value_type = utils.value_field_definer(value)
        if value_type!='list' and value_type!='tuple':
            setattr(value_rpc, value_type, value)
            answer = self.multi_stub.command_call('set_argument', id=self.id,
                                                  argument=name_arg, value=value_rpc)
        else:
            req = rpc_pb2.CommandRequest(id=self.id, argument=name_arg)
            for index, val in enumerate(value):
                if isinstance(val, dict):  # два поля в листе
                    val_type = utils.value_field_definer(val.values()[0])
                    setattr(req.enums[val.keys()[0]], val_type, val.values()[0])
                    if index==0:
                        setattr(req.value, val_type, val.values()[0])
                else:
                    val_type = utils.value_field_definer(val)
                    setattr(req.enums[str(val)], val_type, val)
                    if index==0:
                        setattr(req.value, val_type, val)

            answer = self.multi_stub.call_helper('set_argument', fun_set=MultiStub.command_fun_set, request=req,
                            stub=self.multi_stub.stub_command)

    def owner(self):
        answer = self.multi_stub.command_call('owner', id=self.id)
        return answer.owner

class Command(AbstractCommand):
    def __init__(self, function):
        self.function = function
        self.result_type = function.result_type
        self.arguments = function.arguments
        self.arguments_type = function.arguments_type

    def set_multi_stub(self, multi_stub):
        self.multi_stub = multi_stub

    def call_function(self):
        arg_list = self.argument_list()
        function_dict = {}
        for name_arg in arg_list:
            type_arg = self.arguments_type[name_arg]
            function_dict[name_arg] = self.argument(name_arg, utils.value_type_field_definer(type_arg))
        self.function(self, **function_dict)


def command_preparation(wrapped, func, **kwargs_c): #В этой функции задаются возвращаемое значение команды и ее аргументы
    wrapped.result_type = kwargs_c['result_type']
    (args, varargs, keywords, defaults) = inspect.getargspec(func)
    bias = 1 if 'self' in args else 0 # если первый аргумент self, то нужно рассматривать со второго элемента
    wrapped.__dict__['arguments'] = {}
    wrapped.__dict__['arguments_type'] = {}
    for index, name in enumerate(args[bias:]):
        wrapped.arguments[name] = defaults[index]
        wrapped.arguments_type[name] = utils.get_command_argument_type(defaults[index])

def command(*argv_c, **kwargs_c):
    def decorator(func):
        def wrapped(this_command, *argv, **kwargs):
            result = func(this_command, *argv, **kwargs)
            this_command.set_result(result)
            return result
        command_preparation(wrapped, func, **kwargs_c)
        return wrapped
    return decorator