# Python for Data Analysis

- Cary Miller
- Data Science / Business Analytics Meetup
- Mar 19, 2013
- CU Denver - North Classroom #1539 6:00-8:30

![python](http://i.imgur.com/bc2xk.png)



---
# Overview

- What/Why of Python
- How
- Overview of data analysis tools
- MapReduce in Python
- Insult detector
- Streaming Twitter Feed
- Concurrency


---
![python](http://i.imgur.com/bc2xk.png)

- easy reading, runs everywhere
- lots of libraries
- free, open source
- interactive interpreter (instant feedback)
- non-intrusive (think about the problem not the language)
- consenting adults (assumption of competence)
- multiple programming paradigms (oo/functional/...)
- 2/3 schism

---

# Let's look at code


---
# Code Sample

    !python

    def factorial(n):
        if n==0: 
            return 1
        return n * factorial(n-1)
 
 
    def factorial(n):
        assert type(n) == int and n >= 0
        if n==0: 
            return 1
        return n * factorial(n-1)


---
# Code Sample

    !python

    import requests

    def fetch_ob(url):
        return requests.get(url)


    def fetch(url):
        result = requests.get(url)
        if result.return_code ==200:
            headers = result['headers']
            html_doc = result.content
        return headers, html_doc
 




---
# Coroutine

    !python

    @coroutine
    def grep(pattern):
        print "Looking for %s" % pattern
        while True:
            line = (yield)
            if pattern in line:
                print line,

---
# An Interactive Interlude


demo_all.py
expiring_queue.py



 
---
# Data Analysis in Python

- [IPython] [IPython]
- [Numpy] [Numpy] (fast math libs in C,  vector/matrix operations)
- [Scipy] [Scipy]
- [Matplotlib] [Matplotlib]
![aplot](http://matplotlib.org/mpl_examples/pylab_examples/legend_demo2.png)


---
- [NLTK] [nltk]
- [Pandas] [pandas]
- [statsmodels] [statsmodels]
- [Orange] [orange]




---
# [Pandas] [pandas]

- Inspired by R and Matlab (but better)
- primary data structures are DataFrame and Series.


---
    !python
    >>> cat_data[:5]
                 Open   High    Low  Close   Volume  Adj Close
    Date                                                      
    2000-01-03  47.69  49.00  47.69  48.63  5055000      17.46
    2000-01-04  48.63  49.75  48.00  48.00  6181400      17.24
    2000-01-05  48.00  50.19  48.00  49.13  6398600      17.64
    2000-01-06  50.56  52.25  50.56  51.63  5140600      18.54
    2000-01-07  52.75  55.13  52.75  53.31  6360200      19.14


---
hierarchical indexing

    !python

    >>> import numpy as np
    >>> data = Series(np.random.randn(10), 
        index = [list('aaabbbccdd'), [1,2,3]*2 + [1,2,2,3]]) 
    >>> data
    a  1    0.387480
       2    0.179983
       3   -0.240402
    b  1    1.284860
       2   -0.131864
       3    1.184555
    c  1    0.398136
       2    1.718412
    d  2   -0.129306
       3   -0.434404

---
    !python
    >>> data.unstack()
             1         2         3
    a       0.387480  0.179983 -0.240402
    b       1.284860 -0.131864  1.184555
    c       0.398136  1.718412       NaN
    d            NaN -0.129306 -0.434404


---
    !python

    >>> data.index.names[None, None]

    >>> data.index.names = 'letter number'.split()

    >>> data.index.names
    ['letter', 'number']


    >>> data.swaplevel('letter', 'number')
    number  letter
    1       a         0.387480
    2       a         0.179983
    3       a        -0.240402
    1       b         1.284860
    2       b        -0.131864
    3       b         1.184555
    1       c         0.398136
    2       c         1.718412
            d        -0.129306
    3       d        -0.434404

---
    !python
    >>> data.sortlevel(1)
    letter  number
    a       1         0.387480
    b       1         1.284860
    c       1         0.398136
    a       2         0.179983
    b       2        -0.131864
    c       2         1.718412
    d       2        -0.129306
    a       3        -0.240402
    b       3         1.184555
    d       3        -0.434404


    >>> data.sortlevel(0)
    letter  number
    a       1         0.387480
            2         0.179983
            3        -0.240402
    b       1         1.284860
            2        -0.131864
            3         1.184555
    c       1         0.398136
            2         1.718412
    d       2        -0.129306
            3        -0.434404




---
    !python

    import pandas.io.data as web
    all_data={}
    for ticker in 'MSFT AAPL IBM GOOG CAT'.split():
        all_data[ticker] = web.get_data_yahoo(ticker, '1/1/2000', '1/1/2010')
    cat_data = all_data['CAT']
    high = cat_data.High
    high.plot()



---
    !python
    >>> cat_data[:5]
                 Open   High    Low  Close   Volume  Adj Close
    Date                                                      
    2000-01-03  47.69  49.00  47.69  48.63  5055000      17.46
    2000-01-04  48.63  49.75  48.00  48.00  6181400      17.24
    2000-01-05  48.00  50.19  48.00  49.13  6398600      17.64
    2000-01-06  50.56  52.25  50.56  51.63  5140600      18.54
    2000-01-07  52.75  55.13  52.75  53.31  6360200      19.14





    >>> cat_data.High
    Date
    2011-01-03    88.44
    2011-01-04    85.48
    2011-01-11    83.65
    ...
    2013-02-27    110.64
    2013-02-28    111.64
    2013-03-01    110.42
    Name: High, Length: 543


---
![cathigh]( ~/data/cat_high_daily.png )


---
# Pandas vs R

- Pandas better for data munging
- R has more extensive packages / lattice graphics / ggplot
- Go to the Pandas talk in Boulder, Thursday

---
# End of package overview

- IPython 
- Numpy for numeric/mathematical work
- Pandas for stats
- Orange for machine learning


---
# Map-Reduce

List comprehensions - Fast,  Concise,  Logical

    !python
    >>> nums = range(7)
    >>> nums
    [0, 1, 2, 3, 4, 5, 6]

    >>> [x**2 for x in nums]
    [0, 1, 4, 9, 16, 25, 36]

    >>> [x**2 for x in nums if x>2]
    [9, 16, 25, 36]

    >>> def f(x):
    ...     return x**2 + 3*x + 5 
    ... 

    >>> [f(x) for x in nums]
    [5, 9, 15, 23, 33, 45, 59]


 
---
# A Map-Reduce Example
[Finding Facebook Friends] [mapreduceFriends]

    !python
    # [person, (list of friends)]
    person_friends = [
        [A, (B,C,D)],
        [B, (A,C,D,E)],
        [C, (A,B,D,E)],
        [D, (A,B,C,E)],
        [E, (B,C,D)]
        ]

    [([A, B], [C, D]),
     ([A, C], [B, D]),
     ([A, D], [B, C]),
     ([B, C], [A, D, E]),
     ([B, D], [A, C, E]),
     ([B, E], [C, D]),
     ([C, D], [A, B, E]),
     ([C, E], [B, D]),
     ([D, E], [B, C])]




---
# Support functions 
    !python


    def partition(lst, func):
        '''Partition lst on value of func applied to each element.
        >>> partition(lst, lambda ob: ob[attr])
        >>> partition(lst, lambda sublst: sublst[i])
        >>> partition(lst, lambda ob: ob.attr)
        '''
        res = defaultdict(lambda:[])
        for ob in lst:
            res[func(ob)].append(ob)
        return res


    def flattened(lst):
        return [item for sublist in lst for item in sublist]
        # from Martelli of course


---
# The code
    !python

    def map_func(p_pals):
        person, friends = p_pals
        return [(sorted([person,pal]), friends) for pal in friends]


    mapped = flattened([map_func(p_pals) for p_pals in person_friends])

    part = partition(mapped, lambda ob: str(ob[0]))   
    grouped = sorted([(eval(k),[(b) for (a,b) in part[k]]) for k in part])

    reduced = [(k, list(set.intersection(*(set(s) for s in v)))) 
                                                    for (k,v) in grouped]
    common_friends = reduced

Map-reduce is a special case of list comprehension without filtering and
with constraints on input/output (key,value) pairs.

Of course map-reduce also requires ...


---
# Deep Breath

 
---
# Concurrency

Different kinds of concurrency for different problems

IO-bound

    - fetching multiple URLs
    - calling a web service on 1000's of documents.


CPU-bound

    - splitting huge data and processing small parts independently


---
# Jargon

Process: has its own resources (cpu, memory)

Thread

    - shares resources (cpu, memory)
    - from OS
    - subject to arbitrary interruption
    - shared state / locks / semaphores 
    - NOTE threads != shared state 

GIL: Global Interpreter Lock

Lightweight Process / green thread / greenlet

    - shares resources
    - coroutines
    - NOT subject to arbitrary interruption
    - VM vs OS

---
Shared state (evil)

asynchronous / synchronous / blocking / message passing

sequential / parallel

coroutine

(premptive / cooperative)  multi-tasking

deadlock : thread waiting (forever) for another thread to release a
    resource.

race condition : two threads attempting to change a resource
    simultaneously. 



---
# Python Concurrency (good/bad/ugly)

![good_bad_ugly](~/Downloads/alamogoodbadugly_8.jpg)

---


bad news

  + fundamentally broken (GIL)
  + contrast to Erlang

good news

  + Stackless (microthreads) (still has the GIL)
  + Jython 
  + Iron Python (Python in .Net)
  + Tulip (asynchronous I/O)


ugly

  + sorting it out

---
# At the practical level
 
- Threads   (Threading)
- Processes (multiprocessing)

Threads solve two problems

- Blocking
- Parallelism

Use case for threads:

- downloading multiple urls    
- processing multiple documents



---
# demo_threading.py





---
Threads are great *but*

- Arbitrary interruptions
- Heavy
    * Like a container ship with only 1 container
    * Cruise ship with only 1 passenger

So how else can we do two things at the same time? ...


---
# Asynchronicity
 
Blocking calls

   * reading a file
   * fetching a url

We would like to run jobs in parallel without threads.
Async means the function returns immediately and the result will show up
sometime later.  Inherently more complex than synchronous/blocking
programming.

Async is not built in to the language but there are lots of solutions.

   - Twisted (comprehensive, large, steep learning curve)

   - Eventlet, Greenlet, others
        * associated with green threads
        * coroutines

---
# callbacks vs message-passing

There is some overlap and ambiguity and issues relating to architecture vs
implementation.
But in large strokes:

- a callback is a function that somehow becomes "registered" 
    to listen for event A.
- a message is posted to a specific "mailbox", which may be specific to one
    owner or may have multiple watchers/listeners.
- in general message passing is simpler.  and definitely more consistent
    with the functional paradigm (events are global state).
- the two are not necessarily in conflict.  They have different niches.
- event-driven (callback) code is good for GUI's and web servers.
- message-passing more relevant for communication between well-known
    participants.

 

---
# Async details & example
 
Asynchronicity introduces complexity.

------ blocking / synchronous example

    - callbacks
    - message passing

------ asynchronous example

    - tulip == good/bad news


---
# Coroutines

Extreme lightweight green threads.

example: streaming twitter api


---
# [Kaggle] [kaggle]

- Competitive data analysis.
- Good data sets
- Insult detector


---
# Insult detector

- [nltk][nltk] *Natural Language Tool Kit*
- Insult detector
- Kaggle data ~ 4000 classified examples.


    Insult,Date,Comment==============================================
    1,20120530000452Z,"""Of course you would bottom feeder ..."""
    0,20120619201802Z,"""M\xe1tenlos!!\nhttp://1.bp.blogspot.com/-YVSZ"""
    1,20120619162450Z,"""You are\xa0 a fukin moron. \xa0\xa0 You are"""
    0,20120528135045Z,"""He is doing what any president doe's on ...."""
*    0,20120619193808Z,"""...yeah, and you're a f'ing expert....."""
    0,20120618201005Z,"""Those trails will definitely get plowed """
    0,20120529200220Z,"""Suh had a sack the last time they played."""
*    0,20120612001540Z,"""and you are support argument a-hole....\n\nNot"""
    1,20120619171832Z,"""You are a fucking dumb ass!.  Go back to you Xbox"""

NOTE:  many insults wrongly classified as non-insult.

---

    !python
    def main():
        data_ingestion() 
        feature_extraction()
        training()
        ensembling()
        validation()


---
# Feature Extraction

    !python
    def bad_word_in(msg): 
        return any(bad in msg for bad in bad_word_set)

    def bad_word_count(msg): 
        return sum(bad in msg for bad in bad_word_set)

    def starts_bad(msg): 
        return any(msg.startswith(bad) for bad in bad_word_set)

    def ends_bad(msg): 
        return any(msg.endswith(bad) for bad in bad_word_set)


    def you_are_an(msg): return 'you are an ' in msg

    def your_a(msg): return ' your a ' in msg

    def ur_a(msg): return ' ur a ' in msg

    def you(msg): return any(u(msg) for u in (you_are_an, your_a, ur_a))

---

    !python
    def bag_of_bigrams_words(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
        bigram_finder = BigramCollocationFinder.from_words(words)
        bigrams = bigram_finder.nbest(score_fn, n)
        return bag_of_words( words+bigrams )


    def bag_of_words(words, 
        stopwords = nltk.corpus.stopwords.words('english'),
        func2 = lambda w: w not in nltk.corpus.stopwords.words('english'),
        func1 = lambda w:True
        ):
        return {w:func1(w) for w in words if func2(w)}



---

    !python


    >>> row
    '"You\'re all upset, defending this hipster band...and WE\'RE the
    douches for reading the news and discussing it?\\r\\n\\r\\nPut down
    the PBR, throw away the trucker hat, shave off that silly shadow-beard,
    put down your "99%er" sign, and get a job, ION."'

    >>> msg
    'you re all upset  defending this hipster band...and we re the douches
    for reading the news and discussing it     put down the pbr  throw
    away the trucker hat  shave off that silly shadow beard  put down your
    99 er sign and get a job  ion'


    >>> msg_features(msg)
    {'shave': True, 
    ('that', 'silly'): True, 
    ('reading', 'the'): True,
    'bad_word_ratio': 'low', 
    ('hipster', 'band...and'): True, 
    ('trucker', 'hat'): True, 
    'trucker': True,
    ('shadow', 'beard'): True,
    'word_diversity': 1.0, 
    ...



---
# Training

    !python
    def training(): 
        prep_dict = data_ingestion() 
        train_set, test_set = prep_dict[True], prep_dict[False] #

        test_feat = feature_extraction(test_set)
        train_feat = feature_extraction(train_set)

        nbc = NaiveBayesClassifier.train(train_feat)
     


---
# Validation


    !python
    >>> validation()
    overall accuracy:  0.753861484803
    Most Informative Features
                        shut = True        35.1 : 1.0
                   you______ = True        24.3 : 1.0
                      idiot. = True        22.5 : 1.0
               ('are', 'an') = True        21.1 : 1.0
                        idio = True        17.1 : 1.0
    false negatives: 106
    false positives: 388
    true positives: 419
    true negatives: 1094



---
# TODO 

- improvements to all parts 


---
# Another example


---
# Streaming Twitter Feed

Twitter provides a stream service.  

- Provides a sample of the complete twitter stream.
- [Tweepy] [tweepy] library
- functional code / Coroutines
- seive
- tree classifier


---
# Tweepy Stream Listener

    !python
    class CustomStreamListener2(tweepy.StreamListener):
        def __init__(self, target): # target.send(status)
            self.target = target
            tweepy.StreamListener.__init__(self)

        def on_status(self, status):
            self.target.send(status)

        def on_error(self, status_code):
            print >> sys.stderr, '[Error] status code:', status_code
            return True # Don't kill the stream

        def on_timeout(self):
            print >> sys.stderr, '[Timeout]'
            return True # Don't kill the stream



---
    !python
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

---
# Coroutine Filters

    !python
 
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


---
    !python
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



---
    !python
    @coroutine
    def printer_status(mark, sink=None):
        ''' A sink.  A coroutine that receives data.  '''
        if sink is None: 
            sink=sys.stdout
        while True:
            status = (yield) # target.send lands here
            msg = '%s %d [%s]  %s\n' %(ts(), pid(), mark, status.text)
            sink.write(msg)


---
A function that chains the 3 above.

    !python
    # TODO rename
    def divert(lang, word, sink=None):
        '''A chain of filters terminating in a sink.
        '''
        return language_user(lang, 
            grep_status(word, 
            printer_status('%s %s' %(lang,word), sink)))


---
Examples of the code in action.

    !python
    # twit_stream(printer_status('>>'))
    # twit_stream(printer_status('>>', open('tweet_es.log', 'a')))
    # twit_stream(language_user('es'))
    # twit_stream(language_user('es', out_file=open('tweet_es.log', 'a')))
    # twit_stream(grep_status('love'))
    # twit_stream(grep_status(['love', 'hate']))
    # twit_stream(divert('en', 'love'))
    # twit_stream(broadcast(bc))




---
    !python
    # twit_stream(printer_status('>>')) 
 
    2013/03/17 15:32:08 89288 [>>]  @stephbutlerrrx no it's not on all week x
    2013/03/17 15:32:08 89288 [>>]  @j0e_lcfc I know that now hahah x
    2013/03/17 15:32:08 89288 [>>]  Photo: 16.03 - (x) http://t.co/AZZTnnw0Qn
    2013/03/17 15:32:08 89288 [>>]  Quieres ser diferente x gotay
    2013/03/17 15:32:08 89288 [>>]  RT @onedirectlons: Retweet if you followed
        @Adzlegends for me so i can follow you back x
    2013/03/17 15:32:08 89288 [>>]  @littlemixermuff x http://t.co/CYxl1IrwTM
    2013/03/17 15:32:09 89288 [>>]  o(･x･)/ 名探偵コナン
        全巻セット　全巻専門書店　漫画全巻ドットコム [blog] http://t.co/nVWwahuyNf

---
    !python
    # twit_stream(language_user('es'))
 
    2013/03/17 15:37:29 89288 [es]  @michiiGarcia corriendo te lo voy a ir a
        dejar vas a ver x) nta otro día te hago si queres /o/
    2013/03/17 15:37:29 89288 [es]  @GloriaTrevi x que eres tann taannn
        hermosa"???
    2013/03/17 15:37:30 89288 [es]  "-¿Entendiste el ejercicio de matemáticas?
        -Sí. -¿dónde está la "x"? -En los tweets de Zayn." LOL
    2013/03/17 15:37:30 89288 [es]  RT @iohmygaga: No salio de The X Factor,
        ni de Disney sino del mar y de Youtube, CON USTEDES PETER LA ANGUILA.
    2013/03/17 15:37:30 89288 [es]  #gh14 Lo peor d tdo s k las parejas k hay
        fuera merecen x lo menos una pekeña explicaciòn, no hay excusa cuando stan
        rodeados d camaras
     
 
 ---
    !python
    # twit_stream(grep_status(['love', 'hate']))
 
    2013/03/17 15:40:20 89288 [love hate]  RT @LittleMixOffic: Today was sick!
        I love America, our US mixers are insane! Thank you for everything guys!
        :D #LittleMixInTheUS Leigh x
    2013/03/17 15:40:20 89288 [love hate]  @glovernator1 @macca_s180 Aw lm
        sure it will be!! So excited for you all 😃 x
    2013/03/17 15:40:21 89288 [love hate]  RT @Welovesbiebers: @swagfrombrazil
        ( ) pode melhorar
        (x) gostei (x) lindo ( ) perfeição 
        ( ) passa a senha
     
 
 
---
# Streaming Twitter Feed

- proof-of-concept
- data pipeline
- fan out
- fan in
- needs asynchronicity
- maybe rewrite with greenlets


---
# Conclusions

- Python is great for data analysis
- Concurrency is a weak point


---
# 2 or 3 ?
 
- 2 for Libraries
- 3 for Concurrency


---
# Questions?

[kaggle]: http://www.kaggle.com/
[tweepy]: http://tweepy.github.com/
[functional]: http://en.wikipedia.org/wiki/Functional_programming
[functional python]: http://docs.python.org/2/howto/functional.html

[ipython]: http://ipython.org/
[numpy]: http://www.numpy.org/
[scipy]: http://www.scipy.org/
[matplotlib]: http://matplotlib.org/
[nltk]: http://nltk.org/
[pandas]: http://pandas.pydata.org/
[statsmodels]: http://statsmodels.sourceforge.net/
[orange]: http://orange.biolab.si/
[blaze]: http://continuum.io/blog/blaze

[mouse_python]: http://www.blog.pythonlibrary.org/ 
[mouse_python_queue]: http://www.blog.pythonlibrary.org/2012/08/01/python-concurrency-an-example-of-a-queue/
[benderski]: http://eli.thegreenplace.net/
[beazley]: http://www.dabeaz.com/
[beazley_coroutines]: http://www.dabeaz.com/coroutines/

[pycon]: https://us.pycon.org/2013/
[pydata]: http://pydata.org/
[frpythoneers]: http://www.meetup.com/frpythoneers/

[mapreduceFriends]: http://stevekrenzel.com/finding-friends-with-mapreduce
[erlang]: http://www.erlang.org/
[learnyousomeerlang]: http://learnyousomeerlang.com/





