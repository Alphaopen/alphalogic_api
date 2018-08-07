# -*- coding: utf-8 -*-

from alphalogic_api.logger import log
from alphalogic_api.logger import Logger
from logging import getLogger
from alphalogic_api import options


def init():
    global log

    options.parse_arguments()
    Logger()
    log = getLogger('')

    return options.args.host, options.args.port