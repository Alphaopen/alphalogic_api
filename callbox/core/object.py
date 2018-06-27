# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub


class AbstractManager(object):

    def _call(self, name, *args, **kwargs):
        return self.multi_stub.object_call(name, id=self.id, *args, **kwargs)

    def root(self):
        answer = self._call('root')
        return answer.id

    def is_root(self):
        answer = self._call('is_root')
        return answer.yes

    def parent(self):
        answer = self._call('parent')
        return answer.id

    def type(self):
        answer = self._call('type')
        return answer.yes

    def set_type(self, type_value):
        answer = self._call('set_type', type=type_value)

    def create_string_parameter(self, name):
        answer = self._call('create_string_parameter', name=name)
        return answer.id

    def create_int_parameter(self, name):
        answer = self._call('create_int_parameter', name=name)
        return answer.id

    def create_double_parameter(self, name):
        answer = self._call('create_double_parameter', name=name)
        return answer.id

    def create_datetime_parameter(self, name):
        answer = self._call('create_datetime_parameter', name=name)
        return answer.id

    def create_bool_parameter(self, name):
        answer = self._call('create_bool_parameter', name=name)
        return answer.id

    def create_event(self, name):
        answer = self._call('create_event', name=name)
        return answer.id

    def create_string_command(self, name):
        answer = self._call('create_string_command', name=name)
        return answer.id

    def create_int_command(self, name):
        answer = self._call('create_int_command', name=name)
        return answer.id

    def create_double_command(self, name):
        answer = self._call('create_double_command', name=name)
        return answer.id

    def create_datetime_command(self, name):
        answer = self._call('create_datetime_command', name=name)
        return answer.id

    def create_bool_command(self, name):
        answer = self._call('create_bool_command', name=name)
        return answer.id

    def parameters(self):
        answer = self._call('parameters')
        return answer.ids

    def events(self):
        answer = self._call('events')
        return answer.ids

    def commands(self):
        answer = self._call('commands')
        return answer.ids

    def children(self):
        answer = self._call('children')
        return answer.ids

    def parameter(self, name):
        answer = self._call('parameter', name=name)
        return answer.id

    def event(self, name):
        answer = self._call('event', name=name)
        return answer.id

    def command(self, name):
        answer = self._call('command', name=name)
        return answer.id

    def is_removed(self):
        answer = self._call('is_removed')
        return answer.yes

    def register_maker(self, name):
        answer = self._call('register_maker', name=name)
        return answer.yes

    def unregister_all_makers(self):
        answer = self._call('unregister_all_makers')

    def is_connected(self):
        answer = self._call('is_connected')
        return answer.yes

    def is_error(self):
        answer = self._call('is_error')
        return answer.yes

    def is_ready_to_work(self):
        answer = self._call('is_ready_to_work')
        return answer.yes

    def state_no_connection(self, reason):
        answer = self._call('state_no_connection')

    def state_connected(self, reason):
        answer = self._call('state_connected')

    def state_error(self, reason):
        answer = self._call('state_error')

    def state_ok(self, reason):
        answer = self._call('state_ok')