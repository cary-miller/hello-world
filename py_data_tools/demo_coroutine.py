from coroutine import coroutine


#import gevent
#import gevent.monkey
#gevent.monkey.patch_socket()
#gevent.monkey.patch_all()
#gevent.monkey.patch_all(httplib=True)

import requests  # because urllib2 sucks
import grequests

@coroutine
def printer_status():
    ''' A sink.  A coroutine that receives data.  '''
    while True:
        host = (yield) # target.send lands here
        response = requests.get('http://'+host)
        print host, response.status_code

@timeit
def sequential1():
    ps = printer_status()
    for host in hosts:
        ps.send(host)


@timeit
def parallel1(n):
    ps_list=[]
    for i in range(n):
        ps_list.append(printer_status())
    i=0
    for host in hosts:
        ps_list[i%n].send(host)
        print i, i%n, 
        i+=1



@timeit
def parallel2(n):
    rs = [grequests.get('http://'+host) for host in hosts[:n]]
    res = grequests.map(rs)


@timeit
def sequential2(n):
    rs = [grequests.get('http://'+host) for host in hosts[:n]]
    for r in rs: 
        r.send()
        print r.url
    
if 0:
    def f_local(word):
        print word
        time.sleep(3)

    @timeit
    def parallel(n):
        rs = [f('http://'+host) for host in hosts[:n]]
        res = grequests.map(rs)


    @timeit
    def sequential(n):
        rs = [grequests.get('http://'+host) for host in hosts[:n]]
        for r in rs: 
            r.send()
            print r.url
     




