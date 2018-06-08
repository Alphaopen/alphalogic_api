# -*- coding: utf-8 -*-

import grpc

from callbox.protocol.rpc_pb2 import (
ObjectRequest,
ParameterRequest,
EventRequest,
CommandRequest
)

from callbox.protocol.rpc_pb2_grpc import (
ObjectServiceStub,
ParameterServiceStub,
EventServiceStub,
CommandServiceStub,
AdapterServiceStub,
ObjectServiceServicer,
ParameterServiceServicer,
EventServiceServicer,
CommandServiceServicer,
AdapterServiceServicer
)

class MultiStub(object):

    def __init__(self, target):
        channel = grpc.insecure_channel(target)
        self.stub_object = ObjectServiceStub(channel)
        self.stub_parameter = ParameterServiceStub(channel)
        self.stub_event = EventServiceStub(channel)
        self.stub_command = CommandServiceStub(channel)
        self.stub_adapter = AdapterServiceStub(channel)

    @staticmethod
    def static_initialization():
        MultiStub.object_fun_set = MultiStub.dict_create_helper(ObjectServiceServicer)
        MultiStub.parameter_fun_set = MultiStub.dict_create_helper(ParameterServiceServicer)
        MultiStub.event_fun_set = MultiStub.dict_create_helper(EventServiceServicer)
        MultiStub.command_fun_set = MultiStub.dict_create_helper(CommandServiceServicer)
        MultiStub.adapter_fun_set = MultiStub.dict_create_helper(AdapterServiceServicer)

    @staticmethod
    def dict_create_helper(service):
        obj_fun_list = [fun for fun in dir(service)
              if callable(getattr(service, fun))]
        return set(filter(lambda fun : fun[0:2]!='__', obj_fun_list)) # получить методы Service, исключая служебные

    def object_call(self, *args):
        obj_w = ObjectRequest()
        return self.call_helper(*args, fun_set=MultiStub.object_fun_set,  request=obj_w, stub=self.stub_object)
        '''
        if argv[0] in MultiStub.object_fun_set:
            obj_w = rpc_pb2.ObjectRequest()
            answer = getattr(self.stub_object, argv[0])(obj_w)
            return getattr(answer.object, argv[1])
        else:
            raise Exception('{} not found in object_fun_set'.format(argv[0]))
        '''

    def parameter_call(self, *args, **kwargs):
        par_w = ParameterRequest(**kwargs)
        return self.call_helper(*args, fun_set=MultiStub.parameter_fun_set, request=par_w, stub=self.stub_parameter)

    def event_call(self, *args):
        event_w = EventRequest()
        return self.call_helper(*args, fun_set=MultiStub.event_fun_set, request=event_w, stub=self.stub_event)

    def command_call(self, *args):
        command_w = CommandRequest()
        return self.call_helper(*args, fun_set=MultiStub.command_fun_set, request=command_w, stub=self.stub_command)
    '''
    def adapter_call(self, *args):
        adapter_w = rpc_pb2.AdapterRequest()
        return self.call_helper(*args, fun_set=MultiStub.object_fun_set, request=adapter_w, stub=self.stub_adapter)
    '''
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


print "static MultiStub initialization"
MultiStub.static_initialization()