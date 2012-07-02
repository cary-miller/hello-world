#!/usr/bin/env python2.7

import urllib
from xml.etree import cElementTree
import re
import datetime
from cStringIO import StringIO
import json
from pprint import pprint
import os


def strip_ns(xml_string):
    return re.sub("xmlns='[^']+'", '', xml_string)


def name_contains(node, word):
    return word in node.find('name').text


def pyg_func(pyg):
    '''Parse a multi-line string of coordinate triples, into pairs of
    floats, discarding the third coordinate.
    Input: a Polygon elementtree node.
    Output: table as a list of lists.
    '''
    s = pyg.find('.//coordinates').text
    return [map(float, row.split(',')[:2]) for row in s.split()]


def waldo( basename = 'ActiveFirePerimeters'):
    data_dir = '/Users/marymiller/data/fire/'
    fname = os.path.join(data_dir, basename+'.kml' )
    json_fname = os.path.join(data_dir, basename+'.json')

    fp = StringIO(strip_ns(open(fname).read())) # acts like an open file ob.
    tree = cElementTree.parse(fp)

    waldo = [node for node in tree.iterfind('.//Placemark') if name_contains(node, 'Waldo')]
    assert len(waldo) == 2
    multi_geom = waldo[1].find('MultiGeometry')
    polygons = multi_geom.findall('Polygon')

    coord_list = [pyg_func(pyg) for pyg in polygons]
    jstring = json.dumps(coord_list) # Write json to file or send to R
    with open(json_fname, 'w') as jf:
        jf.write(jstring)
    return jstring

print waldo( basename = 'ActiveFirePerimeters_2012_06_27')


