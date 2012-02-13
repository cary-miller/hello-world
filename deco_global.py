
# simplest possible do-nothing decorator #
def deco(f):
    def inner():
        return f()
    return inner


@deco
def f():
    x=22
    return 44



# simplest possible do-nothing decorator with argument #
def outer(arg):
    def deco(f):
        def inner():
            return f()
        return inner
    return deco


@outer('foo')
def g():
    x=22
    return 44


# simplest possible do-nothing class decorator #
class blah(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *a, **k):
        return self.func(*a, **k)


@blah
def h():
    x=22
    return 44


@blah
def factorial(n):
    assert n == int(n)
    assert n >= 0
    if n==0 or n==1: return 1
    return n*factorial(n-1)

# Does a decorator have access to locals() of the decorated func?
# NO.
# BUT  see functools.update_wrapper
import functools

# decorator that makes all locals global #
def globalize(f):
    def wrapper():
        print wrapper.__dict__
        functools.update_wrapper(wrapper, f)
        wrapper.__dict__ = f.__dict__
        print wrapper.__dict__
        globals().update(locals())
        return f()
        return f(*a, **k)
    return wrapper

@globalize
def i():
    x=22
    return 44



# Really nifty stuff from the decorator module.
import decorator
# Decorator module makes possible to define decorators in a different way with less nesting.
# Also does some good things about function signatures.

@decorator.decorator
def trace(f, *args, **kw):
    print 'calling %s with args %s, %s' % (f.func_name, args, kw)
    return f(*args, **kw)


@trace
def j(*args, **kw):
    x=22
    return 44

def trace1(f):
    def inner(*args, **kw):
        print 'calling %s with args %s, %s' % (f.func_name, args, kw)
        return f(*args, **kw)
    return inner

@trace1
def k():
    x=22
    return 44

# The benefit of decorator shows up when you start looking at func.__name__ and such.
# Or is that really a benefit?  One could spend lots of time tracking a bug that turns
# out to be in the decorator.
# LESSON:  be judicious with decorators.

#@decorator.decorator
def _memoize(func, *args, **kw):
    # The entire set of args and kw is the key.
    if kw: # frozenset to ensure hashability
        key = frozenset(args), frozenset(kw.iteritems())
    else:
        key = frozenset(args)
    cache = func.cache
    if key in cache:
        return cache[key]
    else:
        cache[key] = result = func(*args, **kw)
        return result

def memoize(f):
    f.cache = {}
    return decorator.decorator(_memoize, f)


from collections import defaultdict
import time
def memoize_timeout(timeout):
    def memo(f):
        f.cache = {}
        f.time = defaultdict(lambda:0)
        f.timeout = timeout
        func = f
        def _memo(*args, **kw):
            # The entire set of args and kw is the key.
            if kw: # frozenset to ensure hashability
                key = frozenset(args), frozenset(kw.iteritems())
            else:
                key = frozenset(args)
            cache = func.cache
            t = func.time
            if key in cache and key in t and time.time()-t[key] < func.timeout:
                return cache[key]
            else:
                cache[key] = result = func(*args, **kw)
                t[key] = time.time()
                return result
        return _memo
    return memo


# krebsonsecurity.com





# Enhanced memoize!  Adds a timeout to each key.
def memoize_(timeout=60*60):
    def memo(func):
        func.cache = {}
        def _memo(*args, **kw):
            # The entire set of args and kw is the key.
            # frozenset to ensure hashability
            key = frozenset(args), frozenset(kw.items())
            cache = func.cache
            if key in cache and time.time()-cache[key]['time'] < timeout:
                return cache[key]['value']
            else:
                result = func(*args, **kw)
                cache[key] = dict(value=result, time=time.time())
                return result
        return _memo
    return memo
# Next enhancement:  Check recalulated version for sanity before replacing
# cached value.  If recalc fails return the cached value.




import time

@memoize
def heavy_computation():
    time.sleep(2)
    return 'done'

if 0:
    a = heavy_computation()
    b = heavy_computation()

@memoize
def factorial(n):
    assert type(n) == int and n >= 0
    if n==0: return 1
    return n*factorial(n-1)

# Try class based memoize
class mem(object):
    def __init__(self, f):
        self.d={}
        self.f=f
    def __call__(self, *a, **k):
        key = a,((k,v) for (k,v) in k.items())
        d = self.d
        if key in d.keys():
            return d[key]
        else:
            d[key] = self.f(*a, **k)
            return d[key]
        
@mem
def factorial(n):
    assert n == int(n)
    assert n >= 0
    if n==0 or n==1: return 1
    return n*factorial(n-1)




def a():
    # No need for the -except- block
    try: 1/0
    finally: x=33
    # The exception is uncaught but the finally block is executed.

import inspect
def b():
    try:
        print inspect.getsource(factorial.undecorated)
        inspect.getargspec(f)
    finally:
        print 'blab'
        print inspect.getsource(heavy_computation.undecorated)
        print 'blab'
        # This is sort of funky because the print statements in -finally-
        # appear before the traceback.


import cProfile
cProfile.runctx('heavy_computation()', globals(), locals())

from sys import getsizeof
# hettinger cookbook "memory footprint"
from heapq import nlargest

# aha!
# cookbook: 'decorator to expose local variables of a function after execution' #



