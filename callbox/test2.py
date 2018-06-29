# -*- coding: utf-8 -*-

'взаимодействие потоков производителей и потребителей посредством очереди'
numconsumers = 2 # количество потоков-потребителей
numproducers = 4 # количество потоков-производителей
nummessages = 4 # количество сообщений, помещаемых производителем
import _thread as thread, queue, time
from core.queue_tasks import QueueTasks

def f(*args, **kwargs):
    for index,x in enumerate(args):
        print "{0}={1}".format(index, x)

    for x in kwargs:
        print "{0}={1}".format(x, kwargs[x])
    print 'round'

t = QueueTasks()

t.dataQueue.put(lambda: f(1,2))
t.dataQueue.put(lambda: f(1,2, hj=2, gld='asdf'))
t.dataQueue.put(lambda: f(1,2, kls=2))


'''
safeprint = thread.allocate_lock() # в противном случае вывод может
                                   # перемешиваться
dataQueue = queue.Queue()          # общая очередь неограниченного размера

def producer(idnum):
    for msgnum in range(nummessages):
        time.sleep(idnum)
        dataQueue.put('[producer id=%d, count=%d]' % (idnum, msgnum))

def consumer(idnum):
    while True:
        time.sleep(0.1)
        try:
            data = dataQueue.get(block=False)
        except queue.Empty:
            pass
        else:
            with safeprint:
                print('consumer', idnum, 'got =>', data)

if __name__ == '__main__':
    for i in range(numconsumers):
        thread.start_new_thread(consumer, (i,))

    for i in range(numproducers):
        thread.start_new_thread(producer, (i,))

    time.sleep(((numproducers-1) * nummessages) + 1)
    print('Main thread exit.')
'''