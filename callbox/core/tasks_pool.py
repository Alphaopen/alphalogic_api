# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool as ProcessPool
from threading import Thread, Timer, Event
from Queue import Queue, PriorityQueue
import time
import signal

#1) Подход через таймеры
#2) Подход через один тред, который запускает готовые задачи

# Внутри рабочего потока нужно узанвать сколько времени выполнялась задача, это можно сделать через декоратор
# Чтобы потом стало известно на сколько запускать

class TasksPool(object):

    def __init__(self, is_thread=True, num_thread=None):
        self.thread_pool = ThreadPool(processes=num_thread) if is_thread else ProcessPool(processes=num_thread)
        # если processes=None, то количество поток подбирается автоматически
        self.operation_thread = Thread(target=self.run_operation_thread)
        self.shutdown_flag = Event()
        self.queue_tasks = Queue() # здесь задачи, которые нужно выполнить немедленно
        self.queue_timers = PriorityQueue() # здесь задачи с временными отметками
        self.operation_thread.start()


    def run_operation_thread(self):
        while not self.shutdown_flag.is_set():
            #TODO:
            #проверяет есть ли подешедшии задачи в queue_timers
            #распределяет подошеднии задачи между потоками, queue_tasks
            #заснуть в конце на миллисекунду
        print 'a exit'


    def add_task(self, time_stamp, task):
        self.queue_timers.put((time_stamp, task))



