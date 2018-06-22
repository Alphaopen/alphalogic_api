# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub


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

    def set_time(self, t):
        answer = self.multi_sub.event_call('set_time', id=self.id, time=t)

    def emit(self, **kwargs):  # TODO
        # set_argument
        answer = self.multi_stub.event_call('emit', id=self.id, args=kwargs)

    def clear(self):
        answer = self.multi_stub.event_call('clear', id=self.id)
