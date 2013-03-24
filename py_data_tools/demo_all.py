
import requests


def fetch_ob(url):
    return requests.get(url)


def fetch(url):
    result = requests.get(url)
    if result.return_code ==200:
        headers = result['headers']
        html_doc = result.content
    return headers, html_doc



urls = ['www.d3js.org', 'www.erlang.org', 'www.jquery.org', 'www.lisp.org']
# demo list comprehension
# demo tab tab



# ################################################## #
# ################################################## #
# ################################################## #


from datetime import datetime 

date_string = '2013/01/13 01:45:03 PM MST'
date_string = 'Mon Jan 13 01:45:03 PM MST 2013'
# http://docs.python.org/2/library/datetime.html

# Use the interpreter to demo str(fp)time
# tracebacks are your friend



# ################################################## #
# ################################################## #
# ################################################## #


# The lightweight alternative to threads.

from coroutine import coroutine

@coroutine
def grep(pattern):
    print "Looking for %s" % pattern
    while True:
        line = (yield)
        if pattern in line:
            print line,



# ################################################## #
# ################################################## #
# ################################################## #





