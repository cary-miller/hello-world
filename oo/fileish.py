'''
A class with a write method for simulating a file open for writing.
Could be useful in a pipeline?  Is possible to do same with attaching a
write method to a function?  Of course.  How about a function that
attaches a write method to itself?
'''

class Fileish(object):
    '''
    A file-like object,  with read/write methods.
    The write method is for writing TO this object.  Backwards from how I
    usually think of read/write but totally makes sense to a user.
    With the exception of the method names read/write this class bears no
    resemblance to any file objects.

    REDIRECTING sys.stdout WRITES TO THIS OBJECT.
    >>> f = Fileish()
    >>> sys.stdout = f
    >>> print 'yoohoo'
    >>> sys.stdout = sys.__stdout__
    >>> f.read()
    'yoohoo'
    '''
    def __init__(self):
        self.s = ''

    def write(self, s):
        assert type(s) == str, s
        # What shall we do with string s?
        self.s += s
        # For now just save it.

    def read(self):
        # Write self.s to someplace.  
        return self.s

    def clear(self):
        self.s = ''




def test_fileish():
    f = Fileish()
    f.write('hello\n')
    f.write('there\n')
    print f.read()
    ls = log_sim(sink=f)
    ls.next()
    ls.next()
    f.write('sucker\n')
    ls.next()
    ls.next()
    print f.read()


