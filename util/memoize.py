'''
Proven, useful decorators.
'''

import time
import functools


#@decorator.decorator
def _memoize(func, *args, **kw):
    # frozenset to ensure hashability
    key = frozenset(args), frozenset(kw.items())
    if key not in func.cache:
        func.cache[key] = func(*args, **kw)
    return func.cache[key]

def memoize(f):
    f.cache = {}
    return decorator.decorator(_memoize, f)


# Enhanced memoize!  Adds a timeout to each key.
def memoize_(timeout=60*60*24):
    def memo(func):
        func.cache = {}
        @functools.wraps(func)
        def _memo(*args, **kw):
            # The entire set of args and kw is the key.
            # frozenset to ensure hashability
            key = frozenset(args), frozenset(kw.items())
            cache = func.cache
            if not (key in cache and time.time()-cache[key]['time'] < timeout):
                result = func(*args, **kw)
                cache[key] = dict(value=result, time=time.time())
            return cache[key]['value']
        return _memo
    return memo

# TODO  Check recalculated version for sanity before replacing
# cached value.  If recalc fails return the cached value.
# TODO  Have the decorated func accept optional arg 'recalc'
# TODO  Use decorator.decorator to reduce nesting and preserve params.
# ...... wait.  belay that TODO.  decorator is NOT in std lib.  Use
# functools.


memo_cache = {}
# Yet another memoize!  Delete any key older than timeout.
# And use a global cache.
def memoize_(timeout=60*60*24):
    def memo(func):
#        func.cache = {}
        @functools.wraps(func)
        def _memo(*args, **kw):
            # The entire set of args and kw is the key.
            # frozenset to ensure hashability
            key = func.func_name + str(args) + str(kw.items())
            key = func.func_name , str(args) , frozenset(kw.items())
#            cache = func.cache
            cache = memo_cache
            for key in cache.keys():
                if time.time()-cache[key]['time'] > timeout:
                    del cache[key]
            if not key in cache.keys():
                result = func(*args, **kw)
                cache[key] = dict(value=result, time=time.time())
            return cache[key]['value']
        return _memo
    return memo
#


frozenset([])
lst = ['a', 123, range(3)]
frozenset([])


# How to execute consecutive commands from history.  with arrow keys.
# http://unix.stackexchange.com/questions/24739/how-to-execute-consecutive-command-from-history

import decorator
# Decorator module makes possible to define decorators with
# less nesting.  Also preserves undecorated params.


# The benefit of decorator shows up when you start looking at
# func.__name__ and such.  Or is that really a benefit?  One could waste
# lots of time tracking a bug that turns out to be in the decorator.





# Another memoization scheme.
class Foo(object):

    def __init__(self, timeout=60):
        self.time = 0
        self.timeout = timeout
    
    def __call__(self):
        if time.time() - self.time > self.timeout:  # or not self.bah
            self.bah = 'ha'
        return self.bah

foo = Foo()

# And yet another memo scheme.
# We can attach the data permanently to the function.
def f(timeout=60):
    f.timeout=timeout
    f.time=0
    if time.time() - f.time > f.timeout:
        f.x=2
    return f.x


# Festoon the original function with extra crap.
def memo(func):
    func.timeout=60
    func.time=0
    func.data=None
    def parasite():
        print 'hello from parasite'
        func.data=2
    func.parasite=parasite
    return func

# I see three sorts of decorators.
#   1.  Leave the original function untouched.
#   2.  Like the above festoon the func.
#   3.  Actually alter the code inside the func like w/AST.



