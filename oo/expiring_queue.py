
from datetime import datetime

class ExpiringQueue(object):

    def __init__(self, timeout):
        # items expire after timeout seconds.
        self.list = []
        self.timeout = timeout

    def append(self, item):
        self.list.append((item, datetime.now()))

    def pop(self): # the first non-expired item.
        self.__expunge__()
        return self.list.pop(0)[0]

    def __repr__(self):
        self.__expunge__()
        return str([item for (item, t0) in self.list])

    def __len__(self):
        self.__expunge__()
        return len(self.list)

    def __expunge__(self): # expired items.
        f = lambda t0: (datetime.now()-t0).seconds < self.timeout
        self.list = [(item, t0) for (item, t0) in self.list if f(t0)]


def test_ExpiringQueue():
    from time import sleep
    q = ExpiringQueue(5)
    q.append('a'); sleep(1)
    q.append(2); sleep(1)
    q.append([3]); sleep(1)
    print 'Q contents:', q
    print 'Q length:', len(q)
    print 'Q internals:', q.list
    print
    print '  time  len  contents'
    i = 5
    while i>=0:
        print '    %s    %s   %s' %(i, len(q),  q)
        i -= 1
        sleep(1)
        
    q.append(5)
    q.append('x')
    q.append({})
    print q
    sleep(5)
    print q



