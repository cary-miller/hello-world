




class Proxy(object):
    '''A class that wraps an existing object overriding the
    __getattribute__ method.
    With this it is possible to extend any object, including ones
    where we have no access to source code.
    '''
    def __init__(self, ob):
        self.ob = ob

    def __getattribute__(self, name):
        '''
        '''
        ob = object.__getattribute__(self, 'ob') # unbound method
        # Unbound __getattribute__ is required to avoid circular references.
        if name=='ob': return ob
        if name in 'blah dah bada daha':
            return name # or something
        return ob.__getattribute__(name)



def test_proxy():
    try:
        from cStringIO import StringIO
        op = Proxy(StringIO())
        op.write('hello') 
        assert op.blah == 'blah' 
        op.seek(0)
        assert op.read() == 'hello'
    finally: globals().update(locals())




