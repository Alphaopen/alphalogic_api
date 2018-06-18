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
from callbox.core.parameter import Parameter, ParameterBool, ParameterInt64, ParameterDouble, ParameterDatetime, ParameterString
from callbox.core.multistub import MultiStub

import callbox.protocol.rpc_pb2 as rpc_pb2


class Device(object):
    '''
    type - ссылка на реализацию
    '''

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

class Root(Device):
    def __init__(self, type_device, id_device):
        super(Root, self).__init__(None, type_device, id_device)


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

'''
Попробовать сделать его абстрактным, чтобы 
нельзя было создать экземпляр
'''
class Adapter(object):
    dict_type_objects = {} #По type_when_create можно определить тип узла
    list_objects = {}  # Список всех узлов, по id узла можно обратиться в словаре к узлу

    @staticmethod
    def add_object_to_list(object_id, device):
        Adapter.list_objects[object_id] = device

    def __init__(self):
       # self.root = self.get_root()
        self.multi_stub = MultiStub("localhost:42001")

    def create_object(self, object_id):
        parent_id = self.multi_stub.object_call('parent', id=object_id).id
        parent = Adapter.list_objects[parent_id] if (parent_id in Adapter.list_objects) else None
        id_parameter = self.multi_stub.object_call('parameter', id=object_id, name='type_when_create').id
        type_device_str = self.multi_stub.parameter_call('get', id=id_parameter).value.string_value
        #Device_type = Adapter.dict_type_objects[type_device_str]
        Device_type = Controller
        object = Device_type(parent, type_device_str, object_id)
        Adapter.add_object_to_list(object_id, object)
        self.configure_parameters(object, object_id)

    '''
    def get_root(self):
        root_list = filter (lambda attr: type(getattr(self, attr)) is Root, dir(self))
        if len(root_list)<1:
            raise Exception("Not found Root device")
        elif len(root_list)>1:
            raise Exception("The number of Root device is {0}. It's too many".format(len(root_list)))
        return type(self).__dict__[root_list[0]]
    '''

    def get_available_children(self, id_device):
        available_devices = self.handle_get_available_children()
        self.multi_stub.object_call('unregister_all_makers', id = id_device)
        for device_type, name in available_devices:
            self.multi_stub.object_call('register_maker', id=id_device, name=name)
            Adapter.dict_type_objects[name] = device_type

    '''
    Конфигурирование узла по заготовленной схеме
    '''
    '''
    def configure_device_from_scheme(self, type_object, object_id):
        object = self.root.list_devices[type_object]
        self.configure_parameters(object, object_id)
    '''

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




class ExampleAdapter(Adapter):

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


class Controller(Device):
    name = ParameterString(Value='Controller')
    displayName = ParameterString(Value='Controller')
    hostname = ParameterString(VisibleType.SETUP, AccessType.READ_WRITE, Value=['1', '2'])
    mode = ParameterBool(VisibleType.SETUP, Value=[{'On': True}, {'Off': False}])
    version = Parameter(ValueType.INT64)

'''
class Root(Adapter):

    # Parameters:
    # default: read_write & runtime
    #hostname = ParameterString(visible=setup, default='localhost', callback=hostname_change)
    #mode = ParameterBool(visible=setup, default=True, choices=MODE_CHOICES)
    #version = ParameterInt64(access=read_only)

    hostname = ParameterString(VisibleType.SETUP, AccessType.READ_WRITE, Value = [1, 2])
    mode = ParameterBool(VisibleType.SETUP, Value= [{'On': True, 'Off': False}])
    version = Parameter(ValueType.INT64)


    def handle_create(self):
        pass

    def handle_remove(self):
        pass

    #def handle_get_available_children(self):
    #    return (
    #        (Controller, 'Controller')
    #    )
'''

'''
class Controller(object):
    MODE_CHOICES = (
        (True, "On"),
        (False, "Off"),
    )

    # Parameters:
    # default: read_write & runtime
    hostname = ParameterString(visible=setup, default='localhost', callback=hostname_change)
    mode = ParameterBool(visible=setup, default=True, choices=MODE_CHOICES)
    version = ParameterInt64(access=read_only)

    # Events:
    simple_event = Event()
    alarm = Event(priority=MAJOR, args=dict(where=str, when=datetime.datetime, why=int))

    # Commands:
    @command(result_type=bool)
    def relax(self, where='room', when=datetime.datetime.now(), why=42, which=MODE_CHOICES):
        return True

    def run(self):
        # call periodically
        time.sleep(1.0)
        self.alarm.emit('room', datetime.datetime.now(), 42)  # emit event
        self.version = 777

    def hostname_change(self):
        # что?
        pass
'''