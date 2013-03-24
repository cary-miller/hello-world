'''
Unlike the demo on the web page, this actually works.
The parallel is indeed parallel and indeed goes faster.
'''

from demo_deco import timeit
from urls import urls

import eventlet
requests = eventlet.import_patched('requests')


def fetch(url):
    return requests.get(url)

@timeit
def parallel(urls):
    pool = eventlet.GreenPool()
    for body in pool.imap(fetch, ['http://'+u for u in urls]):
        print body.url


@timeit
def sequential(urls):
    for url in urls:
        body = fetch('http://'+url)
        print body.url




