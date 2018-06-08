# -*- coding: utf-8 -*-
import callbox.core.core as core


d = core.Device(None, "type23")

#core.Api.initialization()
root = core.ExampleAdapter("127.0.0.1:42001", "ExampleAdapter")
root.configure_device_from_scheme("type1", 1234)


a=2


