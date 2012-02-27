
from decorators import memoize_
from functional import (elementwise, flatten,
    propagate_iter)


import operator

def product(lst):
    '''similar to builtin sum.
    >>> product([1, 2, 3])
    6
    '''
    return reduce(operator.mul, lst)





@memoize_(timeout=60*60*24)  # daily refresh
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



def gprimes(max_p):
    # Generator to return all primes <= max_p.
    # Find all primes <= max_p
    # Start with everything being a candidate for primehood.
    # When we find a prime remove it and all of its multiples from the
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
    return n*factorial(n-1)

# tail recursive factorial.
# tail recursive means the recursive call refers ONLY to the function.

def factorial(n, acc=1):
    assert type(n) == int and n >= 0
    if n==0: return acc
    return factorial(n-1, n*acc)



@elementwise
def sq(x):
    return x**2

@elementwise
def sub(x):
    return add(x,-4)

def add(x, n):
    return x+n


if 1:
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


