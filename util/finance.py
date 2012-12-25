
# ################################################################### #
# ############################ Util ################################# #
# ################################################################### #

import operator

def product(lst):
    '''similar to builtin sum.
    >>> product([1, 2, 3])
    6
    '''
    return reduce(operator.mul, lst)



# ################################################################### #
# ########################## Payments ############################### #
# ################################################################### #

def mortgage_payment(principal, interest, years):
    '''
    principal in dollars:  1000000
    interest in human:     8.4
    years as integer:      10
    '''
    months=years*12.0
    if interest == 0:  return principal/months
    rate = interest/1200.0
    payment =  (rate + rate/((1+rate)**months -1)) * principal
    return  int(payment)


def amortization(principal, interest, years, t):
    '''
    Remaining principal after t payments.
    principal in dollars:  1000000
    interest in human:     8.4
    years as integer:      10
    t months as integer:   24  
    amortization(100000, 8.4, 30, 0)
    '''
    r = interest/1200.0 + 1
    A = mortgage_payment(principal, interest, years)
    P = principal
    principal_remaining = P*r**t - A*sum([r**k for k in range(t)])
    return round(principal_remaining, 2)



# ################################################################### #
# ########################### Returns ############################### #
# ################################################################### #


# http://en.wikipedia.org/wiki/Rate_of_return
# Wikipedia gives numerous different ways to calculate rate of return.
from math import log, e

def return_arithmetic(start, end):  # single period
    '''aka yield '''
    return (end-start)/float(start)

def return_logarithmic(start, end, t):
    return log(end/float(start)) / t

def return_amount(principal, rate, time):
    return principal * e**(rate*time)

def rate_of_return(start, end, years): pass

def final_fig(principal, interest, years): pass
