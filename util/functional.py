'''
Functional programming code.  Includes plenty of decorators.

'''


# Functional code lifted from Mertz's Text Processing book
from operator import mul, add, truth
#apply_each = lambda fns, args=[]: map(apply, fns, [args]*len(fns))
bools = lambda lst: map(truth, lst)
bool_each = lambda fns, args=[] : bools(apply_each(fns, args))
conjoin = lambda fns, args=[]: reduce(mul, bool_each(fns, args))
all_ = lambda fns: lambda arg, fns: conjoin(fns, (arg,))
both = lambda f,g: all_((f,g))
all3 = lambda f,g,h: all_((f,g,h)) 
and_ = lambda f,g: lambda x, f=f, g=g: f(x) and g(x)
disjoin = lambda fns, args=[]: reduce(add, bool_each(fns, args))
some = lambda fns: lambda arg, fns=fns: disjoin(fns, (arg,))
either = lambda f,g: some((f,g))
anyof3 = lambda f,g,h: some((f,g,h)) 
#compose = lambda f,g: lambda x, f=f, g=g: f(g(x))
ident = lambda x: x



# Modernized versions
ident = lambda x: x
compose = lambda f,g: lambda x: f(g(x))
bools = lambda lst: [bool(ob) for ob in lst]

# Functions that apply identical args to a list of functions.
apply_each = lambda fns, *pos, **kw: [fn(*pos, **kw) for fn in fns]
bool_each = lambda fns,  *pos, **kw: bools(apply_each(fns, *pos, **kw))
all_true = lambda fns,   *pos, **kw: all(bool_each(fns,  *pos, **kw))
any_true = lambda fns,   *pos, **kw: any(bool_each(fns,  *pos, **kw))

and_ = lambda *funcs: lambda *pos, **kw: all(f(*pos, **kw) for f in funcs)
or_ = lambda *funcs: lambda *pos, **kw: any(f(*pos, **kw) for f in funcs)


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





###################### dictionary with subset of keys ############
d = dict(a=2, b=3, c=4)

def d_from_keys(d, keys):
    return dict((key, d[key]) for key in keys)
    return dict((key, d[key]) for key in keys if key in d)

s = d_from_keys(d, ['a', 'c'])





p2 = lambda x: x**2
a2 = lambda x: x+2
add_func = lambda n: lambda x: x+n
mul_func = lambda n: lambda x: x*n
pow_func = lambda n: lambda x: x**n
p2 = pow_func(2)
a2 = add_func(2)
m2 = mul_func(2)

assert a2(p2(3)) == compose(a2, p2)(3)

lst = [0, 1, [], [0], (), (0,), {}, {'z':0}, False, True]

#assert disjoin([ident], lst) == any(bool_each([ident], lst))




import itertools
def flatten(seq): return itertools.chain.from_iterable(seq)

# Mertz has fascinating stuff on decorators and metaclasses.
# Including this hw assignment.  Extend the elementwise decorator to
# accept an iterator/generator.

def propagate_iter(fn, it):
    # yield fn(x) for x in it.
    while 1:
        yield fn(it.next())

# like propagate_iter except stupid xrange does not have a .next() method
# so we improvise.
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
    >>> sq(3)        # int
    9
    >>> sq(range(5)) # list
    [0, 1, 4, 9, 16]
    >>> g = sq(i for i in range(5)) # generator
    >>> [n for n in g]
    [0, 1, 4, 9, 16]
    >>> sq(xrange(5)) # neither fish nor fowl
    [0, 1, 4, 9, 16]
    >>> sq(set((1,2,3)))
    [1, 4, 9]

    >>> # Would like to have this option.
    >>> sq(1,2,3)    # exception
    >>> # But I think that's impossible.
    '''
    def newfn(arg):
        if type(arg) == dict:
            raise TypeError('elementwise not accepting dict arg, %s'%str(arg))
        if type(arg) in (set):
            return map(fn, arg)
        if type(arg) in (list, tuple):
            return type(arg)(map(fn, arg))
        if hasattr(arg, 'next'): # iterator/generator
            return propagate_iter(fn, arg)
        if type(arg) in (xrange):
            return propagate_xrange(fn, arg)
        return fn(arg)
    return newfn



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
    ''' Return the list.
    '''
    return [ob for ob in iter]



def test_sequencify():
    def f(a): return [a]*3
    blah = sequencify(f)(['a', 'b'])
    haha = sequencify(f)(('b', 'a'))
    #bada = sequencify(f)('a', 'b')
    tada = sequencify(f)('a')



