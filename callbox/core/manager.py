# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import time
import datetime
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub
from callbox.core.parameter import Parameter
from callbox.core.event import Event
from callbox.core import utils


class AbstractManager(object):

    def _call(self, name_func, id_object, *args, **kwargs):
        return self.multi_stub.object_call(name_func, id=id_object, *args, **kwargs)

    def root(self):
        answer = self.multi_stub.object_call('root')
        return answer.id

    def is_root(self, id_object):
        answer = self._call('is_root', id_object)
        return answer.yes

    def parent(self, id_object):
        answer = self._call('parent', id_object)
        return answer.id

    def type(self, id_object):
        answer = self._call('type', id_object)
        return answer.yes

    def set_type(self, id_object, type_value):
        answer = self._call('set_type', id_object, type=type_value)

    def create_string_parameter(self, id_object, name):
        answer = self._call('create_string_parameter', id_object, name=name)
        return answer.id

    def create_int_parameter(self, id_object, name):
        answer = self._call('create_int_parameter', id_object, name=name)
        return answer.id

    def create_double_parameter(self, id_object, name):
        answer = self._call('create_double_parameter', id_object, name=name)
        return answer.id

    def create_datetime_parameter(self, id_object, name):
        answer = self._call('create_datetime_parameter', id_object, name=name)
        return answer.id

    def create_bool_parameter(self, id_object, name):
        answer = self._call('create_bool_parameter', id_object, name=name)
        return answer.id

    def create_event(self, id_object, name):
        answer = self._call('create_event', id_object, name=name)
        return answer.id

    def create_string_command(self, id_object, name):
        answer = self._call('create_string_command', id_object, name=name)
        return answer.id

    def create_int_command(self, id_object, name):
        answer = self._call('create_int_command', id_object, name=name)
        return answer.id

    def create_double_command(self, id_object, name):
        answer = self._call('create_double_command', id_object, name=name)
        return answer.id

    def create_datetime_command(self, id_object, name):
        answer = self._call('create_datetime_command', id_object, name=name)
        return answer.id

    def create_bool_command(self, id_object, name):
        answer = self._call('create_bool_command', id_object, name=name)
        return answer.id

    def parameters(self, id_object):
        answer = self._call('parameters', id_object)
        return answer.ids

    def events(self, id_object):
        answer = self._call('events', id_object)
        return answer.ids

    def commands(self, id_object):
        answer = self._call('commands', id_object)
        return answer.ids

    def children(self, id_object):
        answer = self._call('children', id_object)
        return answer.ids

    def parameter(self, id_object, name):
        answer = self._call('parameter', id_object, name=name)
        return answer.id

    def event(self, id_object, name):
        answer = self._call('event', id_object, name=name)
        return answer.id

    def command(self, id_object, name):
        answer = self._call('command', id_object, name=name)
        return answer.id

    def is_removed(self, id_object):
        answer = self._call('is_removed', id_object)
        return answer.yes

    def register_maker(self, id_object, name):
        answer = self._call('register_maker', id_object, name=name)
        return answer.yes

    def unregister_all_makers(self, id_object):
        answer = self._call('unregister_all_makers', id_object)

    def is_connected(self, id_object):
        answer = self._call('is_connected', id_object)
        return answer.yes

    def is_error(self, id_object):
        answer = self._call('is_error', id_object)
        return answer.yes

    def is_ready_to_work(self, id_object):
        answer = self._call('is_ready_to_work', id_object)
        return answer.yes

    def state_no_connection(self, id_object, reason):
        answer = self._call('state_no_connection', id_object)

    def state_connected(self, id_object, reason):
        answer = self._call('state_connected', id_object)

    def state_error(self, id_object, reason):
        answer = self._call('state_error', id_object)

    def state_ok(self, id_object, reason):
        answer = self._call('state_ok', id_object)


class Manager(AbstractManager):
    dict_type_objects = {} #По type_when_create можно определить тип узла
    list_objects = {}  # Список всех узлов, по id узла можно обратиться в словаре к узлу
    components = {} #По id команды можно обратиться к командам

    def __init__(self):
        pass

    def configure_multi_stub(self, address):
        self.multi_stub = MultiStub(address)

    def prepare_root_node(self, root_device, id_root, type_device_str):
        Manager.dict_type_objects[type_device_str] = type(root_device)
        Manager.list_objects[id_root] = root_device

        self.configure_parameters(root_device, id_root)
        self.configure_commands(root_device, id_root)
        self.configure_events(root_device, id_root)

    def create_object(self, object_id):
        parent_id = self.parent(object_id)
        parent = Manager.list_objects[parent_id] if (parent_id in Manager.list_objects) else None
        id_parameter = self.parameter(object_id, name='type_when_create')
        type_device_str = self.multi_stub.parameter_call('get', id=id_parameter).value.string_value
        Device_type = Manager.dict_type_objects[type_device_str]
        object = Device_type(parent, type_device_str, object_id)
        Manager.list_objects[object_id] = object
        self.configure_parameters(object, object_id)

    def get_available_children(self, id_device):
        device = Manager.list_objects[id_device]
        available_devices = device.handle_get_available_children()
        self.unregister_all_makers(id_object=id_device) # можно будет переписать вызвав у объекта функцию unregister_makers
        for device_type, name in available_devices:
            self.register_maker(id_object=id_device, name=name)
            Manager.dict_type_objects[name] = device_type

    '''
    Конфигурирование узла по заготовленной схеме
    '''
    '''
    def configure_device_from_scheme(self, type_object, object_id):
        object = self.root.list_devices[type_object]
        self.configure_parameters(object, object_id)
    '''
    def root_id_and_type(self):
        id_root = self.root()
        id_parameter = self.parameter(id_object=id_root, name='type_when_create')
        type_device_str = self.multi_stub.parameter_call('get', id=id_parameter).value.string_value
        return id_root, type_device_str

    def configure_parameters(self, object, object_id):
        list_parameters_name = filter(lambda attr: type(getattr(object, attr)) is Parameter, dir(object))
        for name in list_parameters_name:
            parameter = object.__dict__[name]
            parameter.set_multi_stub(self.multi_stub)
            value_type = parameter.value_type
            id_parameter = getattr(self, utils.create_parameter_definer(str(value_type)))\
                (id_object=object_id, name=name)
            parameter.id = id_parameter

            getattr(parameter, parameter.visible.create_func)()
            getattr(parameter, parameter.access.create_func)()

            parameter.val = getattr(parameter, 'value', None)

    def configure_commands(self, object, object_id):
        for name in object.commands:
            command = object.commands[name]
            command.set_multi_stub(self.multi_stub)
            result_type = command.result_type
            id_command = getattr(self, utils.create_command_definer(str(result_type)))\
                (id_object=object_id, name=name)
            command.id = id_command
            for arg in command.arguments:
                name_arg = arg
                value_arg = command.arguments[arg]
                command.set_argument(name_arg, value_arg)
            self.components[id_command] = command

    def configure_events(self, object, object_id):
        list_events = filter(lambda attr: type(getattr(object, attr)) is Event, dir(object))
        for name in list_events:
            event = object.__dict__[name]
            event.set_multi_stub(self.multi_stub)

            event.id = self.create_event(id_object=object_id, name=name)

            getattr(event, event.priority.create_func)()
            event.clear()

            for key, val in event.args.iteritems():
                event.set_argument(key, utils.get_rpc_value(val))

    def join(self):
        for r in self.multi_stub.stub_adapter.states(rpc_pb2.Empty()):
            ack = r
            if r.state == rpc_pb2.AdapterStream.AFTER_CREATING_OBJECT:
                self.create_object(r.id)
                # req = ObjectRequest(id=r.id, name='type_when_create')
                # r = root.multi_stub.stub_object.parameter(req)
                # req = ParameterRequest(id=r.id)
                # r = root.multi_stub.stub_parameter.get(req)
                # print('type_when_create:', r.value.string_value)
            elif r.state == rpc_pb2.AdapterStream.BEFORE_REMOVING_OBJECT:
                if r.id in self.list_objects:
                    self.list_objects[r.id].handle_before_remove_device()
                    del self.list_objects[r.id]
                    # TODO удалить компоненты из self.components

            elif r.state == rpc_pb2.AdapterStream.GETTING_AVAILABLE_CHILDREN:
                self.get_available_children(r.id)

            elif r.state == rpc_pb2.AdapterStream.AFTER_SETTING_PARAMETER:
                self.components[r.id].callback()

            elif r.state == rpc_pb2.AdapterStream.EXECUTING_COMMAND:
                # simulate executing command
                #time.sleep(1.0)
                #print(rpc_pb2.AdapterStream.AdapterState.Name(r.state))
                self.components[r.id].call_function()

            self.multi_stub.stub_adapter.ack(ack)

