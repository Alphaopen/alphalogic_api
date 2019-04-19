# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
import time
from functools import partial

from alphalogic_api.attributes import Visible, Access
from alphalogic_api.objects import Root, Object
from alphalogic_api.objects import MajorEvent
from alphalogic_api.objects import ParameterBool, ParameterLong, \
    ParameterDouble, ParameterDatetime, ParameterString
from alphalogic_api.decorators import command, run

'''
There are handlers available:
1) handler will be executed after parameter was changed

2) handle_prepare_for_work
Handler is executed before work of object

3) handle_defaults_loaded
Handler for configure Object after creation.

4) handle_before_remove_device
Handler is executed before object node was deleted

5) handle_get_available_children
Return possible objects for creation

'''


# handler will be executed after parameter was changed
def handle_after_set_double(node, parameter):
    node.log.info('double changed')
    node.after_set_value_test_event.emit(value=parameter.val)


class MyRoot(Root):
    param_double = ParameterDouble(default=2.3, callback=handle_after_set_double)

    # Example of passing values into constructor of ControlB and ControlC
    def handle_get_available_children(self):

        r = []

        # Object's handle_defaults_loaded will be call after creation of ControllerB
        for i in range(5):
            f = partial(ControllerB, number=i)
            f.cls = ControllerB
            r.append((f, 'ControllerB {0}'.format(i)))

        # ControllerC's handle_defaults_loaded will be call after creation of ControllerC
        for i in range(3):
            f = partial(ControllerC, other_number=i)
            f.cls = ControllerC
            r.append((f, 'ControllerC {0}'.format(i)))

        r.append((ControllerA, 'ControllerA'))

        def handler():
            print('Controller D created')

        f = partial(ControllerD, param=handler)
        f.cls = ControllerD
        r.append((f, 'ControllerD'))

        return r


class ControllerA(Object):
    counter = ParameterLong(default=0)

    @run(period_one=1)
    def run_one(self):
        self.counter.val += 1


class ControllerB(Object):
    number = ParameterLong(visible=Visible.setup)

    def handle_prepare_for_work(self):
        self.displayName.val = str(self.number.val)

    def handle_before_remove_device(self):
        # do some things, close file descriptors and etc
        pass


class ControllerC(Object):
    counter = 0
    number = ParameterLong(visible=Visible.setup)

    # Will be called first after creation
    def handle_defaults_loaded(self, **kwargs):
        if 'other_number' in kwargs:
            self.number.val = kwargs['other_number']

    # Will be called second after creation
    def handle_prepare_for_work(self):
        self.displayName.val = str(self.number.val) + '_' + str(ControllerC.counter)
        ControllerC.counter = ControllerC.counter + 1


class ControllerD(Object):

    def __init__(self, type_device, id_device, **kwargs):
        super(ControllerD, self).__init__(type_device, id_device, **kwargs)
        assert 'param' in kwargs
        kwargs['param']()


if __name__ == '__main__':
    # python loop
    root = MyRoot()
    root.join()

