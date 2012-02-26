





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



def sequencify(func):
    '''func is a function of one argument that returns a list.
    Return a function that accepts a list/tuple of args and returns a
    list.
    Might want to have new_func specifically require type(arg_list) in
    (list, tuple) to prevent issues when type(arg_list) == dict.
    '''
    def new_func(arg_list):
        return flatten(elementwise(func)(arg_list))
        return elementwise(func)(arg_list)
    return new_func


def spread_out(iter):
    ''' Return the list.
    '''
    return [ob for ob in iter]




def f(a): return [a]*3

blah = sequencify(f)(['a', 'b'])
haha = sequencify(f)(('b', 'a'))
#bada = sequencify(f)('a', 'b')
tada = sequencify(f)('a')


import itertools
def flatten(seq): return itertools.chain.from_iterable(seq)

assert spread_out(sequencify(f)(['a', 'b'])) == flatten(elementwise(f)(['a', 'b']))
#assert sequencify(f)(('b', 'a')) == elementwise(f)(('b', 'a'))
#assert sequencify(f)('a', 'b') == elementwise(f)('a', 'b')
assert sequencify(f)('a') == elementwise(f)('a')

if 0:
    assert sequencify(f)(['a', 'b']) == flatten(elementwise(f)(['a', 'b']))
    assert sequencify(f)(('b', 'a')) == flatten(elementwise(f)(('a', 'b')))
#    assert sequencify(f)('a', 'b') == flatten(elementwise(f)('a', 'b'))
    assert sequencify(f)('a') == elementwise(f)('a')




