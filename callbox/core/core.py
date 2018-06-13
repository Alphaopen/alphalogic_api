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
        return self.__dict__[name]

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
        self.multi_stub = MultiStub("localhost:42001")

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
        self.configure_parameters(object, object_id)


    def configure_parameters(self, object, object_id):
        list_parameters_name = filter(lambda attr: type(getattr(object, attr)) is Parameter, dir(object))
        object_rpc = rpc_pb2.Object(id=object_id)
        for name in list_parameters_name:
            parameter = object.__dict__[name]
            value_type = parameter.ValueType
            id_parameter = self.multi_stub.object_call(ValueType.create_dict[value_type], 'parameter', 'id',
                                                       object=object_rpc, name=name)

            parameter_rpc = rpc_pb2.Parameter(id=id_parameter)
            visible_type = parameter.VisibleType
            self.multi_stub.parameter_call(VisibleType.set_dict[visible_type], parameter=parameter_rpc)

            access_type = parameter.AccessType
            self.multi_stub.parameter_call(AccessType.set_dict[access_type], parameter=parameter_rpc)

            if hasattr(parameter, 'Value'):
                if not (isinstance(parameter.Value, list)):  # для одного значения
                    value = rpc_pb2.Value(**ValueType.val_dict[value_type](parameter.Value))
                    self.multi_stub.parameter_call('set', parameter=parameter_rpc, value=value)
                else:  # для списков
                    req = rpc_pb2.ParameterRequest(parameter=parameter_rpc)
                    attr_type = ValueType.val_dict[value_type]('').keys()[0]
                    for val in parameter.Value:
                        if isinstance(val, dict):  # два поля в листе
                            setattr(req.enums[val.keys()[0]], attr_type, val.values()[0])  # проверить
                        else:
                            setattr(req.enums[str(val)], attr_type, val)

                    self.multi_stub.call_helper('set_enums', fun_set=MultiStub.parameter_fun_set, request=req,
                                                stub=self.multi_stub.stub_parameter)





        #ObjectService.create_string_parameter etc
        #set_runtime, set_setup
        #set_read_only, set_read_write
        #set value



class ExampleAdapter(Adapter):
    '''
    Общая схема адаптера
    '''

    root = Root("healhAdapterRoot")
    d1 = Device(root, "type1")
    d2 = Device(root, "type2")

    root.name3 = ParameterInt64(Value=[{'val1': True}, {'val2' : False}])

    root.name1 = Parameter(ValueType.INT64, VisibleType.COMMON, AccessType.READ_WRITE, Value = [1, 2])
    root.name2 = Parameter(ValueType.INT64)


    root.name4 = ParameterDouble(Value=-1.9)
    root.name5 = Parameter(VisibleType.HIDDEN, AccessType.READ_ONLY, ValueType.INT64)
    root.name6 = Parameter(ValueType.INT64)

    root.name7 = ParameterInt64(Value=3)
    root.name8 = Parameter(ValueType.INT64, VisibleType.HIDDEN, AccessType.READ_ONLY)
    root.name9 = Parameter(ValueType.INT64)

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

