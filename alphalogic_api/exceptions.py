# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import linecache
import traceback
from alphalogic_api.logger import log

class IncorrectRPCRequest(Exception):
    """
    Unsupported request by protocol. Check alphalogic_api code
    """
    def __init__(self, msg):
        super(IncorrectRPCRequest, self).__init__(msg)


class RequestError(Exception):
    """
    gRPC call exception
    """
    def __init__(self, msg):
        super(RequestError, self).__init__(msg)


class ComponentNotFound(Exception):
    """
    If component not found in the Device
    """
    def __init__(self, msg):
        super(ComponentNotFound, self).__init__(msg)


class Exit(Exception):
    pass


def exception_traceback(message):
    """
    Writes filename and line of exception
    """
    log.error(message)
    log.error(traceback.format_exc())
