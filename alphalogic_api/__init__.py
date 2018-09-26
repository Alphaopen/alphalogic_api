# -*- coding: utf-8 -*-

from alphalogic_api.logger import log
from alphalogic_api.logger import Logger
from logging import getLogger
from alphalogic_api import options


VERSION_MAJOR = 0  # (System version)
VERSION_MINOR = 0  # (Tests version)
BUILD_NUMBER = 11   # (Issues version)

__version__ = '.'.join(map(str, (VERSION_MAJOR, VERSION_MINOR, BUILD_NUMBER)))


def init():
    """
    Initialize function. Should be run before Root object created.
    :return: host, port
    """
    global log

    options.parse_arguments()
    Logger()
    log = getLogger('')

    return options.args.host, options.args.port
