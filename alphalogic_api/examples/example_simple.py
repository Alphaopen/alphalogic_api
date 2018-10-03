# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from alphalogic_api.attributes import Visible, Access
from alphalogic_api.objects import Root, Object
from alphalogic_api.objects import MajorEvent
from alphalogic_api.objects import ParameterBool, ParameterLong, \
    ParameterDouble, ParameterDatetime, ParameterString
from alphalogic_api.decorators import command, run


# Handle will be executed after parameter param_double was changed
def handle_after_set_double(node, parameter):
    node.log.info('double changed')
    node.after_set_value_test_event.emit(value=parameter.val)


class MyRoot(Root):
    # Parameters
    param_string = ParameterString(default='noop', visible=Visible.setup)
    param_bool = ParameterBool(default=False, visible=Visible.common)
    param_int = ParameterLong(default=2, visible=Visible.runtime, access=Access.read_only)
    param_double = ParameterDouble(default=2.3, callback=handle_after_set_double)
    param_timestamp = ParameterDatetime(default=datetime.datetime.utcnow())
    param_vect2 = ParameterLong(default=2, choices=((0, 'str 77'), (1, 'str 88'), (2, 'str 2'), (3, 'str 3')))
    param_count = ParameterLong(default=0)

    # Events
    alarm = MajorEvent(('where', unicode),
                       ('when', datetime.datetime),
                       ('why', int))

    simple_event = MajorEvent()

    # Possible objects for creation
    def handle_get_available_children(self):
        return [
            (Controller, 'Controller')
            ]

    # Commands
    @command(result_type=long)
    def cmd_alarm(self, where='here', when=datetime.datetime.now(), why=2):
        self.simple_event.emit()
        return self.param_count.val

    @command(result_type=bool)
    def cmd_exception(self):
        raise Exception('fire!')
        return True


class Controller(Object):
    counter = ParameterLong(default=0)

    # This function will be executed periodically once per 1 second
    @run(period_one=1)
    def run_one(self):
        self.counter.val += 1


if __name__ == '__main__':
    # python loop
    root = MyRoot()
    root.join()

