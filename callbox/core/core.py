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

from callbox.core.type_attributes import VisibleType, ValueType, AccessType
from callbox.core.parameter import Parameter, ParameterBool, ParameterInt64, \
    ParameterDouble, ParameterDatetime, ParameterString
from callbox.core.multistub import MultiStub
from callbox.core.command import command

import callbox.protocol.rpc_pb2 as rpc_pb2
import datetime
import inspect

class Manager(object):
    dict_type_objects = {} #По type_when_create можно определить тип узла
    list_objects = {}  # Список всех узлов, по id узла можно обратиться в словаре к узлу

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
            root_device.__dict__[name] = type(root_device).__dict__[name]


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
            value_type = parameter.ValueType
            id_parameter = self.multi_stub.object_call(ValueType.create_parameter[value_type], 'id',
                                                       id=object_id, name=name)
            parameter.id = id_parameter

            visible_type = parameter.VisibleType
            getattr(parameter, VisibleType.set_visible_type[visible_type])()

            access_type = parameter.AccessType
            getattr(parameter, AccessType.set_access_type[access_type])()

            values = getattr(parameter, 'Value', None)
            parameter.val = values

    def configure_commands(self, object, object_id):
        list_command_name = filter(lambda attr: callable(getattr(object, attr)) and attr[0:2]!='__'
                                                and hasattr(getattr(object, attr), 'result_type'), dir(object))
        for name in list_command_name:
            command = object.__dict__[name]
            command.multi_stub = self.multi_stub
            result_type = command.result_type
            if 'string' in str(result_type):
                id_command = self.multi_stub.object_call('create_string_command', 'id',
                                                         id=object_id, name=name)
            elif 'int' in str(result_type):
                id_command = self.multi_stub.object_call('create_int_command', 'id',
                                                         id=object_id, name=name)
            elif 'double' in str(result_type):
                id_command = self.multi_stub.object_call('create_double_command', 'id',
                                                         id=object_id, name=name)
            elif 'datetime' in str(result_type):
                id_command = self.multi_stub.object_call('create_datetime_command', 'id',
                                                         id=object_id, name=name)
            elif 'bool' in str(result_type):
                id_command = self.multi_stub.object_call('create_bool_command', 'id',
                                                         id=object_id, name=name)

            command.id = id_command
            value_rpc = rpc_pb2.Value()
            value_rpc.string_value = '1234'
            answer = self.multi_stub.command_call('set_argument', id=id_command, argument='a', value=value_rpc)


            #id_command = self.multi_stub.object_call()

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

class Command(object):
    def __init__(self, name, result_type, arguments=[]):
        self.name = name
        self.result_type = result_type
        self.arguments = arguments
        self.defaults = None  # Значения аргументов команды по умолчанию
        self.id = None




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

    def check(self):
        pass

    @command(result_type=bool)
    def relax(self, where='room', when=datetime.datetime.now(), why=42, which=[{'On': True}, {'Off': False}]):
        return True

    @command(result_type=int)
    def affair(self, where):
        return 1


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