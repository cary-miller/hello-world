'''
Functional programming code.  Includes plenty of decorators.
Works with Python 2.4+
Starts with Mertz's page of functional code at the beginning of
*Text Processing with Python*
Improves and modernizes Mertz's code.  Mertz wanted backward-compatibility
all the way to 2.0 or something and I only want back to 2.4.

'''

import sys

(major, minor) = [int(sys.version[i]) for i in (0,2)]
if major==2 and minor<5:

    def all(seq):
        for ob in seq:
            if not bool(ob):
                return False
        return True

    def any(seq):
        for ob in seq:
            if bool(ob):
                return True
        return False
        


# Borrowing handy ideas from Lisp.
def head_tail(seq): 
    '''
    >>> head_tail('abcdef')
    ('a', 'bcdef')
    '''
    return (seq[0], seq[1:])

def end_front(seq): 
    # TODO change name to front_end or head_butt
    '''
    >>> end_front('abcdef')
    ('abcde', 'f')
    '''
    return (seq[:-1], seq[-1])



# Modernized versions of Mertz's functional code from *Text Processing with Python*
# A lot of his stuff is superceded by builtins; bool, all, any, list comprehensions,
# ...
ident = lambda x: x
bools = lambda lst: [bool(ob) for ob in lst]
bools = lambda lst: map(bool, lst)
boolify = lambda f: lambda *pos, **kw: bool(f(*pos, **kw))
# TODO show an example/test of using this one.  Is it even needed?

#########################################################################################
################################## Compose functions  ###################################
#########################################################################################


# Original compose only takes two functions.
compose = lambda f,g: lambda x: f(g(x))
compose = lambda f,g: lambda *pos, **kw: f(g(*pos, **kw))


 
def composeR(*funcs): 
    '''
    Recursive compose that takes any number of args.
    Composed functions take a single arg(x) and return a single value.
    '''
    if not funcs: return ident
    (f0, rest) = head_tail(funcs) 
    return lambda x: f0(composeR(*rest)(x))


def composeTR(*funcs, **kw):
    '''
    Tail recursive compose that takes any number of args.
    Composed functions take a single arg(x) and return a single value.
    '''
    composed=kw.get('composed') or ident
    if not funcs: return composed
    (front, end) = end_front(funcs)
    return composeTR(*front, composed=lambda x: end(composed(x)))



def composeRarb(*funcs): 
    '''
    Recursive compose that takes any number of args.
    Composed functions take arbitrary args (*pos, **kw) and return arbitrary values.
    Each composed function must take as parameters the output of the previous
    function.
    '''
    if not funcs: return ident
    (f0, rest) = head_tail(funcs) 
    return lambda *pos, **kw: f0(composeR(*rest)(*pos, **kw))
 
 
def composeR_test():
 try:
    f = lambda x: x+2
    g = lambda x: x*2
    h = lambda x: x**2
    x=4
    assert composeR()(x) == x == ident(x)  ==  composeTR()(x)
    assert composeR(f)(x) == f(x)  == composeTR(f)(x) 
    assert composeR(f,g)(x) == f(g(x))  ==  composeTR(f,g)(x) 
    assert composeR(f,g,h)(x) == f(g(h(x)))  ==  composeTR(f,g,h)(x)
 finally: globals().update(locals())


def composeRarb_test():
 try:
    f = lambda d: str(d['b']) + 'fffffffooooo'
    g = lambda (x,y): dict(a=x,b=y)
    h = lambda x: (x,2)
    x=4
    assert composeRarb()(x) == x
    assert composeRarb(h)(x) == h(x)
    assert composeRarb(g,h)(x) == g(h(x))
    assert composeRarb(f,g,h)(x) == f(g(h(x)))
 finally: globals().update(locals())


composeR_test()
composeRarb_test()



#########################################################################################
############ Apply a list of functions element-wise to one set of arguments #############
#########################################################################################


and_ = lambda *funcs: lambda *pos, **kw: all(f(*pos, **kw) for f in funcs)
or_ = lambda *funcs: lambda *pos, **kw: any(f(*pos, **kw) for f in funcs)
all_true = lambda *funcs: lambda  *pos, **kw: all(f(*pos, **kw) for f in funcs)
any_true = lambda *funcs: lambda  *pos, **kw: any(f(*pos, **kw) for f in funcs)

mertz_apply_each = lambda fns, args=[]: map(apply, fns, [args]*len(fns)) # ugly
apply_each = lambda *funcs: lambda *pos, **kw: [f(*pos, **kw) for f in funcs]
bool_each = lambda *funcs: lambda  *pos, **kw: bools(apply_each(funcs)(*pos, **kw))


def testing(): # TODO rename
 try:
    def f(): return 1
    def g(): return 'a'
    def h(): return {'a':3}
    assert  apply_each(f,g,h)() == [1, 'a', {'a':3}]   == mertz_apply_each([f,g,h], [])


    def f(x): return x+2
    def g(x): return x*2
    def h(x): return x**2
    assert apply_each(f,g,h)(3) == [5, 6, 9]   == mertz_apply_each([f,g,h], [3])


    def f(x,y): return x+y
    def g(x,y): return x*y
    def h(x,y): return x**y
    assert apply_each(f,g,h)(3, 4) == [7, 12, 81]  == mertz_apply_each([f,g,h], [3, 4])


    def f(x,y, f=None): return f(x+y)
    def g(x,y, f=None): return f(x*y)
    def h(x,y, f=None): return f(x**y)
    assert apply_each(f,g,h)(3, 4, f=ident) == [7, 12, 81]
    assert apply_each(f,g,h)(3, 4, f=lambda x: x*2) == [14, 24, 162] \
        == mertz_apply_each([f,g,h], [3, 4,  lambda x: x*2])
    # NOTE mertz requires transforming keyword params to positional,  thus losing information
    # and making it impossible to give keywords args in arbitrary order.

    def f(x,y, f=None, g=0): return f(x+y)
    def g(x,y, f=None, g=0): return f(x*y) + g
    def h(x,y, g=0, f=None): return f(x**y) * g
    assert  apply_each(f,g,h)(3, 4, f=lambda x: x*2, g=11) == \
            apply_each(f,g,h)(3, 4, g=11, f=lambda x: x*2)
    # oops, mertz can't handle this, haha.
 finally: globals().update(locals())
testing()


def a():
 try:
    def t(): return True
    def f(): return False
    assert and_(t,t,t)() == True
    assert and_(t,t,f)() == False
    assert or_(t,t,f)() == True
    assert or_(f,f,f)() == False

    def t(x,y): return True
    def f(x,y): return False
    assert and_(t,t,t)(0,1) == True
    assert and_(t,t,f)(0,1) == False
    assert or_(t,t,f)(0,1) == True
    assert or_(f,f,f)(0,1) == False

    def t(x,y, a,b): return True
    def f(x,y, a,b): return False
    assert and_(t,t,t)(0,1,a='',b=2) == True
    assert and_(t,t,f)(0,1,a='',b=2) == False
    assert or_(t,t,f)(0,1,a='',b=2) == True
    assert or_(f,f,f)(0,1,a='',b=2) == False

 finally: globals().update(locals())
a()


def foooo():
 try:
    # Not sure why this is here.  Tests the original simple compose.
    p2 = lambda x: x**2
    a2 = lambda x: x+2
    add_func = lambda n: lambda x: x+n
    mul_func = lambda n: lambda x: x*n
    pow_func = lambda n: lambda x: x**n
    p2 = pow_func(2)
    a2 = add_func(2)
    m2 = mul_func(2)

    assert a2(p2(3)) == compose(a2, p2)(3)
    assert a2(p2(3)) == composeR(a2, p2)(3)
    assert a2(p2(3)) == composeTR(a2, p2)(3)

    lst = [0, 1, [], [0], (), (0,), {}, {'z':0}, False, True]

    #assert disjoin([ident], lst) == any(bool_each([ident], lst))
 finally: globals().update(locals())
foooo()


#########################################################################################
################# Apply a function element-wise to a list of arguments ##################
#########################################################################################

import itertools
def flatten(seq): return itertools.chain.from_iterable(seq)

# Mertz has fascinating stuff on decorators and metaclasses.
# Including this hw assignment.  Extend the elementwise decorator to
# accept an iterator/generator.

def propagate_iter(fn, it):
    ''' yield fn(x) for x in it. '''
    while 1:
        yield fn(it.next())

# like propagate_iter except xrange does not have a .next() method.
def propagate_xrange(fn, xr):
    for i in xr:
        yield fn(i)



def elementwise(fn):
    '''Decorator to duplicate functionality of matlab/numpy type
    functions.  The function will accept one number or a sequence of
    numbers or an iterator/generator.  NOTE: if the input is an iter/gen
    the output is the same type.

    The input function, fn, is a function of one arg.  Return a function
    that accepts list/tuple/iter/generator/xrange/set of args.
    NOTE: xrange is a misfit non-iterator, xrange is a TYPE!
    
    >>> @elementwise
    >>> def sq(x): return x**2
    >>> sq = elementwise(lambda x:x**2)
    >>> assert sq(3) == 9
    >>> assert sq(range(5)) == [0, 1, 4, 9, 16]
    >>> assert [n for n in sq(i for i in range(5))] == [0, 1, 4, 9, 16]
    >>> assert sq(xrange(5)) == [0, 1, 4, 9, 16]
    >>> assert sq(set((1,2,3))) == [1, 4, 9]

    >>> # Would like to have this option.
    >>> sq(1,2,3)    # exception
    >>> # But I think that's impossible.
    '''
    def newfn(arg):
        if type(arg) == dict:
            raise TypeError('elementwise not accepting dict arg, %s'%str(arg))
        if type(arg) in (set,):         return map(fn, arg)
        if type(arg) in (list, tuple): return type(arg)(map(fn, arg))
        if hasattr(arg, 'next'):       return propagate_iter(fn, arg)# iterator/generator
        if type(arg) in (xrange, ):      return propagate_xrange(fn, arg)
        return fn(arg)
    return newfn

def test_elementwise():
 try:
    @elementwise
    def sq(x): return x**2
    sq = elementwise(lambda x:x**2)
    assert sq(3) == 9
    assert sq(range(5)) == [0, 1, 4, 9, 16]
    assert [n for n in sq(i for i in range(5))] == [0, 1, 4, 9, 16]
    assert [n for n in sq(xrange(5))] == [0, 1, 4, 9, 16]
    assert sq(set((1,2,3))) == [1, 4, 9]
 finally: globals().update(locals())

test_elementwise()


def sequencify(func):
    '''func is a function of one argument that returns a list.
    Return a function that accepts a list/tuple/iter/gen of args and returns a
    list.
    Might want to have new_func specifically require type(arg_list) in
    (list, tuple) to prevent issues when type(arg_list) == dict.
    >>>
    >>>
    >>>
    >>>
    '''
    def new_func(arg_list):
        res=[]
        for arg in arg_list:
            res.extend(func(arg))
        return res
        res = flatten(elementwise(func)(arg_list))
        return [ob for ob in res]
        return flatten(elementwise(func)(arg_list))
        return elementwise(func)(arg_list)
    return new_func


def spread_out(iter):
    ''' Return the list.  '''
    return [ob for ob in iter]



def test_sequencify():
    def f(a): return [a]*3
    blah = sequencify(f)(['a', 'b'])
    haha = sequencify(f)(('b', 'a'))
    #bada = sequencify(f)('a', 'b')
    tada = sequencify(f)('a')


# ######################################################################## #
# ###################### Dictionary Functions ############################ #
# ######################################################################## #

def d_subset(dct, keys):
    '''Subset dict, keeping keys, tossing other keys.
    >>> d = dict(a=1,b=2,c=3)
    >>> assert d_subset(d, ('a', 'c')) == {'a': 1, 'c': 3}
    '''
    return dict((key, value) for (key, value) in dct.items() if key in keys)

# TODO which name to use?  This, that, both, neither?
def d_from_keys(d, keys):
    return dict((key, d[key]) for key in keys)
    return dict((key, d[key]) for key in keys if key in d)

# TODO change trans to translate
def d_trans_keys(dct, mapping, keep_all_keys=True):
    '''Translate dict keys, optionally keeping only mapped keys.
    >>> d = dict(a=1,b=2,c=3)
    >>> m = (('a','x'), ('b','y'))
    >>> assert d_trans_keys(d, m) == {'y': 2, 'x': 1, 'c': 3}
    >>> assert d_trans_keys(d, m, keep_all_keys=False) == {'y': 2, 'x': 1}
    >>> assert d_trans_keys(d, m, False) == {'y': 2, 'x': 1}
    '''
    if keep_all_keys:
        mkeys = [old for (old,new) in mapping]  # translated keys
        mapping = list(mapping) + [(old,old) for old in dct.keys() if old not in mkeys]
    return dict((new, dct[old]) for (old,new) in mapping)


def test_d_funcs():
 try:
    d = dict(a=1,b=2,c=3)
    assert d_subset(d, ('a', 'c')) == {'a': 1, 'c': 3} == d_from_keys(d, ['a', 'c'])
    m = (('a','x'), ('b','y'))

    assert d_trans_keys(d, m) == {'y': 2, 'x': 1, 'c': 3}
    assert d_trans_keys(d, m, keep_all_keys=False) == {'y': 2, 'x': 1}
    assert d_trans_keys(d, m, False) == {'y': 2, 'x': 1}
 finally: globals().update(locals())

test_d_funcs()









