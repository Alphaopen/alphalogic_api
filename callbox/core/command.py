# -*- coding: utf-8 -*-

from callbox.core.type_attributes import VisibleType, ValueType, AccessType
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub


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

