# -*- coding: utf-8 -*-

from alphalogic_api.objects.device import Root, Device
from alphalogic_api.objects.command import Command
from alphalogic_api.objects.event import Event, MajorEvent, MinorEvent, CriticalEvent, BlockerEvent, TrivialEvent
from alphalogic_api.objects.parameter import Parameter, ParameterBool, ParameterInt, \
    ParameterDouble, ParameterDatetime, ParameterString