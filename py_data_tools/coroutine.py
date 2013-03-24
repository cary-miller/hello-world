def coroutine(func):
    '''Advance a coroutine to its first yield.
    '''
    def start(*args,**kwargs):
        cr = func(*args,**kwargs)
        cr.next()
        return cr
    return start


