
from decorators import memoize_
from functional import (elementwise, flatten,
    propagate_iter)


import numpy
import operator
from e_ast import globalize, globalizeA

def product(lst):
    '''similar to builtin sum.
    >>> product([1, 2, 3])
    6
    '''
    return reduce(operator.mul, lst)





#@memoize_(timeout=60*60*24)  # daily refresh
@globalize
def primes(max_p):
    # Find all primes <= max_p
    prms = []
    candidates = range(2, max_p+1)
    while candidates:
        candidates.reverse()
        nextp = candidates.pop()
        prms.append(nextp)
        to_remove = range(nextp, max_p+1, nextp)
        candidates = sorted(list(set(candidates).difference(to_remove)))
    return prms



#@globalizeA
def gprimes(max_p):
    # Generator to return all primes <= max_p.
    # Start with everything being a candidate for primehood.
    # When we find a prime remove it and all its multiples from the
    # candidate list.
    candidates = range(2, max_p+1)
    while candidates:
        nextp = candidates[0]
        yield nextp
        to_remove = range(nextp, max_p+1, nextp) # prime and all multiples.
        candidates = sorted(list(set(candidates).difference(to_remove)))




def is_prime(n):
    return len(factors(n)) == 1

@memoize_(timeout=30)
def factors(n):
    if n in primes(n): return [n]
    maxf = n/2  # max possible factor
    prms = primes(maxf)
    f = []
    while n>1:
        for p in prms:
            if n%p == 0:
                f.append(p)
                n = n/p
            else:
                prms.remove(p)
    return sorted(f)


# TODO not really a math function.
@memoize_(timeout=60*60*24)
def reps(seq):
    '''For each item in set(seq) count the number of occurences.
    '''
    count = []
    for ob in set(seq):
        count.append((ob, seq.count(ob)))
    return count





def lcf(a,b):
    '''
    >>> # largest common factor
    >>> lcf(15, 25)
    5
    >>> lcf(15, 75)
    15
    >>> lcf(8, 12)
    4
    '''
    fa = factors(a)
    fb = factors(b)
    # For each common factor include it the number of times it is in common.
    res = []
    for n in set(fa).intersection(fb):
        ca = fa.count(n)
        cb = fb.count(n)
        res.extend([n]*min(ca,cb))
    return product(res)




def smallest_common_multiple(a,b):
    '''
    >>> # remove largest common factor
    >>> scm(10, 15)
    30
    >>> scm(10, 75)
    150
    '''
    return (a*b)/lcf(a,b)


def factorial(n):
    assert type(n) == int and n >= 0
    if n==0: return 1
    return product(range(1,n+1))


def factorial(n):
    assert type(n) == int and n >= 0
    if n==0: return 1
    return n*factorial(n-1)

# tail recursive factorial.
# tail recursive means the recursive call refers ONLY to the function.

@memoize_(60*5)
def factorial(n, acc=1):
    assert type(n) == int and n >= 0
    if n==0: return acc
    return factorial(n-1, n*acc)


def is_numeric(x):
    try:
        blah = float(x)
        return True
    except ValueError: return False
    except TypeError: return False


def avg(seq): return sum(seq) / (len(seq) or numpy.inf)
def avg_nonzero(seq): return avg(x for x in seq if x!=0)
def avg_nonNone(seq): return avg(x for x in seq if x)
def avg_nznn(seq): return avg(x for x in seq if x and x!=0)



def test_elementwise():
    try:
        sq = elementwise(lambda x:x**2)
        sub = elementwise(lambda x: add(x,-4))
        def add(x, n): return x+n


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
    finally:
        globals().update(locals())

