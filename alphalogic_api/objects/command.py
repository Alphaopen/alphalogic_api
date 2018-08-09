# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from alphalogic_api.protocol import rpc_pb2
from alphalogic_api.multistub import MultiStub
from alphalogic_api import utils
from alphalogic_api.logger import log
import traceback


class AbstractCommand(object):
    """
    AbstractCommand implements CommandService service(see `rpc.proto <https://github.com/Alphaopen/alphalogic_api/blob/
    master/alphalogic_api/protocol/proto/rpc.proto>`_)
    """

    def _call(self, func_name, *args, **kwargs):
        return self.multi_stub.command_call(func_name, id=self.id, *args, **kwargs)

    def name(self):
        """
        Return name of command

        :rtype: unicode
        """
        answer = self._call('name')
        return answer.name

    def display_name(self):
        """
        Return display name of command

        :rtype: unicode
        """
        answer = self._call('display_name')
        return answer.display_name

    def desc(self):
        """
        Return description of command

        :rtype: unicode
        """
        answer = self._call('desc')
        return answer.desc

    def set_display_name(self, display_name):
        """
        Set display name of command

        :arg display_name: unicode
        """
        self._call('set_display_name', display_name=display_name)

    def set_desc(self, desc):
        """
        Set description of command

        :arg desc: unicode
        """
        self._call('set_desc', desc=desc)

    def is_string(self):
        """
        Function return True if result type of command is string

        :rtype: bool
        """
        answer = self._call('is_string')
        return answer.yes

    def is_long(self):
        """
        Function return True if result type of command is long

        :rtype: bool
        """
        answer = self._call('is_long')
        return answer.yes

    def is_double(self):
        """
        Function return True if result type of command is double

        :rtype: bool
        """
        answer = self._call('is_double')
        return answer.yes

    def is_datetime(self):
        """
        Function return True if result type of command is datetime

        :rtype: bool
        """
        answer = self._call('is_datetime')
        return answer.yes

    def is_bool(self):
        """
        Function return True if result type of command is bool

        :rtype: bool
        """
        answer = self._call('is_bool')
        return answer.yes

    def set_result(self, value):
        """
        Set result in command

        :arg value: The possible types of value: long, float, datetime, bool and unicode
        """
        value_rpc = utils.get_rpc_value(type(value), value)
        self._call('set_result', value=value_rpc)

    def set_exception(self, reason):
        """
        Set exception in command.
        Information about exception will be called for adapter's side.

        :arg reason: state unicode string
        """
        self._call('set_exception', exception=reason)

    def clear(self):
        """
        Remove command's arguments
        """
        self._call('clear')

    def argument_list(self):
        """
        Function return argument list of command

        :rtype: list of arguments names
        """
        answer = self._call('argument_list')
        return answer.names

    def argument(self, name_argument):
        """
        Function return argument of command

        :arg name_argument: name of argument
        :rtype:
            | tuple (name, value)
            | name is name of argument
            | value is value of argument
        """
        answer = self._call('argument', argument=name_argument)
        return answer.name, answer.value

    def set_argument(self, name_arg, value):
        """
        Set argument in command

        :arg name_arg: name of argument
        :arg value: value of argument
        """
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
                e = req.enums.add()
                if isinstance(val, tuple):
                    e.name = val[1]
                    val_type = utils.value_type_field_definer(type(val[0]))
                    setattr(e.value, val_type, val[0])
                else:
                    e.name = unicode(val)
                    val_type = utils.value_type_field_definer(type(val))
                    setattr(e.value, val_type, val)

            self.multi_stub.call_helper('set_argument', fun_set=MultiStub.command_fun_set,
                                        request=req, stub=self.multi_stub.stub_command)

    def owner(self):
        """
        Function return id of command's owner

        :rtype: uint64
        """
        answer = self._call('owner')
        return answer.owner


class Command(AbstractCommand):
    """
    | Command class is used in command decorator.
    | Command inherits from :class:`~alphalogic_api.objects.command.AbstractCommand`.

    :arg device: has :class:`~alphalogic_api.objects.Object` type
    :arg function: executed function
    """
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
        """
        This function is performed when user call command

        :rtype: result type is defined in function of adapter code
        """
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
            t = traceback.format_exc()
            log.error('Command \'{0}\' raise exception: {1}'.format(self.name(), t))
