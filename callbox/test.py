# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import grpc
import datetime
import time

from callbox.core.type_attributes import runtime, setup, hidden, common
from callbox.core.type_attributes import read_only, read_write
from callbox.core.type_attributes import major

from callbox.core.core import Root, Device
from callbox.core.command import command
from callbox.core.event import Event
from callbox.core.parameter import Parameter, ParameterBool, ParameterInt, \
    ParameterDouble, ParameterDatetime, ParameterString
from callbox.core import utils
from callbox.core.tasks_pool import run


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

def handle_after_set_double():
    print 'double changed'


class MyRoot(Root):
    #name = ParameterString(value='RootNode')
    #displayName = ParameterString(value='RootNode')

    param_string = ParameterString(value='noop', visible=setup)
    param_bool = ParameterBool(value=False, visible=common)
    param_int = ParameterInt(value=2, visible=runtime, access=read_only)
    param_double = ParameterDouble(value=2.3, callback=handle_after_set_double)
    param_timestamp = ParameterDatetime(value=datetime.datetime.utcnow())
    param_hid = ParameterDouble(value=2.2, access=hidden)
    param_vect = ParameterInt(value=(0, 1, 2, 3))

    alarm = Event(('where', unicode),
                  ('when', datetime.datetime),
                  ('why', int))
    simple_event = Event()

    def handle_create(self):
        pass

    def handle_remove(self):
        pass

    def handle_get_available_children(self):
        return [
            (Controller, 'Controller')
        ]

    @command(result_type=bool)
    def cmd_simple_event(self):
        self.simple_event.emit()
        return True

    @command(result_type=bool)
    def cmd_simple_event_manual_time(self, timestamp=0):
        self.simple_event.set_time(timestamp)
        self.simple_event.emit()
        return True

    @command(result_type=bool)
    def cmd_alarm(self, where='here', when=datetime.datetime.now(), why=2):
        self.alarm.emit(where=where, when=when, why=why)
        return True

    @command(result_type=unicode)
    def check(self, where='here'):
        #self.relax(1, 2, 3, 4)
        return 'abc'

    @command(result_type=bool)
    def failed_cmd(self):
        self.log.info("failed cmd start")
        raise Exception("command failed")
        return False

    # Проверка возвращаемых значений

    @command(result_type=int)
    def cmd_return_int(self):
        ret = int(utils.milliseconds_from_epoch(datetime.datetime.utcnow()) / 1000.0)
        return ret

    @command(result_type=float)
    def cmd_return_float(self):
        ret = int(utils.milliseconds_from_epoch(datetime.datetime.utcnow()) % 1000.0) / 1000.0
        return ret

    @command(result_type=unicode)
    def cmd_return_unicode(self):
        return 'некоторый текст'

    @command(result_type=datetime.datetime)
    def cmd_return_datetime(self):
        return datetime.datetime.utcnow()

    #

    @command(result_type=bool)
    def relax(self, where='room', why=42, which=(1, 2, 3), which2=({'On': True}, {'Off': False})):
        print where
        print why
        print which
        print which2
        return True

    @run(period_a=10)
    def run_two(self):
        print str(self.id) + ' a_run'

    @run(period_b=24)
    def run_one(self):
        print str(self.id) + ' b_run'
    

class Controller(Device):
    # Parameters:
    displayName = ParameterString()

    hostname = ParameterString(visible=setup, access=read_write, value=('1', '2'))
    mode = ParameterBool(visible=setup, value=({'On': True}, {'Off': False}))
    version = Parameter(value_type=int, visible=common)
    counter = ParameterDouble(value=1.0, access=read_only)
    counter_spec = ParameterDouble(value=1.0, access=read_write)

    @command(result_type=bool)
    def relax(self, where='room', when=datetime.datetime.now(), why=42, which=[{'On': True}, {'Off': False}]):
        return True

    @run(period=20)
    def run_third(self):
        print str(self.id)+' c_run'
        val = self.counter_spec.val
        self.counter_spec.val = val+1

    def handle_get_available_children(self):
        return [
            (Controller, 'Controller')
        ]


# python loop
adapter = MyRoot('localhost', 42001)


'''
assert adapter.param_string.val == 'noop'
assert adapter.param_string.is_setup()
assert not adapter.param_bool.val
assert adapter.param_bool.is_common()
assert adapter.param_int.val == 2
assert adapter.param_int.is_runtime()
assert adapter.param_int.is_read_only()
assert adapter.param_double.val == 2.3
assert adapter.param_double.is_runtime(), 'default wrong'
assert adapter.param_double.is_read_write(), 'default wrong'
#assert (datetime.datetime.now() - adapter.param_timestamp.val).total_seconds() < 10

#assert adapter.param_vect.val == (0, 1, 2, 3)


adapter.param_double.val = 5.0
assert adapter.param_double.val == 5.0

#check read_only
#try:
#    adapter.param_int.val = 3
#    assert False
#except Exception:
#    pass


#adapter.relax(1, 2, 3, 4)
'''

adapter.simple_event.emit()

adapter.alarm.set_time(int(time.time()) * 1000 - 100000)
adapter.alarm.emit(where='asdadsadg', why=3, when=datetime.datetime.now())
adapter.join()
