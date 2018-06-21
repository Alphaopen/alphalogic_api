# -*- coding: utf-8 -*-
import datetime
import callbox.protocol.rpc_pb2 as rpc_pb2

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
    elif 'list' in str(type(value)):
        return 'list'

def create_command_definer(result_type_str):
    if 'str' in result_type_str:
        return 'create_string_command'
    elif 'int' in result_type_str:
        return 'create_int_command'
    elif 'float' in result_type_str:
        return 'create_double_command'
    elif 'datetime' in result_type_str:
        return 'create_datetime_command'
    elif 'bool' in result_type_str:
        return 'create_bool_command'

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