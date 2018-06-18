# -*- coding: utf-8 -*-

import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub

class AbstractObject(object):
    def root(self):
        answer = self.multi_stub.object_call('id', id=self.id)
        return answer.id

    def is_root(self):
        answer = self.multi_stub.object_call('is_root', id=self.id)
        return answer.yes

    def parent(self):
        answer = self.multi_stub.object_call('parent', id=self.id)
        return answer.id

    def type(self):
        answer = self.multi_stub.object_call('type', id=self.id)
        return answer.yes

    def set_type(self):
        pass

    def create_string_parameter(self):
        pass

    def create_int_parameter(self):
        pass

    def create_double_parameter(self):
        pass

    def create_datetime_parameter(self):
        pass

    def create_bool_parameter(self):
        pass

    def event(self):
        pass

    def create_string_command(self):
        pass

    def create_int_command(self):
        pass

    def create_double_command(self):
        pass

    def create_datetime_command(self):
        pass

    def create_bool_command(self):
        pass

    def parameters(self):
        pass

    def events(self):
        pass

    def commands(self):
        pass

    def children(self):
        pass

    def parameter(self, ):
        answer = self.multi_stub.object_call('parameter', id=self.id, name='type_when_create')
        return answer.id

    def event(self):
        pass

    def command(self):
        pass

    def is_removed(self):
        pass

    def register_maker(self):
        pass

    def unregister_all_makers(self):
        pass

    def is_connected(self):
        pass

    def is_error(self):
        pass

    def is_ready_to_work(self):
        pass

    def state_no_connection(self):
        pass

    def state_connected(self):
        pass

    def state_error(self):
        pass

    def state_ok(self):
        pass
