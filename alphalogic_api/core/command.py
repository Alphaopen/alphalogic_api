# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import inspect
import alphalogic_api.protocol.rpc_pb2 as rpc_pb2
from alphalogic_api.core.multistub import MultiStub
import alphalogic_api.core.utils as utils
from alphalogic_api.logger import log
from alphalogic_api.core.exceptions import exception_info


class AbstractCommand(object):

    def _call(self, func_name, *args, **kwargs):
        return self.multi_stub.command_call(func_name, id=self.id, *args, **kwargs)

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
        self._call('set_display_name', display_name=display_name)

    def set_desc(self, desc):
        self._call('set_desc', desc=desc)

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

    def set_result(self, value):
        value_rpc = utils.get_rpc_value(type(value), value)
        self._call('set_result', value=value_rpc)

    def set_exception(self, reason):
        self._call('set_exception', exception=reason)

    def clear(self):
        self._call('clear')

    def argument_list(self):
        answer = self._call('argument_list')
        return answer.names

    def argument(self, name_argument):
        answer = self._call('argument', argument=name_argument)
        return answer.name, answer.value

    def set_argument(self, name_arg, value):
        value_type = utils.value_field_definer(value)
        cur_choices = self.choices[name_arg] if name_arg in self.choices else None
        if cur_choices is None:
            value_rpc = utils.get_rpc_value(type(value), value)
            self._call('set_argument', argument=name_arg, value=value_rpc)
        else:
            req = rpc_pb2.CommandRequest(id=self.id, argument=name_arg)
            val_type = utils.value_field_definer(value)
            setattr(req.value, val_type, value)
            for index, val in enumerate(cur_choices):
                if isinstance(val, tuple):
                    val_type = utils.value_field_definer(val[0])
                    setattr(req.enums[val[1]], val_type, val[0])
                else:
                    val_type = utils.value_field_definer(val)
                    setattr(req.enums[str(val)], val_type, val)

            self.multi_stub.call_helper('set_argument', fun_set=MultiStub.command_fun_set,
                                        request=req, stub=self.multi_stub.stub_command)

    def owner(self):
        answer = self._call('owner')
        return answer.owner


class Command(AbstractCommand):
    def __init__(self, device, function):
        self.function = function
        self.result_type = function.result_type
        self.arguments = function.arguments
        self.arguments_type = function.arguments_type
        self.choices = function.choices
        self.device = device

    def set_multi_stub(self, multi_stub):
        self.multi_stub = multi_stub

    def call_function(self):
        try:
            arg_list = self.argument_list()
            function_dict = {}
            info = []
            for name_arg in arg_list:
                type_arg = self.arguments_type[name_arg]
                function_dict[name_arg] = utils.value_from_rpc(self.argument(name_arg)[1])
                info.append('{0}({1}): {2}'.format(name_arg, type_arg, function_dict[name_arg]))

            log.info('Execute command \'{0}\' with arguments [{1}] from device \'{2}\''
                     .format(self.name(), '; '.join(info), self.device.id))
            self.function(self.device, **function_dict)

        except Exception, err:
            exception_info()
            reason = utils.decode_string(err)
            log.info('Command \'{0}\' raise exception: \'{1}\''.format(self.name(), reason))
            self.set_exception(reason)


def command_preparation(wrapped, func, **kwargs_c):
    """
    Return value and command arguments setup
    """
    wrapped.result_type = kwargs_c['result_type']
    (args, varargs, keywords, defaults) = inspect.getargspec(func)
    wrapped.__dict__['arguments'] = []
    wrapped.__dict__['arguments_type'] = {}
    wrapped.__dict__['function_name'] = func.__name__
    wrapped.__dict__['choices'] = {}
    for name_arg in filter(lambda x: x in kwargs_c, args):
        wrapped.choices[name_arg] = kwargs_c[name_arg]
    bias = 1 if 'self' in args else 0  # if first arg is self, see from second
    for index, name in enumerate(args[bias:]):
        wrapped.arguments.append((name, defaults[index]))
        wrapped.arguments_type[name] = utils.get_command_argument_type(defaults[index])


def command(*argv_c, **kwargs_c):
    def decorator(func):
        def wrapped(device, *argv, **kwargs):
            result = func(device, *argv, **kwargs)
            device.__dict__[wrapped.function_name].set_result(result)
            return result
        command_preparation(wrapped, func, **kwargs_c)
        return wrapped
    return decorator
