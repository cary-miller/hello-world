# cobroadcast.py
#
# An example of broadcasting a data stream onto multiple coroutine targets.

from coroutine import coroutine

# A data source.  This is not a coroutine, but it sends
# data into one (target)

import time
def follow(thefile, f_target):
    thefile.seek(0,2)      # Go to the end of the file
    while True:
         line = thefile.readline()
         if not line:
             time.sleep(0.1)    # Sleep briefly
             continue
         f_target.send(line) # send to a coroutine.

# A filter.
@coroutine
def grep(pattern, f_target):
    while True:
        line = (yield)           # Receive a line
        if pattern in line:
            f_target.send(line)    # Send to next stage




# A sink.  A coroutine that receives data
@coroutine
def printer():
    while True:
         line = (yield) # target.send lands here
         print line,

# Broadcast a stream onto multiple targets
@coroutine
def broadcast(l_targets):
    while True:
        item = (yield) # target.send lands here
        for f_target in l_targets:
            f_target.send(item) # send to another coroutine.

# Example use
def b_cast1():
    f = open("access-log")
    follow(f,
       broadcast([grep('python',printer()),
                  grep('ply',printer()),
                  grep('swig',printer())])
           )


# Alt use (broadcast2)
# An example of broadcasting a data stream onto multiple coroutine targets.
# This example shows "fan-in"---a situation where multiple coroutines
# send to the same target.
def b_cast2():
    f = open("access-log")
    p = printer()
    follow(f,
       broadcast([grep('python', p),
                  grep('ply', p),
                  grep('swig', p)])
           )







