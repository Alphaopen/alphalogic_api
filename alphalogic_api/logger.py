# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import sys
from logging import getLogger, StreamHandler, Formatter, getLevelName, CRITICAL
from logging.handlers import RotatingFileHandler
from alphalogic_api import options


class AlphaRotatingFileHandler(RotatingFileHandler):
    """
    Assigns filenames like "stub.1.log" instead of "stub.log.1" as original RotatingFileHandler does
    """

    def doRollover(self):
        if self.stream:
            self.stream.close()
            self.stream = None

        file_name, file_ext = os.path.splitext(self.baseFilename)

        if self.backupCount > 0:
            for i in range(self.backupCount - 1, 0, -1):
                sfn = "{}.{}{}".format(file_name, i, file_ext)
                dfn = "{}.{}{}".format(file_name, i + 1, file_ext)

                if os.path.exists(sfn):
                    # print "%s -> %s" % (sfn, dfn)
                    if os.path.exists(dfn):
                        os.remove(dfn)
                    os.rename(sfn, dfn)

            dfn = file_name + ".1" + file_ext;

            if os.path.exists(dfn):
                os.remove(dfn)
            # Issue 18940: A file may not have been created if delay is True.
            if os.path.exists(self.baseFilename):
                os.rename(self.baseFilename, dfn)
        if not self.delay:
            self.stream = self._open()


class Logger(object):
    def __init__(self):
        log = getLogger('')

        if options.args.log_level == 'off':
            log.setLevel(CRITICAL)  # otherwise warning message 'no handlers'
        else:
            log_level = options.args.log_level.upper()

            # logging doesn't support trace level, which is used in adapters, assign it to debug
            if log_level == "TRACE":
                log_level = b"DEBUG"

            log.setLevel(getLevelName(log_level))

            if not os.path.isdir(options.args.log_directory):
                os.makedirs(options.args.log_directory)

            fh = AlphaRotatingFileHandler(os.path.join(options.args.log_directory, "stub.log"),
                                          maxBytes=options.args.log_max_file_size,
                                          backupCount=options.args.log_max_files)
            fh.setLevel(getLevelName(log_level))

            formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)

            log.addHandler(fh)

            # Use console for log output
            if not (options.args.noconsole or os.getenv('NOCONSOLE') == '1'):
                console = sys.stderr
                if console is not None:
                    # Logging to console and file both
                    console = StreamHandler(console)
                    console.setLevel(getLevelName(log_level))
                    console.setFormatter(formatter)
                    log.addHandler(console)


log = getLogger('')
