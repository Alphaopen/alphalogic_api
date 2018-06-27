# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from callbox.core import utils
from callbox.core.type_attributes import major
import callbox.protocol.rpc_pb2 as rpc_pb2
import datetime


class AbstractEvent(object):

    def _call(self, func_name, *args, **kwargs):
        return self.multi_stub.event_call(func_name, id=self.id, *args, **kwargs)

    def get_name(self):
        return self._call('name').name

    def get_display_name(self):
        return self._call('display_name').display_name

    def get_desc(self):
        return self._call('desc').desc

    def set_display_name(self, display_name):
        self._call('set_display_name', display_name=display_name)

    def set_desc(self, desc):
        self._call('set_desc', desc=desc)

    def is_trivial(self):
        return self._call('is_trivial').yes

    def is_minor(self):
        return self._call('is_minor').yes

    def is_major(self):
        return self._call('is_major').yes

    def is_critical(self):
        return self._call('is_critical').yes

    def is_blocker(self):
        return self._call('is_blocker').yes

    def set_trivial(self):
        self._call('set_trivial')

    def set_minor(self):
        self._call('set_minor')

    def set_major(self):
        self._call('set_major')

    def set_critical(self):
        self._call('set_critical')

    def set_blocker(self):
        self._call('set_blocker')

    def set_time(self, timestamp):
        """
        Установить время события
        :param timestamp: int(time.time() * 1000) (мс)
        """
        self._call('set_time', time=timestamp)

    def emit(self, **kwargs):  # TODO
        """
        Если время требуется не текущее, то вызовите set_time
        :param kwargs: аргументы
        """
        for key, value in kwargs.iteritems():
            if key not in self.args.keys():
                raise Exception('Incorrect argument name of event {0}'.format(self.name))

            value_rpc = utils.get_rpc_value(self.args[key], value)
            self._call('set_argument', argument=key, value=value_rpc)

        self._call('emit')

    def clear(self):
        self._call('clear')

    def set_argument(self, name, value_rpc):
        self._call('set_argument', argument=name, value=value_rpc)


class Event(AbstractEvent):
    def __init__(self, **kwargs):
        self.priority = kwargs.get('priority', major)
        self.args = kwargs.get('args', {})
        self.id = None
        self.multi_stub = None

    def set_multi_stub(self, multi_stub):
        self.multi_stub = multi_stub
