# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
        is_callable = lambda x: callable(getattr(service, x)) and not x.startswith('_')  # получить методы Service, исключая служебные
        return set(filter(is_callable, dir(service)))

    def object_call(self, *args, **kwargs):
        obj_w = ObjectRequest(**kwargs)
        return self.call_helper(*args, fun_set=MultiStub.object_fun_set,  request=obj_w, stub=self.stub_object)

    def parameter_call(self, *args, **kwargs):
        par_w = ParameterRequest(**kwargs)
        return self.call_helper(*args, fun_set=MultiStub.parameter_fun_set, request=par_w, stub=self.stub_parameter)

    def event_call(self, *args, **kwargs):
        event_w = EventRequest(**kwargs)
        return self.call_helper(*args, fun_set=MultiStub.event_fun_set, request=event_w, stub=self.stub_event)

    def command_call(self, *args, **kwargs):
        command_w = CommandRequest(**kwargs)
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
    def call_helper(self, function_name, *args, **kwargs):
        if function_name in kwargs['fun_set']:  # function_name - название функции, проверка на допустимость
            answer = getattr(kwargs['stub'], function_name)(kwargs['request'])
            return reduce(lambda acc, x: getattr(answer, x), args, answer)  # рекурсивный поиск
        else:
            raise Exception('{0} not found in {1}'.format(function_name, kwargs['fun_set']))


print "static MultiStub initialization"
MultiStub.static_initialization()