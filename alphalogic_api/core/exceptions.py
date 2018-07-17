# -*- coding: utf-8 -*-


class IncorrectRPCRequest(Exception):

    def __init__(self, msg):
        super(IncorrectRPCRequest, self).__init__(msg)


class RequestError(Exception):

    def __init__(self, msg):
        super(RequestError, self).__init__(msg)


class ComponentNotFound(Exception):
    """
    If component not found in the Device
    """
    def __init__(self, msg):
        super(ComponentNotFound, self).__init__(msg)
