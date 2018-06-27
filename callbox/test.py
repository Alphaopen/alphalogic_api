# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import grpc
import datetime

from callbox.core.type_attributes import runtime, setup, hidden, common
from callbox.core.type_attributes import read_only, read_write
from callbox.core.type_attributes import major

from core.core import  Root, Device
from core.command import command
from callbox.core.event import Event
from callbox.core.parameter import Parameter, ParameterBool, ParameterInt, \
    ParameterDouble, ParameterDatetime, ParameterString
import time


'''
Не забыть важные моменты:
1) Нужно преобразовать type_attributes в более приемлимое
   Когда создается параметр используется именнованные аргументы.
   Нужно попробовать отказать от словарей и лямбда функций в таком виде

2) Перед запуском проверять узлы адаптера и в соотвествии с этим менять свое состояние.
   Чтобы не было несогласованных состояний.

3) В параметрах, событиях
  присутсвует в описании rpc функции:

  Value value = 4; // rpc set, set_enum
  map<string, Value> enums = 5; // rpc set_enums

  необходимо вынести их обработку в один код

4) Как сделать выбор некоторых параметров по умолчанию?
'''


class MyRoot(Root):
    name = ParameterString(value='RootNode')
    displayName = ParameterString(value='RootNode')

    param_string = ParameterString(value='noop', visible=setup)
    param_bool = ParameterBool(value=False, visible=common)
    param_int = ParameterInt(value=2, visible=runtime, access=read_only)
    param_double = ParameterDouble(value=2.3, access=read_write)
    param_timestamp = ParameterDatetime(value=datetime.datetime.now())
    param_vect = ParameterInt(value=(0, 1, 2, 3))

    simple_event = Event()
    alarm = Event(priority=major, args=dict(where=str, when=datetime.datetime, why=int))

    def handle_create(self):
        pass

    def handle_remove(self):
        pass

    def handle_get_available_children(self):
        return [
            (Controller, 'Controller')
        ]

    @command(result_type=unicode)
    def check(self, where='here'):
        #self.relax(1, 2, 3, 4)
        return 'abc'

    @command(result_type=bool)
    def relax(self, where='room', why=42, which=(1, 2, 3), which2=({'On': True}, {'Off': False})):
        print where
        print why
        print which
        print which2
        return True

    '''
    @command(result_type=int)
    def affair(self, where):
        return 1
    '''


class Controller(Device):
    # Parameters:
    name = ParameterString(value='Controller')
    displayName = ParameterString(value='Controller')
    hostname = ParameterString(visible=setup, access=read_write, value=('1', '2'))
    mode = ParameterBool(visible=setup, value=({'On': True}, {'Off': False}))
    version = Parameter(value_type=int)
    counter = ParameterDouble(default=1.0)

    '''
    @command(result_type=bool)
    def relax(self, where='room', when=datetime.datetime.now(), why=42, which=[{'On': True}, {'Off': False}]):
        return True
    '''

    def run(self):
        pass


# python loop
adapter = MyRoot("localhost:42001")

assert adapter.param_string.val == 'noop'
assert adapter.param_string.is_setup()
assert not adapter.param_bool.val
assert adapter.param_bool.is_common()
assert adapter.param_int.val == 2
assert adapter.param_int.is_runtime()
assert adapter.param_int.is_read_only()
assert adapter.param_double.val == 2.3
#assert (datetime.datetime.now() - adapter.param_timestamp.val).total_seconds() < 10
#param_vect = ParameterInt(value=(0, 1, 2, 3))

#adapter.relax(1, 2, 3, 4)
adapter.simple_event.emit()

adapter.alarm.set_time(int(time.time()) * 1000 - 100000)
adapter.alarm.emit(where='asdadsadg', why=3)
adapter.join()
