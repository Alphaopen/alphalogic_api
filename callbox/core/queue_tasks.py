# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import threading, queue, time
from threading import Condition, Thread

class QueueTasks(object):

    def __init__(self):
        self.dataQueue = queue.Queue()

        t = threading.Thread(target=self.run_loop)
        t.start()

    def run_loop(self):
        while True: # сделать прерывание этого цикла
            task = self.dataQueue.get()
            task()

tot = QueueTasks()

def run(*argv_c, **kwargs_c):
    def decorator(device, func):
        func(device)
    #decorator.period = kwargs_c['period']
    #tot.dataQueue.put(lambda : decorator())
    ## add_periodic_tasks
    return decorator


