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

from callbox.core.enums import VisibleType, ValueType, AccessType, UserType, EventPriority
from callbox.core.multistub import MultiStub


'''
class Root(object):

    def __init__(self, target, name):
        self.api = Api(target)
        self.id = self.api.object_call('root', 'id')
        print self.id
        print self.api.object_call('is_root', 'yes')
'''

class Component(object):
    '''
    type - ссылка на реализацию
    '''
    scheme = {}
    @staticmethod
    def add_device_to_scheme(type_device, device):
        Component.scheme[type_device] = device


class Device(Component):
    def __init__(self, parent, type_device):
        self.__dict__["parent"] = parent
        self.__dict__["type_device"] = type_device
        self.__dict__["parameters"] = []
        self.__dict__["events"] = []
        self.__dict__["commands"] = []
        Component.add_device_to_scheme(self.__dict__["type_device"], self)

    def __getattr__(self, name):
        pass

    def __setattr__(self, name, value):
        if name == "parameter":
            self.parameters.append(value)
        elif name == "event":
            self.events.append(value)
        elif name == "command":
            self.commands.append(value)
        else:
            raise Exception('{0} not found in Device'.format(name))


class Root(Device):
    def __init__(self, type_device):
        super(Root, self).__init__(None, type_device)

class Parameter(Component):
    def __init__(self, name, **kwargs):
        self.name = name
        self.value_type = kwargs.get("value_type", None)
        self.licensed = kwargs.get("licensed", None)
        self.visible = kwargs.get("visible", None)
        self.access = kwargs.get("access", None)
        self.user_type = kwargs.get("user_type", None)
        self.enums = kwargs.get("enums", None)
        self.value = None
        self.id = None

class Event(Component):
    def __init__(self, name, priority, arguments=[]):
        self.name = name
        self.priority = priority
        self.arguments = arguments
        self.id = None

class Command(Component):
    def __init__(self, name, result_type, arguments=[]):
        self.name = name
        self.result_type = result_type
        self.arguments = arguments
        self.defaults = None  # Значения аргументов команды по умолчанию
        self.id = None

class ExampleAdapter(object):
    '''
    Общая схема адаптера
    '''

    root = Root("type")
    d1 = Device(root, "type1")
    d2 = Device(root, "type2")
    d1.parameter = Parameter("name1", value_type=ValueType.INT64, visible=VisibleType.HIDDEN, access=AccessType.READ_ONLY)
    d1.parameter = Parameter("name2", value_type=ValueType.STRING, visible=VisibleType.HIDDEN, access=AccessType.READ_ONLY)
    d2.parameter = Parameter("name3", value_type=ValueType.DOUBLE, visible=VisibleType.HIDDEN, access=AccessType.READ_ONLY)
    #d2.event = Event("name", priority=EventPriority.MAJOR)
    #d1.command = Command("name", result_type=ValueType.BOOL, arguments=[("chat_id", ValueType.INT64)])
    print "fellah"
    #d2.package = PackageDiagnostic()

    '''
    def scheme():
        root = Root("type")
        d1 = Device(parenr=root, "type1")
        d2 = Device(parent=root, "type2")
        d3 = Device(parent=d1, "type3")
        par = d1.Parameter("")
    '''

    '''
    def __init__(self, target, name):
        root = Root(target, name)
        d1 = Device(root, "node 1")
        #d2 = Device(parenr=r, "node 2")
    '''

    #r = Root("ip:port", "Name node")
    #d = Device(parent=r)
    # Сделать обязательным что-то одно либо type, либо #value
    # Можно опредлять тип из value 
    #p = Parameter(parent=d, "name", type, value, visible_type, access_type, display_name)
    #c = Command(parent=d)
    #e = Event(parent=e)

