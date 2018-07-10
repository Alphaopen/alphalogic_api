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

from callbox.core.parameter import Parameter, ParameterString, ParameterBool, ParameterInt
from callbox.core.type_attributes import runtime, setup, hidden, common
from callbox.core.type_attributes import read_only, read_write
from callbox.core.event import Event
from callbox.core.command import Command
from callbox.core.manager import Manager
from callbox.logger import log

class Device(object):
    """
    type - ссылка на реализацию
    """
    manager = Manager()

    def __init__(self, type_device, id_device):
        self.__dict__['log'] = log
        self.__dict__['type'] = type_device
        self.__dict__['id'] = id_device
        self.__dict__["commands"] = {}

        #Параметры
        list_parameters_name = filter(lambda attr: type(getattr(self, attr)) is Parameter, dir(self))
        for name in list_parameters_name:
            self.__dict__[name] = type(self).__dict__[name] if name in type(self).__dict__ else Device.__dict__[name]

        #Команды
        is_callable = lambda x: callable(getattr(self, x)) and not x.startswith('_') and\
                                hasattr(getattr(self, x), 'result_type')
        list_command_name = filter(is_callable, dir(self))
        for name in list_command_name:
            self.commands[name] = Command(self, type(self).__dict__[name])

        #События
        for name in filter(lambda attr: type(getattr(self, attr)) is Event, dir(self)):
            self.__dict__[name] = type(self).__dict__[name]

        #run функции
        is_runnable = lambda x: callable(getattr(self, x)) and not x.startswith('_') and\
                                hasattr(getattr(self, x), 'runnable')
        self.__dict__['run_function_names'] = filter(is_runnable, dir(self))

    @classmethod
    def create_default_parameters(cls):
        cls.name = ParameterString(visible=setup, access=read_only)
        cls.displayName = ParameterString(visible=setup, access=read_write)
        cls.desc = ParameterString(visible=setup, access=read_write)
        cls.type_when_create = ParameterString(visible=hidden, access=read_write)
        cls.isService = ParameterBool(visible=common, access=read_write)
        cls.version = ParameterString(visible=setup, access=read_only)
        cls.connected = ParameterBool(visible=common, access=read_write)
        cls.ready_to_work = ParameterBool(visible=common, access=read_write)
        cls.error = ParameterBool(visible=common, access=read_write)
        cls.number_of_errors = ParameterInt(visible=setup, access=read_write)
        cls.status = ParameterString(visible=common, access=read_write)

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
        type_device = self.manager.get_type(id_root)
        super(Root, self).__init__(type_device, id_root)
        Manager.components_for_device[id_root] = []
        self.manager.prepare_for_work(self, id_root)
        self.manager.prepare_existing_devices(id_root)

    def join(self):
        self.manager.join()


print "Device default values"
Device.create_default_parameters()
