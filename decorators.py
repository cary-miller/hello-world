'''
Proven, useful decorators.
'''


import time
import functools




# The benefit of decorator shows up when you start looking at
# func.__name__ and such.  Or is that really a benefit?  One could spend
# lots of time tracking a bug that turns out to be in the decorator.
# LESSON:  be judicious with decorators.

import decorator

# Decorator module makes possible to define decorators with
# less nesting.  Also preserves undecorated params.




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
def memoize_(timeout=60*60):
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





