# -*- coding: utf-8 -*-
__author__ = 'dontsov'

import os
import sys
import argparse
from logging import getLogger, StreamHandler, Formatter, getLevelName, CRITICAL
from logging.handlers import RotatingFileHandler

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

parser.add_argument('--log_directory', default=log_directory, help='Log files directory. Now: {}'.format(log_directory))
args = parser.parse_args()

if args.help:
    print parser.format_help()
    sys.exit(1)

host = args.h
port = args.p


class Logger(object):
    def __init__(self):
        log = getLogger('')

        if args.log_level == 'off':
            log.setLevel(CRITICAL)  # иначе сообщение, что нет хэндлеров
        else:
            log.setLevel(getLevelName(args.log_level.upper()))

            log_path = os.path.join(os.path.pardir, 'logs')

            if not os.path.isdir(log_path):
                os.makedirs(log_path)

            fh = RotatingFileHandler(os.path.join(log_path, "stub.log"),
                                     maxBytes=args.log_max_file_size,
                                     backupCount=args.log_max_files)
            fh.setLevel(getLevelName(args.log_level.upper()))

            formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)

            log.addHandler(fh)

            # Задействовать консоль для вывода лога
            console = sys.stderr
            if console is not None:
                # Вывод лога производится и на консоль и в файл (одновременно)
                console = StreamHandler(console)
                console.setLevel(getLevelName(args.log_level.upper()))
                console.setFormatter(formatter)
                log.addHandler(console)


Logger()
log = getLogger('')
