# -*- coding: utf-8 -*-
import os
import sys
import argparse

log_levels = ['trace',
              'debug',
              'info',
              'warning',
              'error',
              'off']

log_directory = os.path.join(os.getcwd(), 'logs')

parser = argparse.ArgumentParser(description='Alphalogic Adapter Stub', add_help=False)
parser.add_argument('--help', action='store_true', help='Print help')
parser.add_argument('-h', default='localhost', help='Set host (default 127.0.0.1)')
parser.add_argument('-p', default=42001, type=int, help='Set port (default 42001)')
parser.add_argument('-l', '--log_level', default='info', type=str.lower, choices=log_levels)
parser.add_argument('--log_max_file_size', type=int, default=1024*100, help='Set max file size for rotating log file, bytes. Default: 100кб')
parser.add_argument('--log_max_files', type=int, default=10, help='Set max files for rotating log file. Default=10')
parser.add_argument('--development_mode', action='store_true', help='Don\'t check configure if present')
parser.add_argument('--log_directory', default=log_directory, help='Log files directory. Now: {}'.format(log_directory))
args = parser.parse_args()

if args.help:
    print parser.format_help()
    sys.exit(1)

if args.development_mode:
    print '* * * * * * * * * * * * * * * * * *\n' \
          '* * * !! DEVELOPMENT MODE !!  * * *\n' \
          '* * * * * * * * * * * * * * * * * *'

host = args.h
port = args.p

from alphalogic_api.core.type_attributes import Visible, Access, Priority

from alphalogic_api.core.core import Root, Device
from alphalogic_api.core.command import command
from alphalogic_api.core.event import Event, MajorEvent, MinorEvent, CriticalEvent, BlockerEvent, TrivialEvent
from alphalogic_api.core.parameter import Parameter, ParameterBool, ParameterInt, \
    ParameterDouble, ParameterDatetime, ParameterString
from alphalogic_api.core import utils
from alphalogic_api.core.run_function import run
from alphalogic_api import host, port
from alphalogic_api.core.exceptions import ComponentNotFound, RequestError, exception_info
