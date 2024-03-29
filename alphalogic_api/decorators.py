# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import inspect
import time
import traceback
from alphalogic_api.logger import log
from alphalogic_api import utils
from alphalogic_api.utils import decode_string


def command_preparation(wrapped, func, **kwargs_c):
    """
    Return value and command arguments setup
    """
    wrapped.result_type = kwargs_c['result_type']
    (args, varargs, keywords, defaults) = inspect.getargspec(func)
    wrapped.__dict__['arguments'] = []
    wrapped.__dict__['arguments_type'] = {}
    wrapped.__dict__['function_name'] = func.__name__
    wrapped.__dict__['choices'] = {}
    for name_arg in filter(lambda x: x in kwargs_c, args):
        wrapped.choices[name_arg] = kwargs_c[name_arg]
    bias = 1 if 'self' in args else 0  # if first arg is self, see from second
    for index, name in enumerate(args[bias:]):
        wrapped.arguments.append((name, defaults[index]))
        wrapped.arguments_type[name] = utils.get_command_argument_type(defaults[index])


def command(*argv_c, **kwargs_c):
    """
    Use this decorator to create :class:`~alphalogic_api.objects.command.Command` object.

    Example 1::

        # The command returns True every time
        @command(result_type=bool)
        def cmd_exception(self):
            # do smth
            return True

    Example 2::

        # The command has three arguments and returns 'where' argument value
        @command(result_type=bool)
        def cmd_alarm(self, where='here', when=datetime.datetime.now(), why=2):
            return where

    Example 3::

        # The command hasn't arguments and return dict type
        @command(result_type=dict)
        def cmd_alarm(self):
            return {'a': 1, 'b': 'second', 'c': [1,2,3], 'd' : [1, {'2': 3}, 3]}


    :arg result_type: Command return type
    """
    def decorator(func):
        def wrapped(device, *argv, **kwargs):
            try:
                result = func(device, *argv, **kwargs)
                device.__dict__[wrapped.function_name].set_result(result)
                return result
            except Exception as err:
                t = traceback.format_exc()
                log.error(u'Command: function exception: {0}'.format(decode_string(t)))
                try:
                    device.__dict__[wrapped.function_name].set_exception(decode_string(t))
                except Exception as err:
                    t = traceback.format_exc()
                    log.error(u'Command: Exception in exception: {0}'.format(decode_string(t)))

        command_preparation(wrapped, func, **kwargs_c)
        return wrapped
    return decorator


def run(*argv_r, **kwargs_r):
    """
    | This function is used to be called periodically by the gRPC process.
    | It can be defined inside the Object class body to implement some repeatable tasks like
    | interrogation of the controller, modem, database, etc.
    | It is required to specify the necessary trigger period in seconds in the argument of the function.
    | Name of this function should not be started with ``_``.

    Example: ::

        # Called every 1 second.
        # You can change period by changing 'period_one' parameter.

        @run(period_one=1)
        def run_one(self):
            self.counter.val += 1

    | Synchronization
    | All functions wrapped in ``@run`` decorator may be called simultaneously in a thread pool.
    | However, ``Object`` has ``mutex`` attribute for synchronization between ``@run`` functions
    | defined in one Object instance.
    | They are also synchronized with ``handle_before_remove_device()``.
    | ``handle_before_remove_device()`` can be called only after the end of the last call
    | of any ``@run`` functions of the object.
    | Note however, that there's no any synchronization between ``@run`` functions
    | and object's constructor, ``handle_defaults_loaded()``, ``handle_prepare_for_work()``,
    | ``handle_get_available_children()`` and also between different Object instances.
    """
    def decorator(func):
        def wrapped(device, call_again=False):
            with device.mutex:
                if not device.flag_removing:
                    try:
                        status_perform = True
                        time_start = time.time()
                        try:
                            func(device)
                        except Exception as err:
                            t = traceback.format_exc()
                            log.error(u'Run function exception: {0}'.format(decode_string(t)))

                        time_finish = time.time()
                        time_spend = time_finish-time_start
                        log.info('run function {0} of device {2} was executed for {1} seconds'.
                                 format(func.func_name, time_spend, device.id))

                        period = getattr(device, kwargs_r.keys()[0]).val
                        func.__dict__['mem_period'] = period

                    except Exception as err:
                        t = traceback.format_exc()
                        log.error(u'system error in run decorator: {0}'.format(decode_string(t)))
                        status_perform = False
                    finally:
                        if not status_perform:
                            mem_period = func.__dict__['mem_period'] \
                                if 'mem_period' in func.__dict__ \
                                else kwargs_r.values()[0]
                        else:
                            mem_period = period

                        if call_again:
                            if time_spend < mem_period:
                                device.manager.tasks_pool.add_task(time_finish + mem_period - time_spend,
                                                                   getattr(device, func.func_name))
                            else:
                                device.manager.tasks_pool.add_task(time_finish, getattr(device, func.func_name))

        wrapped.runnable = True
        wrapped.period_name = kwargs_r.keys()[0]
        wrapped.period_default_value = kwargs_r.values()[0]
        return wrapped
    return decorator