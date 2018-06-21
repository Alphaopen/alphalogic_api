# -*- coding: utf-8 -*-

from callbox.core.type_attributes import VisibleType, ValueType, AccessType
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub

import inspect

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
        value_type_proto = ValueType.set_value_type[self.ValueType]('').keys()[0]
        value_rpc = rpc_pb2.Value()
        setattr(value_rpc, value_type_proto, value)
        answer = self.multi_stub.parameter_call('set', id=self.id, value=value_rpc)

    def clear(self):
        pass

    def argument_list(self):
        pass

    def argument(self):
        pass

    def set_argument(self):
        pass

    def owner(self):
        pass


def command_preparation(wrapped, func, **kwargs_c): #В этой функции задаются возвращаемое значение команды и ее аргументы
    wrapped.result_type = kwargs_c['result_type']
    (args, varargs, keywords, defaults) = inspect.getargspec(func)
    bias = 1 if 'self' in args else 0 # если первый аргумент self, то нужно рассматривать со второго элемента
    wrapped.__dict__['arguments'] = {}
    for index, name in enumerate(args[bias:]):
        wrapped.arguments[name] = defaults[index]

def command(*argv_c, **kwargs_c):
    def decorator(func):
        def wrapped(self, *argv, **kwargs):
            return func(*argv, **kwargs)
        command_preparation(wrapped, func, **kwargs_c)
        return wrapped
    return decorator