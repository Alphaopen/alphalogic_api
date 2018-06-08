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


'''
class Root(object):

    def __init__(self, target, name):
        self.api = Api(target)
        self.id = self.api.object_call('root', 'id')
        print self.id
        print self.api.object_call('is_root', 'yes')
'''


class Device(object):
    '''
    type - ссылка на реализацию
    '''
    list_devices = {}  # Список всех узлов, по типу узла можно обратиться в словаре к модели узла
    connection_diag = {}  # Описывает связи между узлами

    @staticmethod
    def add_device_to_list(type_device, device):
        Device.list_devices[type_device] = device

    @staticmethod
    def add_to_connection_diag(parent_type, type_device):
        if parent_type in Device.connection_diag:
            Device.connection_diag[parent_type].append(type_device)
        else:
            Device.connection_diag[parent_type] = [type_device]

    def __init__(self, parent, type_device):
        self.__dict__["parent"] = parent
        self.__dict__["type_device"] = type_device
        self.__dict__["parameters"] = []
        self.__dict__["events"] = []
        self.__dict__["commands"] = []
        Device.add_device_to_list(type_device, self)
        if parent != None:
            Device.add_to_connection_diag(parent.type_device, type_device)

    def __getattr__(self, name):
        pass

    def __setattr__(self, name, value):
        if issubclass(type(value), Parameter):
            self.parameters.append(name)
            value.name = name
            value.__class__ = Parameter # ParameterBool, ParameterInt64 - просто обертка. Все данные храняться в Parameter
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
    def __init__(self, type_device):
        super(Root, self).__init__(None, type_device)


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

    def __init__(self):
        self.root = self.get_root()

    def get_root(self):
        root_list = filter (lambda attr: type(getattr(self, attr)) is Root, dir(self))
        if len(root_list)<1:
            raise Exception("Not found Root device")
        elif len(root_list)>1:
            raise Exception("The number of Root device is {0}. It's too many".format(len(root_list)))
        return type(self).__dict__[root_list[0]]


    def get_available_children(self, connection_diag, type_device):
        #unregister_all_maker(device_id) - вызов api
        print "unregister_all_maker"
        for tmp_type in connection_diag[type_device]:
            print "tmp_type=", tmp_type
            #register_maker(tmp_type)

    #def after_creating_object(self, type_device, ):

    '''
    Конфигурирование узла по заготовленной схеме
    '''
    def configure_device_from_scheme(self, type_object, object_id):
        object = self.root.list_devices[type_object]
        parameters_name = filter (lambda attr: type(getattr(object, attr)) is Parameter, dir(object))
        '''
        for name in parameters_name:
            object.__dict__[name]
        '''


class ExampleAdapter(Adapter):
    '''
    Общая схема адаптера
    '''

    root = Root("type")
    d1 = Device(root, "type1")
    d2 = Device(root, "type2")
    '''
    Можно передавать имя параметра в аргументах Parameter("name1", ...)
    Можно передавать имя параметра в  
    '''
    d1.name3 = ParameterInt64(Value=3)
    d1.name1 = Parameter(ValueType.INT64, VisibleType.HIDDEN, AccessType.READ_ONLY)
    d1.name2 = Parameter(ValueType.INT64)
    #d1.parameter = Parameter("name1", value_type=ValueType.INT64, visible=VisibleType.HIDDEN, access=AccessType.READ_ONLY)
    #d1.parameter = Parameter("name2", value_type=ValueType.STRING, visible=VisibleType.HIDDEN, access=AccessType.READ_ONLY)
    #d2.parameter = Parameter("name3", value_type=ValueType.DOUBLE, visible=VisibleType.HIDDEN, access=AccessType.READ_ONLY)
    #d2.event = Event("name", priority=EventPriority.MAJOR)
    #d1.command = Command("name", result_type=ValueType.BOOL, arguments=[("chat_id", ValueType.INT64)])
    #d2.package = PackageDiagnostic()

    '''
    def scheme():
        root = Root("type")
        d1 = Device(parenr=root, "type1")
        d2 = Device(parent=root, "type2")
        d3 = Device(parent=d1, "type3")
        par = d1.Parameter("")
    '''


    def __init__(self, target, name):
        super(ExampleAdapter, self).__init__()
        #self.get_available_children(Component.connection_diag, "type")
        #root = Root(target, name)
        #d1 = Device(root, "node 1")
        #d2 = Device(parenr=r, "node 2")



    #r = Root("ip:port", "Name node")
    #d = Device(parent=r)
    # Сделать обязательным что-то одно либо type, либо #value
    # Можно опредлять тип из value 
    #p = Parameter(parent=d, "name", type, value, visible_type, access_type, display_name)
    #c = Command(parent=d)
    #e = Event(parent=e)

