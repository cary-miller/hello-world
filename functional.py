'''
Functional programming code.  Includes plenty of decorators.

'''



import itertools
def flatten(seq): return itertools.chain.from_iterable(seq)

# Mertz has fascinating stuff on decorators and metaclasses.
# Including this hw assignment.  Extend the elementwise decorator to
# accept an iterator/generator.

def propagate_iter(fn, it):
    # iteratively apply fn(x) for x in it.
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



