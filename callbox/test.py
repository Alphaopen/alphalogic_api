# -*- coding: utf-8 -*-
import callbox.core.core as core

import callbox.protocol.rpc_pb2 as rpc_pb2

d = core.Device(None, "type23")

#core.Api.initialization()
root = core.ExampleAdapter("192.168.50.23:42001", "ExampleAdapter")
id_root = root.multi_stub.object_call('root', 'object', 'id')
root.configure_device_from_scheme("healhAdapterRoot", id_root)

'''
object_rpc = rpc_pb2.Object(id = id_root)
req = rpc_pb2.ObjectRequest(object = object_rpc)
r = root.multi_stub.stub_object.create_int_parameter(req)
'''

a=2


