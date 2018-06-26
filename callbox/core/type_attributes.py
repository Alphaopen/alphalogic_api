# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from enum import Enum
import datetime

class runtime(object):
    pass

class setup(object):
    pass

class hidden(object):
    pass

class common(object):
    pass

class read_only(object):
    pass

class read_write(object):
    pass

class EventPriority(object):
    TRIVIAL = 'set_trivial'
    MINOR = 'set_minor'
    MAJOR = 'set_major'
    CRITICAL = 'set_critical'
    BLOCKER = 'set_blocker'
