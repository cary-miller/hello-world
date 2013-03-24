'''
'''





# ############################################################## # 
# ######################### Decorators ######################### # 
# ############################################################## # 

import time

def timeit(func):
    '''Print the elapsed time in running func.
    '''
    def inner(*a,**k):
        start = time.time()
        result = func(*a,**k)
        print func.__name__+ " Elapsed Time: %s" % (time.time() - start)
        return result
    return inner

def coroutine(func):
    '''Advance a coroutine to its first yield.
    '''
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start


