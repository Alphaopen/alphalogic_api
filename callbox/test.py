# -*- coding: utf-8 -*-
import callbox.core.core as core

import callbox.protocol.rpc_pb2 as rpc_pb2


import grpc


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

'''
channel = grpc.insecure_channel('localhost:42001')
stub = ParameterServiceStub(channel)
req = ParameterRequest(id = 1932174295306122652)
req.parameter.id = 1932174295306122652
r = stub.get(req)
value = r.value.double_value
print('test get', value)
'''

#python loop
adapter = core.MyRoot("localhost:42001")
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



