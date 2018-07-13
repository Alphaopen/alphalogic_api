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
from threading import Lock
from callbox.core.parameter import Parameter, ParameterString, ParameterBool, ParameterInt
from callbox.core.type_attributes import Visible, Access
from callbox.core.event import Event
from callbox.core.command import Command
from callbox.core.manager import Manager
from callbox.logger import log

class Device(object):
    """
    type - ссылка на реализацию
    """
    manager = Manager()

    name = ParameterString(visible=Visible.setup, access=Access.read_only)
    displayName = ParameterString(visible=Visible.setup, access=Access.read_write)
    desc = ParameterString(visible=Visible.setup, access=Access.read_write)
    type_when_create = ParameterString(visible=Visible.hidden, access=Access.read_write)
    isService = ParameterBool(visible=Visible.common, access=Access.read_write)
    version = ParameterString(visible=Visible.setup, access=Access.read_only)
    connected = ParameterBool(visible=Visible.common, access=Access.read_write)
    ready_to_work = ParameterBool(visible=Visible.common, access=Access.read_write)
    error = ParameterBool(visible=Visible.common, access=Access.read_write)
    number_of_errors = ParameterInt(visible=Visible.setup, access=Access.read_write)
    status = ParameterString(visible=Visible.common, access=Access.read_write)

    def __init__(self, type_device, id_device):
        self.__dict__['log'] = log
        self.__dict__['type'] = type_device
        self.__dict__['id'] = id_device
        self.__dict__['commands'] = {}
        self.__dict__['flag_removing'] = False
        self.__dict__['mutex'] = Lock()

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

    '''
    def __getattr__(self, name):
        return self.__dict__[name]

    def __setattr__(self, name, value):
        if issubclass(type(value), Parameter):
            self.parameters.append(name)
            value.name = name
            self.__dict__[name] = value
    '''
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

