# -*- coding: utf-8 -*-
import callbox.core.core as core

import callbox.protocol.rpc_pb2 as rpc_pb2


import grpc


from protocol.rpc_pb2 import (
    Value,
    ObjectRequest,
    ParameterRequest,
    EventRequest,
    CommandRequest
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


d = core.Device(None, "type23")

#core.Api.initialization()
root = core.ExampleAdapter("192.168.50.23:42001", "ExampleAdapter")
id_root = root.multi_stub.object_call('root', 'id')
root.configure_device_from_scheme("healhAdapterRoot", id_root)

root.check()
'''
object_rpc = rpc_pb2.Object(id = id_root)
req = rpc_pb2.ObjectRequest(object = object_rpc)
r = root.multi_stub.stub_object.create_int_parameter(req)
'''

a=2


