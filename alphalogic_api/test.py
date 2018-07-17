# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import grpc
import datetime
import time

from alphalogic_api.core.type_attributes import Visible, Access, Priority

from alphalogic_api.core.core import Root, Device
from alphalogic_api.core.command import command
from alphalogic_api.core.event import MajorEvent
from alphalogic_api.core.parameter import Parameter, ParameterBool, ParameterInt, \
    ParameterDouble, ParameterDatetime, ParameterString
from alphalogic_api.core import utils
from alphalogic_api.core.run_function import run
from alphalogic_api import host, port
from alphalogic_api.core.exceptions import ComponentNotFound, RequestError

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


def handle_after_set_double(node, parameter):
    node.log.info('double changed')
    node.after_set_value_test_event.emit(value=parameter.val)


class MyRoot(Root):
    name = ParameterString(default='RootNode')
    displayName = ParameterString(default='RootNode')

    param_string = ParameterString(default='noop', visible=Visible.setup)
    param_bool = ParameterBool(default=False, visible=Visible.common)
    param_int = ParameterInt(default=2, visible=Visible.runtime, access=Access.read_only)
    param_double = ParameterDouble(default=2.3, callback=handle_after_set_double)
    param_timestamp = ParameterDatetime(default=datetime.datetime.utcnow())
    param_hid = ParameterDouble(default=2.2, visible=Visible.hidden)
    param_vect = ParameterInt(default=1, choices=(0, 1, 2, 3))
    param_vect2 = ParameterInt(default=2, choices=((0, 'str 77'), (1, 'str 88'), (2, 'str 2'), (3, 'str 3')))

    alarm = MajorEvent(('where', unicode),
                       ('when', datetime.datetime),
                       ('why', int))
    simple_event = MajorEvent()
    after_set_value_test_event = MajorEvent(('value', float))

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

    # Check Command return

    @command(result_type=int)
    def cmd_return_int(self):
        return int(utils.milliseconds_from_epoch(datetime.datetime.utcnow()) / 1000.0)

    @command(result_type=float)
    def cmd_return_float(self):
        return int(utils.milliseconds_from_epoch(datetime.datetime.utcnow()) % 1000.0) / 1000.0

    @command(result_type=unicode)
    def cmd_return_unicode(self):
        return 'некоторый текст'

    @command(result_type=datetime.datetime)
    def cmd_return_datetime(self):
        return datetime.datetime.utcnow()

    #
    @command(result_type=bool, which=(1, 2, 3), which2=((True, 'On'), (False, 'Off')))
    def relax(self, where='room', why=42, which=2, which2=False):
        self.log.info(u'where=' + where + u'; why=' + unicode(why)
                      + u'; which=' + unicode(which) + u'; which2=' + unicode(which2))
        return True

    @run(period_a=10)
    def run_two(self):
        self.log.info(unicode(self.id) + ' a_run')

    @run(period_b=24)
    def run_one(self):
        self.log.info(unicode(self.id) + ' b_run')


class Controller(Device):

    # Parameters:
    name = ParameterString(value='Controller')
    displayName = ParameterString(value='Controller')

    hostname = ParameterString(visible=Visible.setup, access=Access.read_write, default='1', choices=('1', '2'))
    mode = ParameterBool(visible=Visible.setup, default=True, choices=((True, 'On'), (False, 'Off')))
    version = Parameter(value_type=int, visible=Visible.common)
    counter = ParameterDouble(default=1.0, access=Access.read_only)
    counter_spec = ParameterDouble(default=1.0, access=Access.read_write)

    @command(result_type=bool, which=((True, 'On'), (False, 'Off')))
    def relax(self, where='room', when=datetime.datetime.now(), why=42, which=False):
        return True

    @run(period=20)
    def run_third(self):
        self.log.info(unicode(self.id) + ' c_run')
        val = self.counter_spec.val
        self.counter_spec.val = val+1

    def handle_get_available_children(self):
        return [
            (Controller, 'Controller')
        ]


# python loop
root = MyRoot(host, port)

cmds = root.commands()
# Parameters
try:
    root.parameter('asgasdgg')
    assert False, 'ComponentNotFound doesnt\' works'
except ComponentNotFound, err:
    pass
except RequestError, err: # TODO убрать, как починят адаптеры
    pass

pars = root.parameters()
assert list(x.name() == 'param_bool' for x in pars)
param = root.parameter('param_bool')
assert not param.val
param = root.parameter('param_int')
assert param.val == 2

# Events
try:
    root.event('asgasdgg')
    assert False, 'ComponentNotFound doesnt\' works'
except ComponentNotFound, err:
    pass
except RequestError, err: # TODO убрать, как починят адаптеры
    pass

events = root.events()
assert list(x.name() == 'alarm' for x in events)
ev = root.event('alarm')

# Commands

try:
    root.command('asgasdgg')
    assert False, 'ComponentNotFound doesnt\' works'
except ComponentNotFound, err:
    pass
except RequestError, err:  # TODO убрать, как починят адаптеры
    pass

assert list(x.name() == 'cmd_simple_event' for x in cmds)
cmd = root.command('cmd_simple_event')
cmd = root.command('check')

root.join()


'''
assert root.param_string.val == 'noop'
assert root.param_string.is_setup()
assert not root.param_bool.val
assert root.param_bool.is_common()
assert root.param_int.val == 2
assert root.param_int.is_runtime()
assert root.param_int.is_read_only()
assert root.param_double.val == 2.3
assert root.param_double.is_runtime(), 'default wrong'
assert root.param_double.is_read_write(), 'default wrong'
#assert (datetime.datetime.now() - root.param_timestamp.val).total_seconds() < 10

#assert root.param_vect.val == (0, 1, 2, 3)


root.param_double.val = 5.0
assert root.param_double.val == 5.0

#check read_only
#try:
#    root.param_int.val = 3
#    assert False
#except Exception:
#    pass


#adapter.relax(1, 2, 3, 4)

root.simple_event.emit()

root.alarm.set_time(int(time.time()) * 1000 - 100000)
root.alarm.emit(where='asdadsadg', why=3, when=datetime.datetime.now())
'''
