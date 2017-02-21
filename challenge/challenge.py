'''Solution to the CampSpot programming challenge.
Takes an optional json filepath or fname in this directory as input.  Default
filename is shown below in the __main__ block.
Prints to stdout the names of campsites that match the search range and gap
rules.
To run it at the command line:

# python challenge.py [json_filepath]
'''

import json
from datetime import datetime, timedelta


def date_string_2_ob(ds):
    '''
    >>> date_string_2_ob('2016-06-07') 
    datetime.datetime(2016, 6, 7, 0, 0)
    '''
    return datetime.strptime(ds, '%Y-%m-%d')


def convert_dates(ob):
    '''ob is a dictionary.   The values are themselves data structures
    and some of the sub-values in those are date strings.   Return a dictionary
    identical to the input ob but with all date strings converted to datetime
    objects.
    '''
    assert sorted(ob.keys()) == sorted(['gapRules', 'search', 'campsites', 'reservations'])

    res = {}
    res['gapRules'] = ob['gapRules']
    res['campsites'] = ob['campsites']

    res['search'] = {}
    for key in ob['search']:
        res['search'][key] = date_string_2_ob(ob['search'][key])
    
    res['reservations'] = []
    for dct in ob['reservations']:
        foo = {}
        foo['campsiteId'] = dct['campsiteId']
        foo['startDate'] = date_string_2_ob(dct['startDate'])
        foo['endDate'] = date_string_2_ob(dct['endDate'])
        res['reservations'].append(foo)

    return res


def openings_for(id, reservations):
    '''
    reservations is the data structure from the input json with datestrings
    converted to datetime objects.  id is an integer.
    Return the available openings that correspond to the reservations for
    campsite, id.
    '''
    args = [dct for dct in reservations if dct['campsiteId'] == id]
    campsite_reservations = []
    for dct in args:
        campsite_reservations.append((dct['startDate'], dct['endDate']))
    openings = []
    N = len(args)

    # Openings go between reservations.
    for i in range(N - 1):
        start = campsite_reservations[i][1] + timedelta(days=1)
        end = campsite_reservations[i+1][0] - timedelta(days=1)
        openings.append((start, end))

    # If only one reservation, the one opening follows it.
    if N == 1:
        start = campsite_reservations[0][1] + timedelta(days=1)
        magicnumber = 100
        end = start + timedelta(days=magicnumber)
        return [(start, end)]

    # Tack on an opening after all current reservations
    next_available_date = campsite_reservations[-1][1] + timedelta(days=1)
    magicnumber = 30
    final_opening = (next_available_date, next_available_date + timedelta(days=magicnumber))
    openings.append(final_opening)
    return openings


def campsite_name_for(id, ob):
    dct = [d for d in ob['campsites'] if d['id'] == id]
    return dct[0]['name']


def is_in(dates_desired, dates_available):
    '''
    Both parameters are pairs of datetime objects as a 2-tuple.
    >>> dates_desired = (datetime(2016, 6, 10, 0, 0), datetime(2016, 6, 12, 0, 0))
    >>> dates_available = (datetime(2016, 6, 7, 0, 0), datetime(2016, 6, 14, 0, 0))

    Return True/False answering the question:
    Are dates_desired contained in dates_available?
    >>> is_in(dates_desired, dates_available)
    True
    '''
    desired_start, desired_end = dates_desired
    available_start, available_end = dates_available
    if desired_start >= available_start and desired_end <= available_end:
        return True
    return False


def gaps_left(dates_desired, dates_available):
    '''
    Both parameters are pairs of datetime objects as a 2-tuple.
    >>> dates_desired = (datetime(2016, 6, 10, 0, 0), datetime(2016, 6, 12, 0, 0))
    >>> dates_available = (datetime(2016, 6, 7, 0, 0), datetime(2016, 6, 14, 0, 0))

    >>> gaps_left(dates_desired, dates_available)
    (3, 2)
    
    '''
    if not is_in(dates_desired, dates_available):
        return
    desired_start, desired_end = dates_desired
    available_start, available_end = dates_available
    gap1 = abs((available_start - desired_start).days)
    gap2 = (available_end - desired_end).days
    return (gap1, gap2)


def raw_json(fname):
    with open(fname) as fh:
        s = fh.read()
    return json.loads(s)


def disallowed_gaps(ob):
    return set([dct['gapSize'] for dct in ob['gapRules']])


def find_campsites(fname):
    '''Given a filepath or fname in this directory, return the solution to the 
    CampSpot challenge.
    fname is a json file containing a single object as described in the problem
    statement.
    '''
    ob = raw_json(fname)
    converted = convert_dates(ob)
    reservations = converted['reservations']
    search = converted['search']
    dates_desired = sorted(search.values())
    all_ids = [thing['id'] for thing in ob['campsites']]
    res = []
    for id in all_ids:
        for open_interval in openings_for(id, reservations):
            gaps = gaps_left(dates_desired, open_interval)
            disallowed = disallowed_gaps(ob)
            if gaps and disallowed.intersection(gaps) == set():
                res.append(campsite_name_for(id, ob))
    return res


if __name__ == '__main__':
    import sys
    try:
        fname = sys.argv[1]
    except IndexError:
        fname = 'test-case.json'
    for name in find_campsites(fname):
        print name
