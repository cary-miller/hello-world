# cobroadcast.py
#
# An example of broadcasting a data stream onto multiple coroutine targets.
# 
# Based on Beazley's coroutine examples.
# http://dabeaz.com/coroutines/
# http://antroy.blogspot.com/2007/04/python-coroutines.html

from pprint import pprint
import re
import time
from datetime import datetime
import random
import tweepy
from coroutine import coroutine

# Broadcasting an infinite Twitter stream.
execfile('../util/keys.py')

def ts(): return datetime.now().strftime('%Y/%m/%d %H:%M:%S')

def pid(): return os.getpid()


@coroutine
def language_user(lang, f_target=None, out_file=None):
    '''A filter.
    '''
    if f_target is None:
        f_target = printer_status(lang)
    if out_file:
        f_target = printer_status(lang, out_file)
    while True:
        status = (yield)           # Receive a status
        if status.user.lang == lang:
            f_target.send(status)    # Send to next stage


@coroutine
def grep_status(pattern_list, f_target=None):
    '''A filter.
    # accepts a pattern or LIST of patterns.
    '''
    if type(pattern_list) not in (list, tuple):
        pattern_list = [pattern_list]
    if f_target is None:
        f_target = printer_status(' '.join(pattern_list))
    while True:
        status = (yield)           # Receive a status
        if any(pattern in status.text for pattern in pattern_list):
            f_target.send(status)    # Send to next stage




@coroutine
def printer_status(mark, sink=None):
    ''' A sink.  A coroutine that receives data.  '''
    if sink is None: sink=sys.stdout
    i=0
    while True:
        
        status = (yield) # target.send lands here
        msg = '%s %d [%s]  %s\n' %(ts(), pid(), mark, status.text)
        i+=1
        try:
            sink.write(msg)
        except Exception, err:
#            print ts() + str(err) + msg
            print  msg
            sink.write(msg.encode('utf-8'))
            # was catching encoding issue.
        finally: 
            globals().update(locals())


def debug_encoding():
    msg = u'''[>>] 0  RT @DjSpeechless: [MIXTAPE] $wagg - DJ Speechless x OsoENT
    Presents: "More Than Swag" http://t.co/rHBECMXg \u2026 @SwaggOTOD
    @DJSpeechless @H ...\n'''
    print msg
    with open('tweet_es.log', 'w') as fh :
        fh.write(msg.encode('utf-8'))
    # UnicodeEncodeError: 'ascii' codec can't encode character u'\u2026'
    # in position 115: ordinal not in range(128)



# TODO rename
def divert(lang, word, sink=None):
    '''A chain of filters terminating in a sink.
    '''
    return language_user(lang, 
        grep_status(word, 
        printer_status('%s %s' %(lang,word), sink)))


@coroutine
def classify_status(classifier):
    ''' A sink.  A coroutine that receives data. '''
    while True:
         status = (yield) # target.send lands here
         print classifier(status.text), str(status)


@coroutine
def broadcast(l_targets):
    while True:
        item = (yield)
        for f_target in l_targets:
            f_target.send(item) # send to another coroutine.



class CustomStreamListener2(tweepy.StreamListener):
    def __init__(self, target): # target.send(status)
        self.target = target
        tweepy.StreamListener.__init__(self)

    def on_status(self, status):
        try:     self.target.send(status)
        finally: globals().update(locals())

    def on_error(self, status_code):
        print >> sys.stderr, '[Error] status code:', status_code
        return True # Don't kill the stream
        return False # kill the stream

    def on_timeout(self):
        print >> sys.stderr, '[Timeout]'
        return True # Don't kill the stream



def twit_stream(processor):
    '''Data source.  Fetches twitter stream.  Directs the stream to
    multiple watchers.
    '''
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    streaming_api = tweepy.streaming.Stream(auth, 
        CustomStreamListener2(processor), 
        timeout=60)
    try: streaming_api.filter(None, 'x') # no filtering.
    except KeyboardInterrupt: print '\n'
    except Exception,e:
        print "Exception: %s" % str(e)
        time.sleep(1)




def demo_bc(): # ################ some examples ################ #

    # Printers #
    p_generic = printer_status('pgen') # print to stdout
#    p_file = printer_status('pf', open('file1.dat')) # print to file


    # Analyzers #
    # One could define an analyzer similar to the way printers are defined.
    # Or one could simply add a line to the printer.


    # Filters #
    f_you  = grep_status('you', p_generic) # messages containing 'you'
    f_me   = grep_status('me', p_generic) # messages containing  'me'
    f_uNme = grep_status('you', grep_status('me', p_generic) ) # you & me
    # Above gets both 'you' and 'me'.  Contrast with 
    f_youOrMe  = grep_status(['you', 'me'], p_generic) # 'you' OR 'me'

    save_you  = grep_status('you', printer_status('su', open('tweet_you.log'))) 
    with open('tweet_you.log') as fh:
        analyze_kill = grep_status('kill', printer_status('ak', fh)) 


    # List of filters to be targeted by a broadcaster #
    bc = [grep_status('python'),
          language_user('es'),
          divert('en', 'kill'),
          divert('en', 'love'),
          divert('en', 'hate'),
         ]
    globals().update(locals())


    # twit_stream(printer_status('>>'))
    # twit_stream(printer_status('>>', open('tweet_es.log', 'a')))
    # twit_stream(language_user('es'))
    # twit_stream(language_user('es', out_file=open('tweet_es.log', 'a')))
    # twit_stream(grep_status('love'))
    # twit_stream(grep_status(['love', 'hate']))
    # twit_stream(divert('en', 'love'))
    # twit_stream(divert('en', 'love', open('tweet_es.log', 'a')))
    # twit_stream(broadcast(bc))


 
       
def unique_in(repo):
    '''Whatever the result of func, make sure it is unique in set repo.
    '''
    def outer(func):
        def inner(*a,**k):
            result = func(*a,**k)
            while result in repo:
                result = func(*a,**k)
            repo.add(result)
            return result
        return inner
    return outer


def name_it(func):
    func.name='x'
    return func


def demo_unique_in():
    # example of using unique_in
    id_repo = set()
    @unique_in(id_repo)
    def generate_id():
        return random.random()
    print id_repo
    for i in range(4): generate_id()
    print id_repo


import inspect
def g(): 
    self_name = inspect.getframeinfo(inspect.currentframe()).function
    # What a tedious way to get one's own name !!!!!!!!!!!!!!!!!!!!!!
    # But it works.
    self = eval(self_name)
    i=0
    while True:
        word = (yield)
        print 'g.%d %s' % (i, word)
        yield (i, word)
        i+=1

def g(): 
    i=0
    while True:
        word = (yield)
        print 'g.%d %s' % (i, word)
        yield (i, word)
        i+=1



f = g(); f.next()
h = g(); h.next()

def i_gen():
    i=0
    while True:
        yield i
        i+=1

i = i_gen()

#f.send('foo'+str(i.next()))
# "set noautoindent
# " for pasting from outside.
# http://superuser.com/questions/134709/how-can-i-keep-the-code-formated-as-original-source-when-i-paste-them-to-vim

start = time.time()
tick = lambda:'%1.2f' %(time.time()-start)


# Threadless concurrency in Python.
# message-passing
# functional
# analyze the twitter stream.
# erlang erlports
# 
# 
#
