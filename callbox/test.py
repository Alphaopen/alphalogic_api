# -*- coding: utf-8 -*-
import callbox.core.core as core

import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.type_attributes import VisibleType, ValueType, AccessType
from callbox.core.parameter import Parameter, ParameterBool, ParameterInt64, \
    ParameterDouble, ParameterDatetime, ParameterString

import grpc
import datetime

from protocol.rpc_pb2 import (
    Value,
    ObjectRequest,
    ParameterRequest,
    EventRequest,
    CommandRequest,
    Empty,
    AdapterStream
)
from  protocol.rpc_pb2_grpc import (
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
value = r.value.double_value
print('test get', value)
'''

class MyRoot(Root):
    name = ParameterString(Value='RootNode')
    displayName = ParameterString(Value='RootNode')
    noopr = ParameterString(Value='noop')
    valuet = ParameterInt64(Value=[0,1,2,3])

    def handle_create(self):
        pass

    def handle_remove(self):
        pass

    def handle_get_available_children(self):
        return [
            (Controller, 'Controller')
        ]

    def check(self, where='here'):
        pass

    @command(result_type=str)
    def relax(self, where='room', when=datetime.datetime.now(), why=42, which=[{'On': True}, {'Off': False}]):
        return True
    '''
    @command(result_type=int)
    def affair(self, where):
        return 1
    '''

class Controller(Device):
    #Parameters:
    name = ParameterString(Value='Controller')
    displayName = ParameterString(Value='Controller')
    hostname = ParameterString(VisibleType.SETUP, AccessType.READ_WRITE, Value=['1', '2'])
    mode = ParameterBool(VisibleType.SETUP, Value=[{'On': True}, {'Off': False}])
    version = Parameter(ValueType.INT64)
    counter = ParameterDouble(Value=1.0)

    #Events:
    #simple_event = Event()
    #alarm = Event(priority=MAJOR, args=dict(where=str, when=datetime.datetime, why=int))
    '''
    @command(result_type=bool)
    def relax(self, where='room', when=datetime.datetime.now(), why=42, which=[{'On': True}, {'Off': False}]):
        return True
    '''

    def run(self):
        pass

#python loop
adapter = MyRoot("localhost:42001")
adapter.relax(1, 2)

for r in adapter.manager.multi_stub.stub_adapter.states(Empty()):
    if r.state == AdapterStream.AFTER_CREATING_OBJECT:
        adapter.manager.create_object(r.id)
        #req = ObjectRequest(id=r.id, name='type_when_create')
        #r = root.multi_stub.stub_object.parameter(req)
        #req = ParameterRequest(id=r.id)
        #r = root.multi_stub.stub_parameter.get(req)
        #print('type_when_create:', r.value.string_value)

    elif r.state == AdapterStream.GETTING_AVAILABLE_CHILDREN:
        print "id={0}".format(r.id)
        adapter.manager.get_available_children(r.id)



