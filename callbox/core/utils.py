# -*- coding: utf-8 -*-
import datetime

def milliseconds_from_epoch(dt):
    return int((dt - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)



def value_field_definer(value):
    if 'str' in str(type(value)):
        return 'string_value'
    elif 'int' in str(type(value)):
        return 'int64_value'
    elif 'float' in str(type(value)):
        return 'double_value'
    elif 'datetime' in str(type(value)):
        return 'datetime_value'
    elif 'bool' in str(type(value)):
        return 'bool_value'
