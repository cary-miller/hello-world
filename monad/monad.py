#!/usr/bin/python
'''
I've struggled a couple of times now with grasping the monad concept.
http://blog.sigfpe.com/2006/08/you-could-have-invented-monads-and.html
'''

# Pretend we are in a pure functional language, ie. no print statements.

# We have functions that take a number and return a number.  We want to output
# strings too for debugging.


def f(x):
    return 2 * x

def g(x):
    return x ** 2

def compose(f, g):
    return lambda *pos: f(g(*pos))

def ident(x):
    return x

def fp(x):
    return f(x), 'f was called'

def gp(x):
    return g(x), 'g was called'

def bind(fp, gp):
    def inner(x):
        (gx, gs) = gp(x)
        (final, s) = fp(gx) 
        return final, '%s%s' % (s, gs)
    return inner

def unit(x):
    return (x, '')

def lift(f):
    return lambda x: unit(f(x))


def test():
    '''The initial example'''
    x = 5
    assert f(g(x)) == compose(f,g)(x)
    fpx = fp(x)
    gpx = gp(x)
    bfg = bind(fp, gp)
    (n, s) = bfg(x)
    assert n == f(g(x))
    assert s == '%s%s' % (fpx[1], gpx[1])
    print bfg(x)
    print lift(f)(x)
    c1 = bind(lift(f), lift(g))
    c2 = lift(compose(f,g))
    assert c1(x) == c2(x)

test()


'''Complex roots'''

def sqrt(x):
    try:
        return x ** (1/2.)
    except:
        return x
    pos = x ** (1/2.)
    return pos

def cbrt(x):
    res = x ** (1/3.)
    return [res, 0, 0]

def sixthrt(x):
    return sqrt(cbrt(x))


def bind(even_root, odd_root):
    def inner(x):
        odds = odd_root(x)
        return [(-even_root(odd), even_root(odd)) for odd in odds]
        even = even_root(odd)
        return (-even, even)
    return inner


def unit(x):
    return [x]

def test_roots():
    x = 2
    print sqrt(x)
    print cbrt(x)
#    print sixthrt(x) ** 6
    b = bind(sqrt, cbrt)
    print b(x)
    print bind(sqrt, unit)(x)
    print bind(unit, sqrt)(x)


if __name__ == '__main__':
    test_roots()



