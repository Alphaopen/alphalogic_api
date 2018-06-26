# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import callbox.core.core as core

import callbox.core.core as core
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.type_attributes import runtime, setup, hidden, common
from callbox.core.type_attributes import read_only, read_write

from callbox.core.parameter import Parameter, ParameterBool, ParameterInt, \
    ParameterDouble, ParameterDatetime, ParameterString

import grpc
import datetime
import time

from protocol.rpc_pb2 import (
    Value,
    ObjectRequest,
    ParameterRequest,
    EventRequest,
    CommandRequest,
    Empty,
    AdapterStream
)
from protocol.rpc_pb2_grpc import (
    ObjectServiceStub,
    ParameterServiceStub,
    EventServiceStub,
    CommandServiceStub,
    AdapterServiceStub,
)

from core.core import (
    Root,
    Device
)

from core.command import (
    command
)

'''
Не забыть важные моменты:
1) Нужно преобразовать type_attributes в более приемлимое
   Когда создается параметр используется именнованные аргументы.
   Нужно попробовать отказать от словарей и лямбда функций в таком виде

2) Перед запуском проверять узлы адаптера и в соотвествии с этим менять свое состояние.
   Чтобы не было несогласованных состояний.

3) В параметрах, событиях
  присутсвует в описании rpc функции:

  Value value = 4; // rpc set, set_enum
  map<string, Value> enums = 5; // rpc set_enums

  необходимо вынести их обработку в один код

4) Как сделать выбор некоторых параметров по умолчанию?

'''
'''
channel = grpc.insecure_channel('localhost:42001')

stub = ParameterServiceStub(channel)
req = ParameterRequest(id = 1932174295306122652)
req.parameter.id = 1932174295306122652
r = stub.get(req)
value = r.value.string_value
print('test get', value)


stub = ObjectServiceStub(channel)
r = stub.root(ObjectRequest())
root_id = r.id
req = ObjectRequest(id=root_id)
r = stub.children(req)

child_id = r.ids[0]

obj = ObjectServiceStub(channel)

req = ObjectRequest(id=root_id, name="NewEvent")
r = obj.create_event(req)

new_event_id = r.id

req = ObjectRequest(id=child_id, name='GeneratedEvent')
r = obj.event(req)

event_id = r.id

ev_stub = EventServiceStub(channel)
req = EventRequest(id=event_id)
r = ev_stub.emit(req)
'''


class MyRoot(Root):
    name = ParameterString(value='RootNode')
    displayName = ParameterString(value='RootNode')
    noopr = ParameterString(value='noop')
    valuet = ParameterInt(value=(0, 1, 2, 3))

    def handle_create(self):
        pass

    def handle_remove(self):
        pass

    def handle_get_available_children(self):
        return [
            (Controller, 'Controller')
        ]

    @command(result_type=unicode)
    def check(self, where='here'):
        #self.relax(1, 2, 3, 4)
        return 'abc'

    @command(result_type=bool)
    def relax(self, where='room', why=42, which=(1, 2, 3), which2=({'On': True}, {'Off': False})):
        print where
        print why
        print which
        print which2
        return True

    '''
    @command(result_type=int)
    def affair(self, where):
        return 1
    '''


class Controller(Device):
    # Parameters:
    name = ParameterString(value='Controller')
    displayName = ParameterString(value='Controller')
    hostname = ParameterString(visible=setup, access=read_write, value=('1', '2'))
    mode = ParameterBool(visible=setup, value=({'On': True}, {'Off': False}))
    version = Parameter(value_type=int)
    counter = ParameterDouble(default=1.0)

    # Events:
    # simple_event = Event()
    # alarm = Event(priority=MAJOR, args=dict(where=str, when=datetime.datetime, why=int))
    '''
    @command(result_type=bool)
    def relax(self, where='room', when=datetime.datetime.now(), why=42, which=[{'On': True}, {'Off': False}]):
        return True
    '''

    def run(self):
        pass


# python loop
adapter = MyRoot("localhost:42001")
#adapter.relax(1, 2, 3, 4)
#adapter.simple_event.emit()
#adapter.event2.set_time(int(time.time()) * 1000 - 100000)
#adapter.event2.emit(where='here', why=1)

for r in adapter.manager.multi_stub.stub_adapter.states(Empty()):
    ack = r
    if r.state == AdapterStream.AFTER_CREATING_OBJECT:
        adapter.manager.create_object(r.id)
        # req = ObjectRequest(id=r.id, name='type_when_create')
        # r = root.multi_stub.stub_object.parameter(req)
        # req = ParameterRequest(id=r.id)
        # r = root.multi_stub.stub_parameter.get(req)
        # print('type_when_create:', r.value.string_value)

    elif r.state == AdapterStream.GETTING_AVAILABLE_CHILDREN:
        print "id={0}".format(r.id)
        adapter.manager.get_available_children(r.id)

    elif r.state == AdapterStream.EXECUTING_COMMAND:
        # simulate executing command
        time.sleep(1.0)
        print(AdapterStream.AdapterState.Name(r.state))
        adapter.manager.list_commands[r.id].call_function()

    adapter.manager.multi_stub.stub_adapter.ack(ack)

