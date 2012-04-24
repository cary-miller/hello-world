


import time

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



@memo
def goo():
    print 'hello from goo'
    return 44
assert goo.data==None
goo()
assert goo.data==None
goo.parasite()
assert goo.data==2




class ctx_mgr(object):
    def __init__(self, handle_err):
        assert handle_err in (True, False)
        self.handle_error = handle_err
        print 'init'
    def __enter__(self):
        print 'enter'
        testing_vars = (42, [], 'a', {}, object())
        return testing_vars
    def __exit__(self, exc_type, exc_val, exc_tb):
        print 'exit'
        if self.handle_error: return True
        return False


with ctx_mgr(True) as testing_vars:
    (n, L, s, d, o) = testing_vars
    print '*#&@ it %d' %n

# Context manager for testing ...
# http://jessenoller.com/2009/02/03/get-with-the-program-as-contextmanager-completely-different/

# Interesting stuff re recursive object inspection... Walking Python objects recursively
# Django error page middleware... Introducing django-ajaxerrors
#http://tech.blog.aknin.name/



# Self-referential functions !!!!!!!!!!!!!!!!!
# From akira at stackoverflow !
import inspect
def foo():
     felf = globals()[inspect.getframeinfo(inspect.currentframe()).function]
     print felf.__name__, felf.__doc__
     felf.__name__ = 'dick'

import sys
def bar():
     felf = globals()[sys._getframe().f_code.co_name]
     print felf.__name__, felf.__doc__




