



def memory():
    import cProfile
    from guppy import hpy
    h = hpy()
    print h.heap()
 

# set/frozenset shortcuts
# s < t  subset
# s > t  superset
# s | t  subset
# s & t  subset
# s - t  subset
# s ^ t  subset
# s^t  |  s&t == s|t


