# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import time
import sys
from threading import Lock, Thread
from alphalogic_api.objects.event import Event
from alphalogic_api.objects.command import Command
from alphalogic_api.objects.parameter import Parameter, ParameterString, ParameterBool, ParameterInt
from alphalogic_api.attributes import Visible, Access
from alphalogic_api.manager import Manager
from alphalogic_api.logger import log
from alphalogic_api.utils import Exit, decode_string
from alphalogic_api.tasks_pool import TasksPool
from alphalogic_api.exceptions import exception_info


class Device(object):
    """
    Node with parameters, commands, events and run functions.
    Parameters, commands, events can't be with same name.
    """
    manager = Manager()

    name = ParameterString(visible=Visible.setup, access=Access.read_only)
    displayName = ParameterString(visible=Visible.setup, access=Access.read_write)
    desc = ParameterString(visible=Visible.setup, access=Access.read_write)
    type_when_create = ParameterString(visible=Visible.hidden, access=Access.read_only)
    isService = ParameterBool(visible=Visible.common, access=Access.read_write)
    connected = ParameterBool(visible=Visible.common, access=Access.read_only)
    ready_to_work = ParameterBool(visible=Visible.common, access=Access.read_only)
    error = ParameterBool(visible=Visible.common, access=Access.read_only)
    number_of_errors = ParameterInt(visible=Visible.setup, access=Access.read_write)
    status = ParameterString(visible=Visible.common, access=Access.read_only)

    def __init__(self, type_device, id_device):
        self.__dict__['log'] = log
        self.__dict__['type'] = type_device
        self.__dict__['id'] = id_device
        self.__dict__['flag_removing'] = False
        self.__dict__['mutex'] = Lock()

        # Parameters
        list_parameters_name = filter(lambda attr: type(getattr(self, attr)) is Parameter, dir(self))
        for name in list_parameters_name:
            if name in type(self).__dict__:
                self.__dict__[name] = type(self).__dict__[name]
            elif name in Device.__dict__:
                self.__dict__[name] = Device.__dict__[name]
            elif name in Root.__dict__:
                self.__dict__[name] = Root.__dict__[name]

        # Commands
        is_callable = lambda x: callable(getattr(self, x)) and not x.startswith('_') and\
                                hasattr(getattr(self, x), 'result_type')
        list_command_name = filter(is_callable, dir(self))
        for name in list_command_name:
            self.__dict__[name] = Command(self, type(self).__dict__[name])

        # Events
        for name in filter(lambda attr: type(getattr(self, attr)) is Event, dir(self)):
            self.__dict__[name] = type(self).__dict__[name]

        # Run functions
        is_runnable = lambda x: callable(getattr(self, x)) and not x.startswith('_') and\
                                hasattr(getattr(self, x), 'runnable')
        self.__dict__['run_function_names'] = filter(is_runnable, dir(self))

    def parameters(self):
        return self.manager.get_components(self.id, 'parameters')

    def events(self):
        return self.manager.get_components(self.id, 'events')

    def commands(self):
        return self.manager.get_components(self.id, 'commands')

    def parameter(self, name):
        return self.manager.get_component_by_name(name, self.id, 'parameter')

    def event(self, name):
        return self.manager.get_component_by_name(name, self.id, 'event')

    def command(self, name):
        return self.manager.get_component_by_name(name, self.id, 'command')

    def parent(self):
        return self.manager.parent(self.id)

    def root(self):
        return self.manager.root()

    def children(self):
        return self.manager.children(self.id)


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
    version = ParameterString(visible=Visible.setup, access=Access.read_only)

    def __init__(self, host, port):
        try:
            self.manager.start_threads()
            self.joinable = False
            self.manager.configure_multi_stub(host + ':' + str(port))
            id_root = self.manager.root_id()
            type_device = self.manager.get_type(id_root)
            super(Root, self).__init__(type_device, id_root)
            self.log.info('Connecting to ' + host + ':' + unicode(port))
            self.init(id_root)
            self.joinable = True
            self.log.info('Root connected OK')

        except Exception, err:
            exception_info()
            log.error(decode_string(err))
            self.manager.tasks_pool.stop_operation_thread()
            sys.exit(2)

    def init(self, id_root):
        list_id_device_exist = []
        self.manager.get_all_device(id_root, list_id_device_exist)
        list_need_to_delete = set(Manager.nodes.keys()) - set(list_id_device_exist)
        map(self.manager.delete_object, list_need_to_delete)
        Manager.components_for_device[id_root] = []
        self.manager.prepare_for_work(self, id_root)
        self.manager.prepare_existing_devices(id_root)

    def join(self):
        if self.joinable:
            is_connected = True
            while True:
                try:
                    if is_connected:
                        self.manager.join()
                        is_connected = False
                        self.manager.tasks_pool.stop_operation_thread()
                        self.manager.g_thread.join()
                        self.manager.g_thread = Thread(target=self.manager.grpc_thread)
                        self.manager.tasks_pool = TasksPool()
                    time.sleep(1)
                    id_root = self.manager.root_id()
                    self.init(id_root)
                    is_connected = True
                except Exit:
                    self.manager.tasks_pool.stop_operation_thread()
                    self.manager.multi_stub.channel.close()
                    if self.manager.g_thread.is_alive():
                        self.manager.g_thread.join()
                    break
                except Exception, err:
                    log.error(decode_string(err))

