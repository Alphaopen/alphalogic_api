# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import signal
import time
from threading import Thread
import alphalogic_api.protocol.rpc_pb2 as rpc_pb2
from alphalogic_api.core.multistub import MultiStub
from alphalogic_api.core.parameter import Parameter
from alphalogic_api.core.event import Event
from alphalogic_api.core import utils
from alphalogic_api.logger import log
from alphalogic_api.core.tasks_pool import TasksPool
from alphalogic_api.core.parameter import ParameterDouble
from alphalogic_api.core.utils import Exit, shutdown, decode_string
from alphalogic_api.core.type_attributes import Visible


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
        return answer.type

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

    def register_maker(self, id_object, name, type_str):
        answer = self._call('register_maker', id_object, name=name, type=type_str)
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
    dict_type_objects = {}  # По type можно определить соответсвующий класс для создания
    nodes = {}  # Список всех узлов, по id узла можно обратиться в словаре к узлу
    components = {}  # По id команды можно обратиться к параметрам, событиям, командам
    components_for_device = {}  # По id устройства можно определить id его компонент

    def __init__(self):
        signal.signal(signal.SIGTERM, shutdown)
        signal.signal(signal.SIGINT, shutdown)
        self.g_thread = Thread(target=self.grpc_thread)
        self.tasks_pool = TasksPool()

    def configure_multi_stub(self, address):
        self.multi_stub = MultiStub(address)

    def prepare_for_work(self, object, id):
        Manager.nodes[id] = object
        list_id_parameters_already_exists = self.parameters(id)
        list_parameters_name_already_exists = map(lambda id: self.multi_stub.parameter_call('name', 'name', id=id),
                                                  list_id_parameters_already_exists)
        list_parameters_name_period = [getattr(object, name).period_name for name in object.run_function_names]
        list_parameters_name_should_exists = filter(lambda attr: type(getattr(object, attr)) is Parameter, dir(object))
        list_parameters_name_should_exists = list(set(list_parameters_name_should_exists)
                                                  | set(list_parameters_name_period))
        list_parameters_name_should_exists = list(set(list_parameters_name_should_exists)
                                                  - set(list_parameters_name_already_exists))
        # order of call below function is important
        self.configure_run_function(object, id, list_id_parameters_already_exists)
        self.configure_parameters(object, id, list_id_parameters_already_exists, list_parameters_name_should_exists)
        self.configure_parameters(object, id, list_id_parameters_already_exists, list_parameters_name_already_exists)
        self.configure_commands(object, id)
        self.configure_events(object, id)

    def prepare_existing_devices(self, id_parent):
        for child_id in self.children(id_parent):
            class_name_str = self.get_type(child_id)
            if class_name_str not in Manager.dict_type_objects:
                Manager.dict_type_objects[class_name_str] = utils.get_class_name_from_str(class_name_str)
            class_name = Manager.dict_type_objects[class_name_str]
            object = class_name(class_name_str, child_id)
            Manager.components_for_device[child_id] = []
            self.prepare_for_work(object, child_id)
            self.prepare_existing_devices(child_id)

    def create_object(self, object_id):
        parent_id = self.parent(object_id)
        parent = Manager.nodes[parent_id] if (parent_id in Manager.nodes) else None
        class_name_str = self.get_type(object_id)
        class_name = Manager.dict_type_objects[class_name_str]
        object = class_name(class_name_str, object_id)
        Manager.nodes[object_id] = object
        Manager.components_for_device[object_id] = []
        self.prepare_for_work(object, object_id)

    def delete_object(self, object_id):
        with Manager.nodes[object_id].mutex:
            Manager.nodes[object_id].flag_removing = True
            Manager.nodes[object_id].handle_before_remove_device()

            def delete_id(id):
                del Manager.components[id]

            map(delete_id, Manager.components_for_device[object_id])
            del Manager.components_for_device[object_id]
            del Manager.nodes[object_id]
            log.info('Device {0} removed'.format(object_id))

    def get_available_children(self, id_device):
        device = Manager.nodes[id_device]
        available_devices = device.handle_get_available_children()
        self.unregister_all_makers(id_object=id_device)

        for class_name, type_when_create in available_devices:
            self.register_maker(id_object=id_device, name=type_when_create, type_str=class_name.__name__)
            if class_name.__name__ not in Manager.dict_type_objects:
                Manager.dict_type_objects[class_name.__name__] = class_name

    def get_type(self, node_id):
        type_str = self.type(node_id)[7:]  # cut string 'device.'
        return type_str

    def create_parameter(self, name, object, object_id, list_id_parameters_already_exists, is_copy=True,
                         parameter=None):
        if is_copy:
            parameter = object.__dict__[name].get_copy()
        object.__dict__[name] = parameter
        parameter.parameter_name = name
        parameter.set_multi_stub(self.multi_stub)
        value_type = parameter.value_type
        id_parameter = getattr(self, utils.create_parameter_definer(str(value_type))) \
            (id_object=object_id, name=name)
        parameter.id = id_parameter
        getattr(parameter, parameter.visible.create_func)()
        getattr(parameter, parameter.access.create_func)()
        if parameter.choices is not None:
            parameter.set_choices()
        if not (id_parameter in list_id_parameters_already_exists):
            parameter.val = getattr(parameter, 'default', None)
        elif parameter.choices is not None:
            is_tuple = type(parameter.choices[0]) is tuple
            if (is_tuple and not (parameter.val in zip(*parameter.choices)[0])) \
                    or not is_tuple and not (parameter.val in parameter.choices):
                parameter.val = getattr(parameter, 'default', None)
        if is_copy:
            Manager.components[id_parameter] = parameter
            Manager.components_for_device[object_id].append(id_parameter)

    def configure_parameters(self, object, object_id, list_id_parameters_already_exists, list_names):
        for name in list_names:
            self.create_parameter(name, object, object_id, list_id_parameters_already_exists)

    def create_command(self, name, command, object_id):
        command.set_multi_stub(self.multi_stub)
        result_type = command.result_type
        id_command = getattr(self, utils.create_command_definer(str(result_type))) \
            (id_object=object_id, name=name)
        command.id = id_command
        command.clear()
        for arg in command.arguments:
            name_arg, value_arg = arg
            command.set_argument(name_arg, value_arg)
        Manager.components[id_command] = command
        Manager.components_for_device[object_id].append(id_command)

    def configure_commands(self, object, object_id):
        for name in object.commands:
            command = object.commands[name]
            self.create_command(name, command, object_id)

    def configure_single_event(self, name, event, object_id):
        event.set_multi_stub(self.multi_stub)
        event.id = self.create_event(id_object=object_id, name=name)
        getattr(event, event.priority.create_func)()
        event.clear()
        for name_arg, value_type in event.arguments:
            value_arg = utils.value_from_rpc(utils.get_rpc_value(value_type), value_type)
            event.set_argument(name_arg, value_arg)
        Manager.components[event.id] = event
        Manager.components_for_device[object_id].append(event.id)

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
            parameter_period = ParameterDouble(default=period, visible=Visible.setup)
            self.create_parameter(period_name, object, object.id, list_id_parameters_already_exists,
                                  is_copy=False, parameter=parameter_period)
            period = parameter_period.val  # Если параметр все-таки существует
            self.tasks_pool.add_task(time_stamp + period, getattr(object, name))

    def get_all_device(self, object_id, result):
        list_children = self.children(object_id)
        result.append(object_id)
        map(lambda x: self.get_all_device(x, result), list_children)

    def join(self):
        self.g_thread.start()
        while True:  # главный тред, который нужен для того, чтобы можно было завершит остальные
            time.sleep(0.1)  # цикл прерывается при посылке сигнала SIGINT
            if not (self.g_thread.is_alive()):
                break

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
                        if r.id in Manager.nodes:
                            self.delete_object(r.id)
                        else:
                            log.warn('Device {0} not found'.format(r.id))

                    elif r.state == rpc_pb2.AdapterStream.GETTING_AVAILABLE_CHILDREN:
                        log.info('Get available children of {0}'.format(r.id))
                        self.get_available_children(r.id)

                    elif r.state == rpc_pb2.AdapterStream.AFTER_SETTING_PARAMETER:
                        if r.id in Manager.components:
                            if Manager.components[r.id].callback:
                                param = Manager.components[r.id]  # TODO check
                                device = Manager.nodes[param.owner()]  # TODO check
                                Manager.components[r.id].callback(device, param)
                        else:
                            log.warn('Parameter {0} not found'.format(r.id))

                    elif r.state == rpc_pb2.AdapterStream.EXECUTING_COMMAND:
                        if r.id in Manager.components:
                            Manager.components[r.id].call_function()
                        else:
                            log.warn('Command {0} not found'.format(r.id))

                except Exception, err:
                    log.error(decode_string(err) + '\nstate=' + decode_string(r.state))

                finally:
                    self.multi_stub.stub_adapter.ack(ack)

        except Exception, err:
            log.error(decode_string(err))