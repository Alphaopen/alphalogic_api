# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool as ProcessPool
from threading import Thread, Timer, Event, Lock
from Queue import Queue, PriorityQueue
import time
import signal
from callbox.logger import log


class PriorityTasks(object):
    '''
    Этот класс выдает задачи, которые нужно выполнять в данный момент.
    '''
    def __init__(self):
        self.peak = None
        self.queue = PriorityQueue()
        self.mutex = Lock()

    def get_tasks(self, current_time):
        with self.mutex:
            if self.peak is None:
                return None
            elif current_time < self.peak[0]:
                return None
            else:
                result = [self.peak[1]]
                self.peak = None
                while not(self.queue.empty()):
                    tmp = self.queue.get()
                    if current_time >= tmp[0]:
                        result.append(tmp[1])
                    else:
                        self.peak = tmp
                        break
                return result

    def put(self, item):
        with self.mutex:
            if self.peak is None:
                self.peak = item
            elif item[0] < self.peak[0]:
                self.queue.put(self.peak)
                self.peak = item
            else:
                self.queue.put(item)

    def empty(self):
        with self.mutex:
            if (self.peak is None) and (self.queue.empty()):
                return True
            else:
                return False


class TasksPool(object):
    '''
    Распределяет задачи по пулу потоков
    '''
    def __init__(self, is_thread=True, num_thread=None):
        self.thread_pool = ThreadPool(processes=num_thread) if is_thread else ProcessPool(processes=num_thread)
        # если processes=None, то количество поток подбирается автоматически
        self.operation_thread = Thread(target=self.run_operation_thread)
        self.shutdown_flag = Event()
        self.queue_tasks = PriorityTasks() # здесь задачи с временными отметками
        self.operation_thread.start()

    def run_operation_thread(self):
        while not self.shutdown_flag.is_set():
            tasks = self.queue_tasks.get_tasks(time.time())
            if not(tasks is None):
                self.thread_pool.map_async(lambda f: f(), tasks)
            time.sleep(0.001)#заснуть в конце на миллисекунду
        log.info('run_operation_thread close')

    def add_task(self, time_stamp, task):
        print 'add_task'
        self.queue_tasks.put((time_stamp, task))


def run(period=60):
    def decorator(func):
        def wrapped(device):
            time_start = time.time()
            func(device)
            time_finish = time.time()
            if (time_finish-time_start) < wrapped.runable:
                print 'A case {0}\n'.format(time_finish-time_start)
                device.manager.tasks_pool.add_task(time_finish+period-(time_finish-time_start),
                                                   getattr(device, func.func_name))
            else:
                print 'B case {0}\n'.format(time_finish - time_start)
                device.manager.tasks_pool.add_task(time_finish, getattr(device, func.func_name))
        wrapped.runable = decorator.period
        return wrapped
    decorator.period = period
    return decorator


