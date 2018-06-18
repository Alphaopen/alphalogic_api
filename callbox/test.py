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
adapter = core.ExampleAdapter()

for r in adapter.multi_stub.stub_adapter.states(Empty()):
    if r.state == AdapterStream.AFTER_CREATING_OBJECT:
        adapter.create_object(r.id)
        #req = ObjectRequest(id=r.id, name='type_when_create')
        #r = root.multi_stub.stub_object.parameter(req)
        #req = ParameterRequest(id=r.id)
        #r = root.multi_stub.stub_parameter.get(req)
        #print('type_when_create:', r.value.string_value)

    elif r.state == AdapterStream.GETTING_AVAILABLE_CHILDREN:
        print "id={0}".format(r.id)
        adapter.get_available_children(r.id)







d = core.Device(None, "type23")

#core.Api.initialization()
root = core.ExampleAdapter()
id_root = root.multi_stub.object_call('root', 'id')
root.configure_device_from_scheme("healhAdapterRoot", id_root)

root.check()
'''
object_rpc = rpc_pb2.Object(id = id_root)
req = rpc_pb2.ObjectRequest(object = object_rpc)
r = root.multi_stub.stub_object.create_int_parameter(req)
'''

a=2


