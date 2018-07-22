# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from type_attributes import Visible, Access, Priority
from alphalogic_api.logger import log
from alphalogic_api.core.exceptions import exception_info
from alphalogic_api.core.utils import decode_string, Exit

class ConfigureInspector(object):


    def is_parameter_exist(self, name, object):
        try:
            parameter = object.parameter(name)
            return parameter
        except Exception, err:
            return None

    def check_parameter_accordance(self, parameter_model):
        try:
            id_parameter = parameter_model.id
            #1 check value_type
            if parameter_model.value_type is bool and not(parameter_model.is_bool()):
                raise Exception('Real and model type are different')
            elif parameter_model.value_type is int and not(parameter_model.is_int()):
                raise Exception('Real and model type are different')
            elif parameter_model.value_type is float and not(parameter_model.is_double()):
                raise Exception('Real and model type are different')
            elif parameter_model.value_type is datetime.datetime and not(parameter_model.is_datetime()):
                raise Exception('Real and model type are different')
            elif parameter_model.value_type is unicode and not(parameter_model.is_string()):
                raise Exception('Real and model type are different')

            #2 check visible
            if parameter_model.visible == Visible.runtime and not(parameter_model.is_runtime()):
                raise Exception('Real and model visible are different')
            elif parameter_model.visible == Visible.setup and not(parameter_model.is_setup()):
                raise Exception('Real and model visible are different')
            elif parameter_model.visible == Visible.hidden and not(parameter_model.is_hidden()):
                raise Exception('Real and model visible are different')
            elif parameter_model.visible == Visible.common and not(parameter_model.is_common()):
                raise Exception('Real and model visible are different')

            #3 check access
            if parameter_model.access == Access.read_only and not(parameter_model.is_read_only()):
                raise Exception('Real and model access are different')
            elif parameter_model.access == Access.read_write and not(parameter_model.is_read_write()):
                raise Exception('Real and model access are different')

            #4 enums
            # Пока проверка только на соотвествие enums, позже на последовательность enums
            model_choices = parameter_model.choices
            real_choices = parameter_model.enums()
            if model_choices is None and len(real_choices)!=0:
                raise Exception('Real and model enums are different')
            elif model_choices is not None:
                if len(model_choices) != len(real_choices):
                    raise Exception('Real and model enums are different')
                else:
                    if type(model_choices[0]) is not tuple:
                        model_vals = sorted(model_choices)
                        real_vals  = sorted(zip(*real_choices)[0])
                        if model_vals != real_vals:
                            raise Exception('Real and model enums are different')
                    else:
                        model_vals, model_keys = zip(*model_choices)
                        model_vals, model_keys = sorted(model_vals), sorted(model_keys)
                        real_vals, real_keys = zip(*real_choices)
                        real_vals, real_keys = sorted(real_vals), sorted(real_keys)
                        if model_vals != real_vals or model_keys != real_keys:
                            raise Exception('Real and model enums are different')
        except Exception, err:
            exception_info()
            log.error('Parameter discrepancy {0}'.format(parameter_model.parameter_name))
            raise Exit


        #if parameter_model.has_e

    def is_event_exist(self, name, object):
        try:
            event = object.event(name)
            return event
        except Exception, err:
            return None

    def check_event_accordance(self, event_model):
        try:
            id_event = event_model.id
            #1 check priority
            if event_model.priority == Priority.blocker and not(event_model.is_blocker()):
                raise Exception('Real and model priority are different')
            elif event_model.priority == Priority.critical and not(event_model.is_critical()):
                raise Exception('Real and model priority are different')
            elif event_model.priority == Priority.major and not(event_model.is_major()):
                raise Exception('Real and model priority are different')
            elif event_model.priority == Priority.minor and not(event_model.is_minor()):
                raise Exception('Real and model priority are different')


            #2 enums
            # Можно проверить только на соотвествие имен
            model_choices = list(zip(*event_model.arguments)[0])
            real_choices = event_model.argument_list()
            if model_choices != real_choices:
                raise Exception('Real and model arguments are different')
            '''
            if model_choices is None and len(real_choices)!=0:
                raise Exception('Real and model enums are different')
            elif model_choices is not None:
                if len(model_choices) != len(real_choices):
                    raise Exception('Real and model enums are different')
                else:
                    if type(model_choices[0]) is not tuple:
                        model_vals = sorted(model_choices)
                        real_vals  = sorted(zip(*real_choices)[0])
                        if model_vals != real_vals:
                            raise Exception('Real and model enums are different')
                    else:
                        model_vals, model_keys = zip(*model_choices)
                        model_vals, model_keys = sorted(model_vals), sorted(model_keys)
                        real_vals, real_keys = zip(*real_choices)
                        real_vals, real_keys = sorted(real_vals), sorted(real_keys)
                        if model_vals != real_vals or model_keys != real_keys:
                            raise Exception('Real and model enums are different')
            '''
        except Exception, err:
            exception_info()
            log.error('Parameter discrepancy {0}'.format(event_model.name()))
            raise Exit