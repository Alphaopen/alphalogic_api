# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from callbox.core.type_attributes import EventPriority
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub
import time
import datetime

class AbstractEvent(object):

    def get_name(self):
        answer = self.multi_sub.event_call('name', id=self.id)
        return answer.name

    def get_display_name(self):
        answer = self.multi_sub.event_call('display_name', id=self.id)
        return answer.display_name

    def get_desc(self):
        answer = self.multi_sub.event_call('desc', id=self.id)
        return answer.desc

    def set_display_name(self, display_name):
        answer = self.multi_stub.event_call('set_display_name', id=self.id, display_name=display_name)

    def set_desc(self, desc):
        answer = self.multi_stub.event_call('set_desc', id=self.id, desc=desc)

    def is_trivial(self):
        answer = self.multi_sub.event_call('is_trivial', id=self.id)
        return answer.yes

    def is_minor(self):
        answer = self.multi_sub.event_call('is_minor', id=self.id)
        return answer.yes

    def is_major(self):
        answer = self.multi_sub.event_call('is_major', id=self.id)
        return answer.yes

    def is_critical(self):
        answer = self.multi_sub.event_call('is_critical', id=self.id)
        return answer.yes

    def is_blocker(self):
        answer = self.multi_sub.event_call('is_blocker', id=self.id)
        return answer.yes
    '''
    def set_trivial(self):
        answer = self.multi_sub.event_call('set_trivial', id=self.id)

    def set_minor(self):
        answer = self.multi_sub.event_call('set_minor', id=self.id)

    def set_major(self):
        answer = self.multi_sub.event_call('set_major', id=self.id)

    def set_critical(self):
        answer = self.multi_sub.event_call('set_critical', id=self.id)

    def set_blocker(self):
        answer = self.multi_sub.event_call('set_blocker', id=self.id)
    '''
    def set_time(self, timestamp):
        '''
        Установить время события
        :param timestamp: int(time.time() * 1000) (мс)
        '''
        self.multi_stub.event_call('set_time', id=self.id, time=timestamp)

    def emit(self, **kwargs):  # TODO
        '''
        Если время требуется не текущее, то вызовите set_time
        :param kwargs: аргументы
        '''
        # set_argument

        for key, val in kwargs.iteritems():
            if key not in self.args.keys():
                raise Exception('Incorrect argument name of event {0}'.format(self.name))
            value_rpc = rpc_pb2.Value()
            if self.args[key] == int:
                value_rpc.int64_value = val
            elif self.args[key] == str:
                value_rpc.string_value = val
            elif self.args[key] == float:
                value_rpc.double_value = val
            elif self.args[key] == datetime.datetime:
                value_rpc.datetime_value = val  # ms
            elif self.args[key] == bool:
                value_rpc.bool_value = val

        self.multi_stub.event_call('emit', id=self.id)

    def clear(self):
        self.multi_stub.event_call('clear', id=self.id)


class Event(AbstractEvent):
    def __init__(self, **kwargs):
        self.priority = kwargs.get('priority', EventPriority.MAJOR)
        self.args = kwargs.get('args', {})
        self.id = None
        self.multi_stub = None

    def set_multi_stub(self, multi_stub):
        self.multi_stub = multi_stub
