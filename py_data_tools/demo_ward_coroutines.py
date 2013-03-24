'''
http://excess.org/article/2013/02/itergen2/
'''

from coroutine import coroutine

@coroutine 
def running_avg():
    "coroutine that accepts numbers and yields their running average"
    total = float((yield))
    count = 1
    while True:
        num = yield total / count
        count += 1
        total += num




@coroutine
def rock_paper_scissors():
    """
    coroutine for playing rock-paper-scissors

    yields: 'invalid key': invalid input was sent
            ('win', player, choice0, choice1): when a player wins
            ('tie', None, choice0, choice1): when there is a tie
            None: when waiting for more input

    accepts to .send(): (player, key):
        player is 0 or 1, key is a character in 'rps'
    """
    valid = 'rps'
    wins = 'rs', 'sp', 'pr'
    result = None

    while True:
        chosen = [None, None]
        while None in chosen:
            player, play = yield result
            result = None
            if play in valid:
                chosen[player] = play
            else:
                result = 'invalid key'
            print chosen

        if chosen[0] + chosen[1] in wins:
            result = ('win', 0) + tuple(chosen)
        elif chosen[1] + chosen[0] in wins:
            result = ('win', 1) + tuple(chosen)
        else:
            result = ('tie', None) + tuple(chosen)

#We play this game by passing (player number, play) tuples to .send()

rps = rock_paper_scissors()
#rps.send((0, 'r'))
#rps.send((1, 'p'))


@coroutine
def telnet_filter():
    """
    coroutine accepting characters and yielding True when the character
    passed is actual input or False when it is part of a telnet command.
    """
    actual_input = None
    while True:
        print 'block 0'
        key = yield actual_input # normal
        print 'yield ', actual_input
        print '   key:', ord(key)
        if key != chr(255):
            actual_input = True
            print 'normal', ord(key), '==%s==' %key
            print
            continue

        print 'block 1'
        # key == 255 => grab next key
        key = yield False # command
        print 'yield False(prevkey 255)'
        print '   key:', ord(key)
        if key == chr(255):
            actual_input = True
            print 'command', ord(key)
            print
            continue

        print 'block 2   ', ord(key)
        actual_input = False
        if key == chr(250):
            print 'start subnegotiation', ord(key)
            while key != chr(240):
                key = yield False # subnegotiation
                print '    yield False next:', ord(key)
            print
        else:
            yield False # parameter
            print '  yield False (parameter)  '
            print


keep = telnet_filter()
chatter = ('\xff\xfd\x03si\xff\xfb"gn\xff\xfa"\x03\x01\x00\x00\x03b'
           '\x03\x04\x02\x0f\x05\x00\x00\x07b\x1c\x08\x02\x04\tB\x1a'
           '\n\x02\x7f\x0b\x02\x15\x0f\x02\x11\x10\x02\x13\x11\x02'
           '\xff\xff\x12\x02\xff\xff\xff\xf0al\xff\xfd\x01')

def test_telnet_filter():
    for c in chatter:
        if keep.send(c):
            print c,



# ok.  So that is really cool.
# But he goes on to do this interesting cross-network version that is highly
# specialized for its one case.  He uses low-level socket code to avoid
# blocking, on code that is controlled by him at both ends.
# I want to do something more general,  call arbitrary code without blocking.
# 
# That seems to require some sort of monkey-patched http client.  See
# demo_eventlet.

@coroutine 
def fetch():
    import eventlet
    requests = eventlet.import_patched('requests')
    "coroutine that accepts urls and yields objects"
    ob = lambda x:x
    ob.url = 'x'
    while True:
        url = yield ob.url
        ob = requests.get(url)
        print ob.url
 

from demo_deco import timeit
from urls import urls

@timeit 
def g(func, urls):
    f = func()
    return [f.send('http://'+url) for url in urls]
    # Does the work sequentially.


