# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import locale
import datetime
import callbox.protocol.rpc_pb2 as rpc_pb2
from callbox.core.type_attributes import runtime, setup, hidden, common
from callbox.core.type_attributes import read_only, read_write
from callbox.logger import log
import inspect


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

'''
to do :
Можно сократить
'''
def value_field_definer(value):
    if 'unicode' in str(type(value)):
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
    elif 'tuple' in str(type(value)):
        return 'tuple'


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


def get_command_argument_type(arg):
    if type(arg) == tuple:
        for val_type in arg:
            if type(val_type) == dict:
                val_dict = val_type.values()[0]
                return type(val_dict)
            else:
                return type(val_type)
    else:
        return type(arg)


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


def milliseconds_from_epoch(dt):
    return int((dt - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000)


def get_rpc_value(value_type, value=None):
    value_rpc = rpc_pb2.Value()

    if value_type == int:
        value_rpc.int64_value = value if value else 0
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
    elif value_type == unicode:
        value_rpc.string_value = value if value else ''
    elif value_type == str:
        raise Exception('\'str\' type using is prohibited')

    return value_rpc


def value_from_rpc(value_rpc, value_type):

    if 'unicode' in str(value_type):
        return value_rpc.string_value
    elif 'int' in str(value_type):
        return value_rpc.int64_value
    elif 'float' in str(value_type):
        return value_rpc.double_value
    elif 'datetime' in str(value_type):
        return datetime.datetime.utcfromtimestamp(value_rpc.datetime_value / 1000) \
                    + datetime.timedelta(milliseconds=value_rpc.datetime_value % 1000)
    elif 'bool' in str(value_type):
        return value_rpc.bool_value
    elif 'list' in str(value_type):
        pass   # TODO return value_rpc.list
    elif 'tuple' in str(value_type):
        pass   # TODO


class Exit(Exception):
    pass


def shutdown(signum, frame):
    log.info("Shutdown. Signal is {0}".format(signum))
    raise Exit

def get_class_name_from_str(self, class_name_str):
    frame = inspect.currentframe()
    while frame:
        if class_name_str in frame.f_locals:
            return frame.f_locals[class_name_str]
        frame = frame.f_back
    raise Exception('{0} is not a class of device'.format(class_name_str))