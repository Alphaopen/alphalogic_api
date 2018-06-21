# -*- coding: utf-8 -*-

import callbox.core.core as core
import callbox.protocol.rpc_pb2 as rpc_pb2
import grpc
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

'''
channel = grpc.insecure_channel('localhost:42001')

stub = ParameterServiceStub(channel)
req = ParameterRequest(id=7081186749427145300)
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

#python loop
adapter = core.MyRoot("localhost:42001")

adapter.simple_event.emit()
adapter.event2.set_time(int(time.time()) * 1000 - 100000)
adapter.event2.emit(where='here', why=1)

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



