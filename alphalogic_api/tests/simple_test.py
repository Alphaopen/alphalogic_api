# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from alphalogic_api.attributes import Visible, Access
from alphalogic_api.objects import Root, Device
from alphalogic_api.objects import MajorEvent
from alphalogic_api.objects import ParameterBool, ParameterInt, \
    ParameterDouble, ParameterDatetime, ParameterString
from alphalogic_api.options import host, port
from alphalogic_api.decorators import command, run


def handle_after_set_double(node, parameter):
    node.log.info('double changed')
    node.after_set_value_test_event.emit(value=parameter.val)


class MyRoot(Root):
    param_string = ParameterString(default='noop', visible=Visible.setup)
    param_bool = ParameterBool(default=False, visible=Visible.common)
    param_int = ParameterInt(default=2, visible=Visible.runtime, access=Access.read_only)
    param_double = ParameterDouble(default=2.3, callback=handle_after_set_double)
    param_timestamp = ParameterDatetime(default=datetime.datetime.utcnow())
    param_vect2 = ParameterInt(default=2, choices=((0, 'str 77'), (1, 'str 88'), (2, 'str 2'), (3, 'str 3')))

    alarm = MajorEvent(('where', unicode),
                       ('when', datetime.datetime),
                       ('why', int))

    simple_event = MajorEvent()

    def handle_get_available_children(self):
        return [
            (Controller, 'Controller')
        ]

    @command(result_type=bool)
    def cmd_alarm(self, where='here', when=datetime.datetime.now(), why=2):
        return True

    @command(result_type=bool)
    def cmd_exception(self):
        raise Exception('fire!')
        return True


class Controller(Device):

    counter = ParameterInt(default=0)

    @run(period_one=1)
    def run_one(self):
        self.counter.val += 1


# python loop
root = MyRoot(host, port)
root.join()

