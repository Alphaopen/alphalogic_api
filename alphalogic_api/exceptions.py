# -*- coding: utf-8 -*-
from __future__ import unicode_literals


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
    If component not found in the Object
    """
    def __init__(self, msg):
        super(ComponentNotFound, self).__init__(msg)


class TimeoutError(Exception):
    """
    gRPC request timeout. See --timeout argument
    """
    def __init__(self, msg):
        super(TimeoutError, self).__init__(msg)


class ConnectError(Exception):
    """
    gRPC can't connect to Stub
    """
    def __init__(self, msg):
        super(ConnectError, self).__init__(msg)


class Exit(Exception):
    pass
