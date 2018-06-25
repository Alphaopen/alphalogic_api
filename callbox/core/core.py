# -*- coding: utf-8 -*-

'''
Рассмотреть возможности:
1) Дерево уже существует  
2) Дерева не существует

Возможны варианты:
Добавить узлы к существующему состоянию
Удалить все и создавать по скрипту
Ничего не удалять подсоединиться и просто наблюдать за деревом

'''
from __future__ import unicode_literals
from callbox.core.type_attributes import runtime, setup, hidden, common
from callbox.core.type_attributes import read_only, read_write

from callbox.core.parameter import Parameter, ParameterBool, ParameterInt, \
    ParameterDouble, ParameterDatetime, ParameterString
from callbox.core.multistub import MultiStub
from callbox.core.command import (
    command,
    Command
)
import callbox.protocol.rpc_pb2 as rpc_pb2
import datetime
import inspect
import callbox.core.utils as utils

class Manager(object):
    dict_type_objects = {} #По type_when_create можно определить тип узла
    list_objects = {}  # Список всех узлов, по id узла можно обратиться в словаре к узлу
    list_commands = {} #По словарю можно обратиться к командам

    @staticmethod
    def add_object_to_list(object_id, device):
        Manager.list_objects[object_id] = device

    def __init__(self):
        pass

    def configure_multi_stub(self, address):
        self.multi_stub = MultiStub(address)

    def prepare_root_node(self, root_device, id_root, type_device_str):
        Manager.dict_type_objects[type_device_str] = type(root_device)
        Manager.add_object_to_list(id_root, root_device)

        list_parameters_name = filter(lambda attr: type(getattr(root_device, attr)) is Parameter, dir(root_device))
        for name in list_parameters_name:
            root_device.__dict__[name] = type(root_device).__dict__[name]

        list_command_name = filter(lambda attr: callable(getattr(root_device, attr)) and attr[0:2] != '__'
                                                and hasattr(getattr(root_device, attr), 'result_type'), dir(root_device))
        for name in list_command_name:
            root_device.__dict__['command_'+name] = Command(type(root_device).__dict__[name])


        self.configure_parameters(root_device, id_root)
        self.configure_commands(root_device, id_root)


    def create_object(self, object_id):
        parent_id = self.multi_stub.object_call('parent', id=object_id).id
        parent = Manager.list_objects[parent_id] if (parent_id in Manager.list_objects) else None
        id_parameter = self.multi_stub.object_call('parameter', id=object_id, name='type_when_create').id
        type_device_str = self.multi_stub.parameter_call('get', id=id_parameter).value.string_value
        Device_type = Manager.dict_type_objects[type_device_str]
        object = Device_type(parent, type_device_str, object_id)
        Manager.add_object_to_list(object_id, object)
        self.configure_parameters(object, object_id)


    def get_available_children(self, id_device):
        device = Manager.list_objects[id_device]
        available_devices = device.handle_get_available_children()
        self.multi_stub.object_call('unregister_all_makers', id = id_device) # можно будет переписать вызвав у объекта функцию unregister_makers
        for device_type, name in available_devices:
            self.multi_stub.object_call('register_maker', id=id_device, name=name)
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
        id_root = self.multi_stub.object_call('root').id
        id_parameter = self.multi_stub.object_call('parameter', id=id_root, name='type_when_create').id
        type_device_str = self.multi_stub.parameter_call('get', id=id_parameter).value.string_value
        return (id_root, type_device_str)

    def configure_parameters(self, object, object_id):
        list_parameters_name = filter(lambda attr: type(getattr(object, attr)) is Parameter, dir(object))
        for name in list_parameters_name:
            parameter = object.__dict__[name]
            parameter.set_multi_stub(self.multi_stub)
            value_type = parameter.value_type
            id_parameter = self.multi_stub.object_call(utils.create_parameter_definer(str(value_type)), 'id',
                                                       id=object_id, name=name)
            parameter.id = id_parameter

            visible_type = parameter.visible
            getattr(parameter, utils.set_visible_definer(visible_type))

            access_type = parameter.access
            getattr(parameter, utils.set_access_definer(access_type))

            values = getattr(parameter, 'value', None)
            parameter.val = values

    def configure_commands(self, object, object_id):
        list_command_name = filter(lambda attr: type(getattr(object, attr)) is Command, dir(object))
        for name in list_command_name:
            command = object.__dict__[name]
            command.set_multi_stub(self.multi_stub)
            result_type = command.result_type
            id_command = self.multi_stub.object_call(utils.create_command_definer(str(result_type)), 'id',
                                                         id=object_id, name=name)
            command.id = id_command
            for arg in command.arguments:
                name_arg = arg
                value_arg = command.arguments[arg]
                command.set_argument(name_arg, value_arg)
            self.list_commands[id_command] = command


class Device(object):
    '''
    type - ссылка на реализацию
    '''
    manager = Manager()

    def __init__(self, parent, type_device, id_device):
        self.__dict__["parent"] = parent
        self.__dict__["type_device"] = type_device
        self.__dict__["parameters"] = []
        self.__dict__["events"] = []
        self.__dict__["commands"] = []
        list_parameters_name = filter(lambda attr: type(getattr(self, attr)) is Parameter, dir(self))
        for name in list_parameters_name:
            self.__dict__[name] = type(self).__dict__[name]

        list_command_name = filter(lambda attr: callable(getattr(self, attr)) and attr[0:2] != '__'
                                                and hasattr(getattr(self, attr), 'result_type'), dir(self))
        for name in list_command_name:
            self.__dict__['command_'+name] = Command(type(self).__dict__[name])

        #Device.add_device_to_list(id_device, self)
        #if parent != None:
        #    Device.add_to_connection_diag(parent.type_device, type_device)

    def __getattr__(self, name):
        return self.__dict__[name]

    def __setattr__(self, name, value):
        if issubclass(type(value), Parameter):
            self.parameters.append(name)
            value.name = name
            self.__dict__[name] = value

        '''
        if name == "parameter":
            self.parameters.append(value)
        elif name == "event":
            self.events.append(value)
        elif name == "command":
            self.commands.append(value)
        else:
            raise Exception('{0} not found in Device'.format(name))
        '''

    def handle_get_available_children(self):
        return []


class Root(Device):
    def __init__(self, address):
        self.manager.configure_multi_stub(address)
        id_root, type_device = self.manager.root_id_and_type()
        self.manager.prepare_root_node(self, id_root, type_device)
        super(Root, self).__init__(None, type_device, id_root)


class Event(object):
    def __init__(self, name, priority, arguments=[]):
        self.name = name
        self.priority = priority
        self.arguments = arguments
        self.id = None
