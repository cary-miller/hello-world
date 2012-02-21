

def coroutine(func):
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start



@coroutine
def grep(pattern):
    print "Looking for %s" % pattern
    try:
        while True:
            line = (yield)
            if pattern in line:
                yield line
    except GeneratorExit:
        print "Going away. Goodbye"



# Example use
if __name__ == '__main__':
    g = grep("python")
    h = grep("yemp")
    g.send("Yeah, but no, but yeah, but no\n")
    g.send("A series of tubes\n")
    g.send("python generators rock!\n")
    x = g.send("python generators rock!\n")
    y = h.send("yemp generators rock!")
    x = g.send("python yemp rock!")
    g.close()

    
import sys
import time
from deco_global import _memoize


# For popping into Fred code.
def auto_update(ugly, time_limit=60*60):
    t0 = 0
    while True:
        if time.time()-t0 > time_limit:
            blah = ugly()
            t0 = time.time()
        yield blah

'''        
f = auto_update(ugly_cmpl_query)
f.next()['route'][23456]  
f.next()['route'][46352]  

But then I thought of something maybe simpler.  Why not just add a
timeout parameter to memoize.
BAM!  Done.  And very slick too.
'''        



# coroutine to produce intermittent output to logfile.
# Have it read some file every few seconds/minutes, read a random line,
# and print that line to some `log` file.  Then use that `log` file as the
# input to something else.
import random
def random_string(fname = '/private/var/log/system.log'):
    source = open(fname).readlines()
    while True:
        yield random.choice(source)

# TODO this is the problem.  time.sleep blocks anything from happening.
# I want non-blocking time.sleep.
# Good luck with that.
def random_interval(mean=10, sd=3): # seconds
    while True:
        yield time.sleep(abs(random.gauss(mean, sd)))

import time
def log_sim_n(sink=sys.stdout):
    rs = random_string()        
    ri = random_interval(1)
    while True:
        sink.write(rs.next())
        sink.write(str(time.time()))
        ri.next()

# TODO  This emits messages randomly which is what I want but it does not
# relenquish control to command line between emissions.
def log_sim(sink=sys.stdout):
    rs = random_string()        
    ri = random_interval(1)
    while True:
        yield sink.write(rs.next())
        ri.next()
#


# A class with a write method for simulating a file open for writing.
# Could be useful in a pipeline?  Is possible to do same with attaching a
# write method to a function?  Of course.  How about a function that
# attaches a write method to itself?

class Fileish(object):
    '''
    A file-like object,  with read/write methods.
    The write method is for writing TO this object.  Backwards from how I
    usually think of read/write but totally makes sense to a user.

    REDIRECTING sys.stdout WRITES TO THIS OBJECT.
    >>> f = Fileish()
    >>> sys.stdout = f
    >>> print 'yoohoo'
    >>> sys.stdout = sys.__stdout__
    >>> f.read()
    yoohoo
    '''
    def __init__(self):
        self.s = ''

    def write(self, s):
        assert type(s) == str, s
        # What shall we do with string s?
        self.s += s
        # For now just save it.

    def read(self):
        # Write self.s to someplace.  
        return self.s

    def clear(self):
        self.s = ''





f = Fileish()
f.write('hello\n')
f.write('there\n')
print f.read()
ls = log_sim(sink=f)
ls.next()
ls.next()
f.write('sucker\n')
ls.next()
ls.next()
print f.read()

# The problem with log_sim is blocking time.sleep.

import Queue
import threading
import datetime

class ThreadClass2(threading.Thread):
    def run(self):
        now = datetime.datetime.now()
        print '%s ... %s' %(self.getName(), now)
        ls = log_sim_n(f)



class ThreadClass3(threading.Thread):
    '''Run long-running func in a thread while we do other crap in
    the foreground.
    '''

    def __init__(self, f, *arg, **kw):
        self.f = f
        self.arg = arg
        self.kw = kw

    def run(self):
        self.result = self.f(*self.arg, **self.kw)




t = ThreadClass2()
t.setDaemon(True)
t.start()
# Wow.  This joker now works.  With the thread I have non-blocking
# intermittent input to f.
# So f receives erratic input.  Super.
# Gee whiz.  This would be a really good way to run tedious jobs.


