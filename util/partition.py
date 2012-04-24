

from collections import defaultdict

def partition(lst, attr):
    res = defaultdict(lambda:[])
    for ob in lst:
        res[ob[attr]].append(ob)
    return res


