'''
Implementing a map-reduce example described at
http://stevekrenzel.com/finding-friends-with-mapreduce
Requires 2.6
'''
from pprint import pprint
from collections import defaultdict

# ###################### Support functions ###################### #

def partition(lst, func):
    '''Partition lst on value of func applied to each element.
    >>> partition(lst, lambda ob: ob[attr])
    >>> partition(lst, lambda sublst: sublst[i])
    >>> partition(lst, lambda ob: ob.attr)
    '''
    res = defaultdict(lambda:[])
    for ob in lst:
        res[func(ob)].append(ob)
    return res


def flattened(lst):
    '''
    >>> nested = [[1], [2,3,4], [5], [6,7]]
    >>> flattened(nested)
    [1,2,3,4,5,6,7]
    '''
    return [item for sublist in lst for item in sublist]
    # from Martelli of course



# ############################ Data ############################# #
A,B,C,D,E = range(5)

# [person, (list of friends)]
person_friends = [
    [A, (B,C,D)],
    [B, (A,C,D,E)],
    [C, (A,B,D,E)],
    [D, (A,B,C,E)],
    [E, (B,C,D)]
    ]


# ####################### The juicy parts ####################### #

def map_func(p_pals):
    person, friends = p_pals
    return [(sorted([person,pal]), friends) for pal in friends]


mapped = flattened([map_func(p_pals) for p_pals in person_friends])

part = partition(mapped, lambda ob: str(ob[0]))   
grouped = sorted([(eval(k),[(b) for (a,b) in part[k]]) for k in part])

reduced = [(k, list(set.intersection(*(set(s) for s in v)))) for (k,v) in grouped]
common_friends = reduced


# ########################## The result ######################### #
assert common_friends == [
 ([A, B], [C, D]),
 ([A, C], [B, D]),
 ([A, D], [B, C]),
 ([B, C], [A, D, E]),
 ([B, D], [A, C, E]),
 ([B, E], [C, D]),
 ([C, D], [A, B, E]),
 ([C, E], [B, D]),
 ([D, E], [B, C])]


