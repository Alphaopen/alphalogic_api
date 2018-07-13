# -*- coding: utf-8 -*-

import os
import sys
from logging import getLogger, StreamHandler, Formatter, getLevelName, CRITICAL
from logging.handlers import RotatingFileHandler
from callbox import args


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
