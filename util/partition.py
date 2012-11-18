

from collections import defaultdict # 2.6+

def partition(lst, attr):
    '''Partition lst on attr, an attribute of each element.
    '''
    res = defaultdict(lambda:[])
    for ob in lst:
        res[ob[attr]].append(ob)
    return res


def partition(lst, func):
    '''Partition lst on value of func applied to each element.
    Duplicate previous version thus:
    >>> partition(lst, lambda ob: ob[attr])
    '''
    res = defaultdict(lambda:[])
    for ob in lst:
        res[func(ob)].append(ob)
    return res


def test_partition():
 try:   
    # examples
    lst = range(12)
    func = lambda x: x>6
    p1 = partition(lst, func)

    # An example using objects.
    class C(object):
        def __init__(self, val):
            self.foo=val
    import random
    lst = [C(random.choice(list('abc'))) for i in range(12)]
    func = lambda ob: ob.foo
    p2 = partition(lst, func)
 finally: globals().update(locals())


def d_partition(lst, func):
    # TODO consider changing to this name.
    pass


