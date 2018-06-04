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

import grpc
import callbox.protocol.rpc_pb2 as rpc_pb2
import callbox.protocol.rpc_pb2_grpc as rpc_pb2_grpc

class Api(object):

    def __init__(self, target):
        channel = grpc.insecure_channel(target)
        self.stub_object = rpc_pb2_grpc.ObjectServiceStub(channel)
        self.stub_parameter = rpc_pb2_grpc.ParameterServiceStub(channel)
        self.stub_event = rpc_pb2_grpc.EventServiceStub(channel)
        self.stub_command = rpc_pb2_grpc.CommandServiceStub(channel)
        self.stub_adapter = rpc_pb2_grpc.AdapterServiceStub(channel)

    @staticmethod
    def static_initialization():
        Api.object_fun_set = Api.dict_create_helper(rpc_pb2_grpc.ObjectServiceServicer)
        Api.parameter_fun_set = Api.dict_create_helper(rpc_pb2_grpc.ParameterServiceServicer)
        Api.event_fun_set = Api.dict_create_helper(rpc_pb2_grpc.EventServiceServicer)
        Api.command_fun_set = Api.dict_create_helper(rpc_pb2_grpc.CommandServiceServicer)
        Api.adapter_fun_set = Api.dict_create_helper(rpc_pb2_grpc.AdapterServiceServicer)

    @staticmethod
    def dict_create_helper(service):
        obj_fun_list = [fun for fun in dir(service)
              if callable(getattr(service, fun))]

        return set(filter(lambda fun : fun[0:2]!='__', obj_fun_list)) # получить методы Service, исключая служебные

    def object_call(self, *args):
        obj_w = rpc_pb2.ObjectRequest()
        return self.call_helper(*args, fun_set=Api.object_fun_set,  request=obj_w, stub=self.stub_object)
        '''
        if argv[0] in Api.object_fun_set:
            obj_w = rpc_pb2.ObjectRequest()
            answer = getattr(self.stub_object, argv[0])(obj_w)
            return getattr(answer.object, argv[1])
        else:
            raise Exception('{} not found in object_fun_set'.format(argv[0]))
        '''

    def parameter_call(self, *args):
        par_w = rpc_pb2.ParameterRequest()
        return self.call_helper(*args, fun_set=Api.parameter_fun_set, request=par_w, stub=self.stub_parameter)

    def event_call(self, *args):
        event_w = rpc_pb2.EventRequest()
        return self.call_helper(*args, fun_set=Api.event_fun_set, request=event_w, stub=self.stub_event)

    def command_call(self, *args):
        command_w = rpc_pb2.CommandRequest()
        return self.call_helper(*args, fun_set=Api.command_fun_set, request=command_w, stub=self.stub_command)

    def adapter_call(self, *args):
        adapter_w = rpc_pb2.AdapterRequest()
        return self.call_helper(*args, fun_set=Api.object_fun_set, request=adapter_w, stub=self.stub_adapter)

    '''
       Подумать над схемой:
       Первый член в *argv - это название функции для вызова
       Остальные - это разный уровень вложенности обращения : obj.argv[1].argv[2].argv[3] и т.д.

       Как можно проинспектировать тип переменной, которую надо создать чтобы передать в stub?
    '''
    def call_helper(self, *args, **kwargs):
        if args[0] in kwargs['fun_set']:
            answer = getattr(kwargs['stub'], args[0])(kwargs['request'])
            return getattr(answer.object, args[1])
        else:
            raise Exception('{0} not found in {1}'.format(args[0], kwargs['fun_set']))

class Device(object):

    def __init__(self, parent, name_device):
        self.parent = parent


class Root(object):

    def __init__(self, target, name):
        self.api = Api(target)
        self.id = self.api.object_call('root', 'id')
        print self.id
        print self.api.object_call('is_root', 'yes')


class ExampleAdapter(Root):
    '''
    Общая схема адаптера
    '''

    '''
    def scheme():
        root = Root("type")
        d1 = Device(parenr=root, "type1")
        d2 = Device(parent=root, "type2")
        d3 = Device(parent=d1, "type3")
        par = d1.Parameter("")
    '''


    def __init__(self, target, name):
        root = Root(target, name)
        d1 = Device(root, "node 1")
        #d2 = Device(parenr=r, "node 2")


    #r = Root("ip:port", "Name node")
    #d = Device(parent=r)
    # Сделать обязательным что-то одно либо type, либо #value
    # Можно опредлять тип из value 
    #p = Parameter(parent=d, "name", type, value, visible_type, access_type, display_name)
    #c = Command(parent=d)
    #e = Event(parent=e)
    
    

if __name__ != "__main__":
    print "static initializtion"
    Api.static_initialization()

