#!/usr/bin/env python
__doc__="""
.. Hello.  Yoohoo!

Parsing CSV data
========================

First some useful imports and variables.
Then a quick look at the test data.

>>> from pprint import pprint
>>> numeric_data_file = "/home/cary/data/test.numeric.csv"  
>>> quoted_data_file = "/home/cary/data/test.quoted.csv"  
>>> print open(numeric_data_file).read()
1,2,3,4
1,  2,  3,      4
1,,3,4
,2,3,4
1,2,3,
,2,3,
,,,
<BLANKLINE> 

Without optional arguments the output consists of strings.

>>> pprint(simple_csv(numeric_data_file))
[['1', '2', '3', '4'],
 ['1', '  2', '  3', '      4'],
 ['1', '', '3', '4'],
 ['', '2', '3', '4'],
 ['1', '2', '3', ''],
 ['', '2', '3', ''],
 ['', '', '', '']]

An optional conversion function converts strings to something else.
Values that generate an exception are returned unchanged.

>>> pprint(simple_csv(numeric_data_file, convert=int)) # ints
[[1, 2, 3, 4],
 [1, 2, 3, 4],
 [1, '', 3, 4],
 ['', 2, 3, 4],
 [1, 2, 3, ''],
 ['', 2, 3, ''],
 ['', '', '', '']]

>>> pprint(simple_csv(numeric_data_file, convert=float))  # floats
[[1.0, 2.0, 3.0, 4.0],
 [1.0, 2.0, 3.0, 4.0],
 [1.0, '', 3.0, 4.0],
 ['', 2.0, 3.0, 4.0],
 [1.0, 2.0, 3.0, ''],
 ['', 2.0, 3.0, ''],
 ['', '', '', '']]


With optional delimiter.

>>> simple_csv(numeric_data_file, convert=float, delim=',') 
... # doctest: +NORMALIZE_WHITESPACE
[[1.0, 2.0, 3.0, 4.0],
 [1.0, 2.0, 3.0, 4.0],
 [1.0, '', 3.0, 4.0],
 ['', 2.0, 3.0, 4.0],
 [1.0, 2.0, 3.0, ''],
 ['', 2.0, 3.0, ''],
 ['', '', '', '']]



Character Data
=====================

Here is the test data.

>>> print 'Character Data'
Character Data
>>> print open(quoted_data_file).read()
"hello_mello_yello",2,    "a_b_",      "_c_d"
"hello,mello,yello",2,    "a,b,",      ",c,d"
"hello,mello,yello",  2,  "a,b,",      ",c,d"
"hello,mello,yello",,"a,b,",           ",c,d"
,2,"a,b,",",c,d"
"hello,mello,yello",2,"a,b,",
,2,"a,b,",
,,,
<BLANKLINE> 

.. code-block:: python

    # Does not work unless pygments installed.
    import os
    for in os.uname():
        print i

>>> print 'foo'
foo
"""


def simple_csv(fname):  
    return [line[:-1].split(',') for line in open(fname).readlines()]  
# Leaves everything as a string.

# Same as above but attempts type conversion.
# Items that raise an Error on conversion are left alone.
# Only anticipate empty strings as the problem.
def simple_csv(fname, *op_list):  
    data = [line[:-1].split(',') for line in open(fname).readlines()]  
    try: convert = op_list[0]  # optional args in a list  
    except IndexError: return data  
    for i in range(len(data)):  
        for j in range(len(data[i])):  
            try:  
                data[i][j] = convert(data[i][j])  
            except:  
                pass  
    return data  
# also should pass optional delimiter.
# Maybe convert options to keywords.


import csv
def simple_csv(fname, **op_keys):
    try: delim = op_keys['delim']
    except KeyError:  delim = ','
    data = [row for row in csv.reader(open(fname))]
    try: convert = op_keys['convert']  
    except KeyError: return data
    for i in range(len(data)):
        for j in range(len(data[i])):
            try: data[i][j] = convert(data[i][j])
            except: pass  # Leave the item unaltered.
    return data
# The csv module deals with headers (and other things).



def quoted_csv(fname):
    '''
    Hello Title
    =================

    Hello Section
    ====================

    Below is some kind of rst list

    x: `int`
        parameter, first
    y: `int`
        parameter, second
    '''
    return [line for line in open(fname)]

#quo = quoted_csv(quoted_data_file)

import doctest
if __name__=='__main__':
    doctest.testmod()
else:
    exec(doctest.script_from_examples(__doc__))
    # This allows to say >>> from here import *
    # and get all vars defined in the doc string placed into the
    # namespace.  A nice separation of production from testing.  But yet
    # the testing stuff is available when you want it.


