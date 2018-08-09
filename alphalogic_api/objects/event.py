# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from alphalogic_api import utils
from alphalogic_api.attributes import Priority


class AbstractEvent(object):
    """
    AbstractEvent implements EventService service(see `rpc.proto <https://github.com/Alphaopen/alphalogic_api/blob/
    master/alphalogic_api/protocol/proto/rpc.proto>`_)
    """

    def _call(self, func_name, *args, **kwargs):
        return self.multi_stub.event_call(func_name, id=self.id, *args, **kwargs)

    def name(self):
        """
        Return name of event

        :rtype: unicode
        """
        return self._call('name').name

    def display_name(self):
        """
        Return display name of event

        :rtype: unicode
        """
        return self._call('display_name').display_name

    def desc(self):
        """
        Return description of event

        :rtype: unicode
        """
        return self._call('desc').desc

    def set_display_name(self, display_name):
        """
        Set display name of event

        :arg display_name: unicode
        """
        self._call('set_display_name', display_name=display_name)

    def set_desc(self, desc):
        """
        Set description of event

        :arg desc: unicode
        """
        self._call('set_desc', desc=desc)

    def is_trivial(self):
        """
        Function return True if type of event is trivial

        :rtype: bool
        """
        return self._call('is_trivial').yes

    def is_minor(self):
        """
        Function return True if type of event is minor

        :rtype: bool
        """
        return self._call('is_minor').yes

    def is_major(self):
        """
        Function return True if type of event is major

        :rtype: bool
        """
        return self._call('is_major').yes

    def is_critical(self):
        """
        Function return True if type of event is critical

        :rtype: bool
        """
        return self._call('is_critical').yes

    def is_blocker(self):
        """
        Function return True if type of event is blocker

        :rtype: bool
        """
        return self._call('is_blocker').yes

    def set_trivial(self):
        """
        Set type of event to trivial
        """
        self._call('set_trivial')

    def set_minor(self):
        """
        Set type of event to minor
        """
        self._call('set_minor')

    def set_major(self):
        """
        Set type of event to major
        """
        self._call('set_major')

    def set_critical(self):
        """
        Set type of event to critical
        """
        self._call('set_critical')

    def set_blocker(self):
        """
        Set type of event to blocker
        """
        self._call('set_blocker')

    def set_time(self, timestamp):
        """
        Set event time UTC

        :param timestamp: int(time.time() * 1000) (мс)
        """
        self._call('set_time', time=timestamp)

    def emit(self, **kwargs):
        """
        | Function emit event with the current UTC time.
        | In order to set timestamp other than the current UTC time, you should call set_time function with required
         timestamp before execute emit function.

        :param kwargs: arguments
        """
        for arg_name, arg_type in self.arguments:
            if arg_name not in kwargs:
                raise Exception('Incorrect argument name of event {0}'.format(self.name))

            value_rpc = utils.get_rpc_value(arg_type, kwargs[arg_name])
            self._call('set_argument', argument=arg_name, value=value_rpc)

        self._call('emit')

    def clear(self):
        """
        Remove event arguments
        """
        self._call('clear')

    def argument_list(self):
        """
        Function return argument list of event

        :rtype: list of arguments names
        """
        answer = self._call('argument_list')
        return answer.names

    def argument(self, name_argument):
        """
        Function return argument of event

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
        Set argument in event

        :arg name_arg: name of argument
        :arg value: value of argument
        """
        value_type = utils.value_type_field_definer(type(value))

        if value_type not in ['list', 'tuple']:
            value_rpc = utils.get_rpc_value(type(value), value)
            self._call('set_argument', argument=name_arg, value=value_rpc)
        else:
            raise Exception('Event argument type not supported')

    def owner(self):
        """
        Function return id of event's owner

        :rtype: uint64
        """
        answer = self._call('owner')
        return answer.owner


class Event(AbstractEvent):
    """
    Event inherits from :class:`~alphalogic_api.objects.event.AbstractEvent`.

    :arg priority: trivial, minor, major, critical, blocker
    :arg args: tuple of tuples (argument name, argument type)
    """
    def __init__(self, priority, *args):
        self.arguments = args
        self.id = None
        self.priority = priority
        self.multi_stub = None

    def set_multi_stub(self, multi_stub):
        self.multi_stub = multi_stub


class TrivialEvent(Event):
    def __new__(cls, *args):
        return Event(Priority.trivial, *args)


class MinorEvent(Event):
    def __new__(cls, *args):
        return Event(Priority.minor, *args)


class MajorEvent(Event):
    def __new__(cls, *args):
        return Event(Priority.major, *args)


class CriticalEvent(Event):
    def __new__(cls, *args):
        return Event(Priority.critical, *args)


class BlockerEvent(Event):
    def __new__(cls, *args):
        return Event(Priority.blocker, *args)
