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

from callbox.core.parameter import Parameter
from callbox.core.event import Event
from callbox.core.command import Command
from callbox.core.manager import Manager


class Device(object):
    """
    type - ссылка на реализацию
    """
    manager = Manager()

    def __init__(self, parent, type_device, id_device):
        #self.__dict__["parent"] = parent
        #self.__dict__["type_device"] = type_device
        #self.__dict__["parameters"] = []
        #self.__dict__["events"] = []
        self.__dict__['type'] = type_device
        self.__dict__['id'] = id_device
        self.__dict__["commands"] = {}
        list_parameters_name = filter(lambda attr: type(getattr(self, attr)) is Parameter, dir(self))
        for name in list_parameters_name:
            self.__dict__[name] = type(self).__dict__[name]

        is_callable = lambda x: callable(getattr(self, x)) and not x.startswith('_') and\
                                hasattr(getattr(self, x), 'result_type')
        list_command_name = filter(is_callable, dir(self))
        for name in list_command_name:
            self.commands[name] = Command(self, type(self).__dict__[name])

        for name in filter(lambda attr: type(getattr(self, attr)) is Event, dir(self)):
            self.__dict__[name] = type(self).__dict__[name]

    def __getattr__(self, name):
        return self.__dict__[name]

    def __setattr__(self, name, value):
        if issubclass(type(value), Parameter):
            self.parameters.append(name)
            value.name = name
            self.__dict__[name] = value

    def handle_get_available_children(self):
        return []

    def handle_before_remove_device(self):
        pass


class Root(Device):
    def __init__(self, host, port):
        self.manager.configure_multi_stub(host + ':' + str(port))
        id_root = self.manager.root()
        type_device = self.manager.get_type_when_create(id_root)
        super(Root, self).__init__(None, type_device, id_root)
        self.manager.prepare_root_node(self, id_root, type_device)

    def join(self):
        self.manager.join()



