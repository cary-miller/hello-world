'''Tests for the CampSpot programming challenge.
Some of the tests use the sample data from the problem statement so the json
file must be in this directory.

To run it at the command line:

# python tests.py
'''

from challenge import *


def test_convert_dates():
    fname = 'test-case.json'
    ob = raw_json(fname)
    converted = convert_dates(ob)
    assert converted['gapRules'] == ob['gapRules']
    assert converted['campsites'] == ob['campsites']

    for key in ob['search']:
        assert converted['search'][key] == date_string_2_ob(ob['search'][key])

    for (truth, q) in zip(ob['reservations'], converted['reservations']):
        assert truth['campsiteId'] == q['campsiteId']
        assert date_string_2_ob(truth['startDate']) == q['startDate']
        assert date_string_2_ob(truth['endDate']) == q['endDate']

    print 'convert_dates ok'


def test_is_in():
    dates_desired = (datetime(2016, 6, 10, 0, 0), datetime(2016, 6, 12, 0, 0))
    dates_available = (datetime(2016, 6, 7, 0, 0), datetime(2016, 6, 14, 0, 0))
    assert is_in(dates_desired, dates_available)
    assert is_in(dates_desired, dates_desired)
    assert not is_in(dates_available, dates_desired)
    print 'is_in ok'


def test_gaps_left():
    dates_desired = (datetime(2016, 6, 10, 0, 0), datetime(2016, 6, 12, 0, 0))
    dates_available = (datetime(2016, 6, 7, 0, 0), datetime(2016, 6, 14, 0, 0))
    assert gaps_left(dates_desired, dates_available) == (3, 2)
    assert gaps_left(dates_desired, dates_desired) == (0, 0)
    assert gaps_left(dates_available, dates_desired) is None
    print 'gaps_left ok'
 
 
def test_openings_for():
    '''testing on input data.
    '''
    fname = 'test-case.json'
    ob = raw_json(fname)
    converted = convert_dates(ob)
    reservations = converted['reservations']
    for id in range(1, 10):
        campsite_reservations = [dct for dct in reservations if dct['campsiteId'] == id]
        openings = openings_for(id, reservations)
        for (res, opening) in zip(campsite_reservations, openings):
            assert res['endDate'] + timedelta(days=1) == opening[0]
    print 'openings_for ok'


def test_find_campsites():
    answer = '''
        "Daniel Boone Bungalow"
        "Teddy Rosevelt Tent Site"
        "Bear Grylls Cozy Cave"
        "Wyatt Earp Corral"
    '''
    # NOTE
    # Problem answer in email contains a typo.
    # "Teddy Roosevelt Tent Site"
    # should be
    # "Teddy Rosevelt Tent Site"
    # or json data should be changed.  Roosevelt is the correct spelling.
    fname = 'test-case.json'
    for name in find_campsites(fname):
        assert str(name) in answer
    print 'find_campsites ok'


test_is_in()
test_gaps_left()
test_openings_for()
test_convert_dates()
test_find_campsites()
