# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.type_attributes import runtime, setup, hidden, common
from callbox.core.type_attributes import read_only, read_write
import locale

def milliseconds_from_epoch(dt):
    return int((dt - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)

def value_type_field_definer(value_type):
    if 'unicode' in str(value_type):
        return 'string_value'
    elif 'int' in str(value_type):
        return 'int64_value'
    elif 'float' in str(value_type):
        return 'double_value'
    elif 'datetime' in str(value_type):
        return 'datetime_value'
    elif 'bool' in str(value_type):
        return 'bool_value'
    elif 'list' in str(value_type):
        return 'list'

def value_field_definer(value):
    if 'unicode' in str(type(value)):
        return 'string_value'
    elif 'int' in str(type(value)):
        return 'int64_value'
    elif 'float' in str(type(value)):
        return 'double_value'
    elif 'datetime' in str(value):
        return 'datetime_value'
    elif 'bool' in str(value):
        return 'bool_value'
    elif 'list' in str(value):
        return 'list'

def create_command_definer(result_type_str):
    if 'unicode' in result_type_str:
        return 'create_string_command'
    elif 'int' in result_type_str:
        return 'create_int_command'
    elif 'float' in result_type_str:
        return 'create_double_command'
    elif 'datetime' in result_type_str:
        return 'create_datetime_command'
    elif 'bool' in result_type_str:
        return 'create_bool_command'

def create_parameter_definer(result_type_str):
    if 'unicode' in result_type_str:
        return 'create_string_parameter'
    elif 'int' in result_type_str:
        return 'create_int_parameter'
    elif 'float' in result_type_str:
        return 'create_double_parameter'
    elif 'datetime' in result_type_str:
        return 'create_datetime_parameter'
    elif 'bool' in result_type_str:
        return 'create_bool_parameter'

def set_visible_definer(visible_type):
    if visible_type==runtime:
        return 'set_runtime'
    elif visible_type==setup:
        return 'set_setup'
    elif visible_type==hidden:
        return 'set_hidden'
    elif visible_type==common:
        return 'set_common'

def set_access_definer(access_type):
    if access_type==read_only:
        return 'set_read_only'
    elif access_type==read_write:
        return 'set_read_write'

def decode_string(s):
    """
    Функция создает unicode из s, пытаясь угадать кодировку.
    """
    if isinstance(s, unicode):
        return s  # Если это не строка вовсе, то ничего не делаем

    for codec in [locale.getpreferredencoding(), 'utf8', 'cp1251', 'cp1252']:
        try:
            return s.decode(codec)
        except:
            pass
    # Если ничего не осталось
    return unicode(s)

def get_rpc_value(value_type, value=None):
    value_rpc = rpc_pb2.Value()

    if value_type == int:
        value_rpc.int64_value = value if value else 0
    elif value_type == str:
        value_rpc.string_value = value if value else ''
    elif value_type == float:
        value_rpc.double_value = value if value else 0.0
    elif value_type == datetime.datetime:
        if value:
            value_rpc.datetime_value = int((value - datetime.datetime(1970, 1, 1, 0, 0, 0)).total_seconds()) * 1000 \
                                       + value.microsecond / 1000
        else:
            value_rpc.datetime_value = 0
    elif value_type == bool:
        value_rpc.bool_value = value if value else False

    return value_rpc