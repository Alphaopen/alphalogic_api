# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import signal
import time
from threading import Thread
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.multistub import MultiStub
from callbox.core.parameter import Parameter
from callbox.core.event import Event
from callbox.core import utils
from callbox.logger import log
from callbox.core.tasks_pool import TasksPool
from callbox.core.parameter import ParameterDouble
from callbox.core.type_attributes import setup
from callbox.core.utils import Exit, shutdown


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
        self._call('unregister_all_makers', id_object)

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
        self._call('state_no_connection', id_object, reason=reason)

    def state_connected(self, id_object, reason):
        self._call('state_connected', id_object, reason=reason)

    def state_error(self, id_object, reason):
        self._call('state_error', id_object, reason=reason)

    def state_ok(self, id_object, reason):
        self._call('state_ok', id_object, reason=reason)


class Manager(AbstractManager):
    dict_type_objects = {}  # По type_when_create можно определить тип узла
    nodes = {}  # Список всех узлов, по id узла можно обратиться в словаре к узлу
    components = {} #По id команды можно обратиться к командам

    def __init__(self):
        signal.signal(signal.SIGTERM, shutdown)
        signal.signal(signal.SIGINT, shutdown)
        self.tasks_pool = TasksPool()

    def configure_multi_stub(self, address):
        self.multi_stub = MultiStub(address)

    def update_dict_type_objects(self, list_types):
        if len(list_types) > 0:
            for class_name, type_str in list_types:
                if not(type_str in Manager.dict_type_objects):
                    Manager.dict_type_objects[type_str] = class_name

    def prepare_for_work(self, object, id):
        list_id_parameters_already_exists = self.parameters(id)
        self.configure_parameters(object, id, list_id_parameters_already_exists)
        self.configure_commands(object, id)
        self.configure_events(object, id)
        self.configure_run_function(object, id, list_id_parameters_already_exists)

    def prepare_root_node(self, root_device, id_root, type_device_str):
        Manager.nodes[id_root] = root_device
        self.prepare_for_work(root_device, id_root)

    def create_object(self, object_id):
        parent_id = self.parent(object_id)
        parent = Manager.nodes[parent_id] if (parent_id in Manager.nodes) else None
        type_when_create = self.get_type_when_create(object_id)
        class_name = Manager.dict_type_objects[type_when_create]
        object = class_name(parent, type_when_create, object_id)
        Manager.nodes[object_id] = object
        self.prepare_for_work(object, object_id)

    def get_available_children(self, id_device):
        device = Manager.nodes[id_device]
        available_devices = device.handle_get_available_children()
        self.unregister_all_makers(id_object=id_device)

        for class_name, type_when_create in available_devices:
            self.register_maker(id_object=id_device, name=type_when_create)

    def get_type_when_create(self, node_id):
        id = self.parameter(id_object=node_id, name='type_when_create')
        answer = self.multi_stub.parameter_call('get', id=id)
        return utils.value_from_rpc(answer.value, unicode)

    def create_parameter(self, name, parameter, object_id, list_id_parameters_already_exists):
        parameter.set_multi_stub(self.multi_stub)
        value_type = parameter.value_type
        id_parameter = getattr(self, utils.create_parameter_definer(str(value_type))) \
            (id_object=object_id, name=name)
        parameter.id = id_parameter
        getattr(parameter, parameter.visible.create_func)()
        getattr(parameter, parameter.access.create_func)()
        if not(id_parameter in list_id_parameters_already_exists):
            parameter.val = getattr(parameter, 'value', None)

    def configure_parameters(self, object, object_id, list_id_parameters_already_exists):
        list_parameters_name_should_exists = filter(lambda attr: type(getattr(object, attr)) is Parameter, dir(object))
        for name in list_parameters_name_should_exists:
            parameter = object.__dict__[name]
            parameter.parameter_name = name
            self.create_parameter(name, parameter, object_id, list_id_parameters_already_exists)

    def create_command(self, name, command, object_id):
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

    def configure_commands(self, object, object_id):
        for name in object.commands:
            command = object.commands[name]
            self.create_command(name, command, object_id)

    def configure_single_event(self, name, event, object_id):
        event.set_multi_stub(self.multi_stub)
        event.id = self.create_event(id_object=object_id, name=name)
        getattr(event, event.priority.create_func)()
        event.clear()
        for key, val in event.args.iteritems():
            event.set_argument(key, utils.get_rpc_value(val))

    def configure_events(self, object, object_id):
        list_events = filter(lambda attr: type(getattr(object, attr)) is Event, dir(object))
        for name in list_events:
            event = object.__dict__[name]
            self.configure_single_event(name, event, object_id)

    def configure_run_function(self, object, object_id, list_id_parameters_already_exists):
        for name in object.run_function_names:
            time_stamp = time.time()
            period_name = getattr(object, name).period_name
            period = getattr(object, name).period_default_value
            parameter_period = ParameterDouble(value=period, visible=setup)
            object.__dict__[period_name] = parameter_period
            self.create_parameter(period_name, parameter_period, object.id, list_id_parameters_already_exists)
            self.tasks_pool.add_task(time_stamp+period, getattr(object, name))

    def join(self):
        try:
            g_thread = Thread(target=self.grpc_thread)
            g_thread.start()
            while True: #главный тред, который нужен для того, чтобы можно было завершит остальные
                time.sleep(0.1) # цикл прерывается при посылке сигнала SIGINT
                if not(g_thread.is_alive()):
                    break

        except Exit:
            self.tasks_pool.shutdown_flag.set()
            self.tasks_pool.operation_thread.join()
            self.multi_stub.channel.close()
            g_thread.join()

    def grpc_thread(self):
        """
        Бесконечный цикл: получаем состояние от адаптера.
        :return:
        """
        try:
            for r in self.multi_stub.stub_adapter.states(rpc_pb2.Empty()):
                ack = r
                try:
                    if r.state == rpc_pb2.AdapterStream.AFTER_CREATING_OBJECT:
                        log.info('Create device {0}'.format(r.id))
                        self.create_object(r.id)

                    elif r.state == rpc_pb2.AdapterStream.BEFORE_REMOVING_OBJECT:
                        log.info('Remove device {0}'.format(r.id))
                        if r.id in self.nodes:
                            self.nodes[r.id].handle_before_remove_device()
                            del self.nodes[r.id]
                            # TODO удалить компоненты из self.components
                            log.info('Device {0} removed'.format(r.id))
                        else:
                            log.warn('Device {0} not found'.format(r.id))

                    elif r.state == rpc_pb2.AdapterStream.GETTING_AVAILABLE_CHILDREN:
                        log.info('Get available children of {0}'.format(r.id))
                        self.get_available_children(r.id)

                    elif r.state == rpc_pb2.AdapterStream.AFTER_SETTING_PARAMETER:
                        if r.id in self.components:  # есть параметры, которые по умолчанию в адаптере
                            self.components[r.id].callback()

                    elif r.state == rpc_pb2.AdapterStream.EXECUTING_COMMAND:
                        if r.id in self.components:
                            self.components[r.id].call_function()
                        else:
                            log.warn('Command {0} not found'.format(r.id))

                    self.multi_stub.stub_adapter.ack(ack)

                except Exit:
                    self.tasks_pool.shutdown_flag.set()
                    self.tasks_pool.operation_thread.join()
                    self.multi_stub.channel.close()

                except Exception, err:
                    log.error(str(err) + '\nstate=' + str(r.state))

        except Exception, err:
            log.error(str(err))

