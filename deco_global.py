# Super simple examples showing the bare bones structure of different sorts of
# decorators.


# simplest possible do-nothing decorator #
def deco(f):
    def inner(*a, **k):
        return f(*a, **k)
    return inner


@deco
def f():
    x=22
    return 44

# No, not the simplest.

def deco2(f): return f

def deco3(f):
    f.blah = 'ha'
    return f

def deco4(name, val):
    def deco5(f):
        f.__setattr__(name, val)
        return f
    return deco5


# simplest possible do-nothing decorator with argument #
def outer(arg):
    def deco(f):
        # do something with arg here
        def inner(*a):
            # or here
            return f(*a)
            # or here
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


#@blah
def facto(n):
    assert n == int(n) and n >= 0
    if n==0: return 1
    return n*factorial(n-1)



def preserve_sig(f):
    # figure out func sig here.
    argspec = inspect.getargspec(f)
    return lambda sig: f(sig)


def preserve_sig(f):
    fglob = f.func_globals
    argspec = inspect.getargspec(f)
    fco = f.func_code
    call_fn = types.FunctionType(fco, fglob, 'foo')
    return call_fn


f = factorial



# Mertz has fascinating stuff on decorators and metaclasses.
# Including this hw assignment.

def propagate_iter(fn, it):
    # iteratively apply fn(x) for x in it.
    while 1:
        yield fn(it.next())

def elementwise(fn):
    def newfn(arg):
        if hasattr(arg, 'next'): # iterator/generator
            return propagate_iter(fn, arg)
        try:
            if hasattr(arg, '__getitem__'): # sequence
                return type(arg)(map(fn, arg))
        except TypeError:   # xrange is neither seq nor iter nor gen.
                return map(fn, arg)
        return fn(arg)
    return newfn

@elementwise
def sq(x):
    return x**2

@elementwise
def sub(x):
    return add(x,-4)

def add(x, n):
    return x+n



sq(3)        # int
sq(range(5)) # list
sq(ob for ob in range(5)) # generator
sq(xrange(5)) # neither fish nor fowl

g = (ob for ob in range(5)) # generator
pi = propagate_iter(sq, g)
pc = propagate_iter(sub, pi)
pc = propagate_iter(sub, propagate_iter(sq, g))
pc = sub(sq(g))
# All pc's give the same result


# http://wiki.python.org/moin/PythonDecoratorLibrary

# Does a decorator have access to locals() of the decorated func?
# NO.
# BUT  see functools.update_wrapper
import functools


# decorator that makes all locals global #
# No it doesn't.
def globalizeA(f):
    def wrapper(*a, **k):
        print wrapper.__dict__
        functools.update_wrapper(wrapper, f)
        wrapper.__dict__ = f.__dict__
        print wrapper.__dict__
        print f.__dict__
        globals().update(locals())
        return f(*a, **k)
    return wrapper

@globalizeA
def i(a):
    x=22
    return 44*a


import time

import decorator
# Decorator module makes possible to define decorators with
# less nesting.  Also preserves undecorated params.

@decorator.decorator
def trace(f, *args, **kw):
    print 'calling %s with args %s, %s' % (f.func_name, args, kw)
    return f(*args, **kw)


@trace
def j(*args, **kw):
    x=22
    return 44

@trace
def kk():
    x=22
    return 44

# compare f.func_name for f in (k, kk)
# Passing params to k & kk yield interestingly different results.
# k begins execution of *inner* and does not raise an exception until the
# undecorated func begins execution.  kk never begins and raises the
# exception immediately, just as the undecorated version would.




def trace1(f):
    def inner(*args, **kw):
        print 'calling %s with args %s, %s' % (f.func_name, args, kw)
        return f(*args, **kw)
    return inner

@trace1
def k():
    x=22
    return 44

# The benefit of decorator shows up when you start looking at
# func.__name__ and such.  Or is that really a benefit?  One could spend
# lots of time tracking a bug that turns out to be in the decorator.
# LESSON:  be judicious with decorators.

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


from collections import defaultdict
import time






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





@memoize
def factorial(n):
    assert type(n) == int and n >= 0
    if n==0: return 1
    return n*factorial(n-1)





# class based memoize
class mem(object):
    def __init__(self, f):
        self.d={}
        self.f=f
    def __call__(self, *a, **k):
        key = frozenset(a), frozenset(k.items())
        if key not in self.d:
            self.d[key] = self.f(*a, **k)
        return self.d[key]
        
@mem
def factorial(n):
    assert n == int(n) and n >= 0
    if n==0: return 1
    return n*factorial(n-1)


# ....................................................................
# ......................... end of decorators ........................
# ....................................................................

# pdb 
# http://plone.org/documentation/kb/using-pdb
# http://pythonconquerstheuniverse.wordpress.com/category/python-debugger/

# Probing the mysteries of try/finally.
def a():
    # No need for the -except- block
    x = 1
    y = 0
    try: z = x/y
    finally: 
        x=33
        # The exception is uncaught but the finally block is executed.


import inspect
def c():
    try:
        print inspect.getsource(factorial.undecorated)
        inspect.getargspec(f)
    finally:
        print 'blab'
        print inspect.getsource(b.undecorated)
        print 'blab'
        # This is sort of funky because the print statements in -finally-
        # appear before the traceback.
        # .... and that is quite proper.  That is exactly how it works.  If there
        # is an uncaught exception in the try the finally gets executed BEFORE the
        # exception is raised.
        # That is how finally works.  The finally block ALWAYS GETS
        # EXECUTED, even if there is an exception.


import cProfile
cProfile.runctx('factorial(8)', globals(), locals())

from sys import getsizeof
# hettinger cookbook "memory footprint"
from heapq import nlargest

# aha!
# cookbook: 'decorator to expose local variables of a function after execution' #



# krebsonsecurity.com







# ---------------- class method ---------------------------
# According to Guido there is no use case for @classmethod.  If you want a
# class method define it using metaclass like so (Armin Ronacher)
'''
>>> class CMeta(type):
...  def foo(cls):
...   print cls
... 
>>> class C(object):
...  __metaclass__ = CMeta
... 
>>> C.foo()
<class '__main__.C'>
'''

# I've been thinking @staticmethod is completely worthless but maybe not..
#'''
#Staticmethod is not useless. since it is not passed an implicit class or
#instance of class as first argument, it is useful for processing class
#attributes that spans instances   Eric Wang
#'''
# ... of course I have not seen an example.



# And here are two interesting things.
#   1.  Method decorator
#   2.  Per instance ...

import functools

def counted(method):
    @functools.wraps(method)
    def wrapped(obj, *args, **kwargs):
        if hasattr(obj, 'count'): 
            obj.count += 1
        else:
            obj.count = 1
        return method(obj, *args, **kwargs)
    return wrapped

# In above code, we intercept the object as obj parameter of the decorated
# version of method. Usage of the decorator is pretty straightforward:

class Foo(object):
    @counted
    def do_something(self): pass



# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# And here is an example use of a metaclass.  You want to decorate all
# methods of a class.
# thanks TokenMacGuy

def myDecorator(fn):
    fn.foo = 'bar'
    return fn

class myMetaClass(type):
    def __new__(cls, name, bases, local):
        for attr in local:
            value = local[attr]
            if callable(value):
                local[attr] = myDecorator(value)
        return type.__new__(cls, name, bases, local)

class myClass(object):
    __metaclass__ = myMetaClass
    def baz(self):
        print self.baz.foo

'''
>>> quux = myClass()
>>> quux.baz()
bar
'''
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# And here is the same problem solved with a class decorator.
# delnan
def mydecorator(f):
    @functools.wraps(f)
    def inner(*a, **k):
        return f(*a, **k)
    return inner
        


def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate

#Use like this:

@for_all_methods(mydecorator)
class C(object):
    def m1(self): pass
    def m2(self, x): pass

# And for this example since py 3.0 3.1 does not have callable one could
# use
# inspect.getmembers(cls, inspect.ismethod) 




# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
import types
def deco_g(fn):
    fglob = fn.func_globals
    def inner(*a, **k):
#        call_fn = types.FunctionType(fn.func_code, globals())
        call_fn = types.FunctionType(fn.func_code, fglob)
        return call_fn(*a, **k)
    return inner

import pdb
from ast_exp import globalize, parrot

def fx():
    try:
        pass
    finally:
        return


xy=67
@deco_g
def aa():
    xy=23
    return
    
def ab():
    xy=23456
    return
 
p = parrot(ab)
globalize(ab)


