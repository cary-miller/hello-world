import time
import requests
import Queue
import threading
from util import timeit


def fetch(host):
    url = requests.get('http://'+host)
    print 'req ', host


def sleeper(host):
    time.sleep(1)
    print 'req ', host
    


@timeit
def sequential(n, func):
    for host in hosts[:n]:
        doc = func(host)


@timeit
def parallel(n, func, nthread):
    queue = Queue.Queue()

    # spawn a pool of threads, and pass them queue instance 
    for i in range(nthread):
        t = ThreadUrl(queue, func)
        t.setDaemon(True)
        t.start()

    # populate the queue 
    for host in hosts[:n]:
        queue.put(host)

    # wait until everything has been processed     
    queue.join()



class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, func):
        threading.Thread.__init__(self)
        self.queue = queue
        self.func = func

    def run(self):
        while True:
            thing = self.queue.get() # get item from queue
            doc = self.func(thing)
            self.queue.task_done()



