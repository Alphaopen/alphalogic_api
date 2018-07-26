# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from alphalogic_api.protocol import rpc_pb2
from alphalogic_api.multistub import MultiStub
from alphalogic_api import utils
from alphalogic_api.logger import log
from alphalogic_api.exceptions import exception_info


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
        value_type = utils.value_type_field_definer(type(value))
        cur_choices = self.choices[name_arg] if name_arg in self.choices else None
        if cur_choices is None:
            value_rpc = utils.get_rpc_value(type(value), value)
            self._call('set_argument', argument=name_arg, value=value_rpc)
        else:
            req = rpc_pb2.CommandRequest(id=self.id, argument=name_arg)
            val_type = utils.value_type_field_definer(type(value))
            setattr(req.value, val_type, value)
            for val in cur_choices:
                if isinstance(val, tuple):
                    val_type = utils.value_type_field_definer(type(val[0]))
                    setattr(req.enums[val[1]], val_type, val[0])
                else:
                    val_type = utils.value_type_field_definer(type(val))
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
