'''
Dictionary Functions 
'''

def subdict(dct, keys):
    '''Subset dict, keeping keys, tossing other keys.
    >>> d = dict(a=1,b=2,c=3)
    >>> assert subdict(d, ('a', 'c')) == {'a': 1, 'c': 3}
    '''
    return dict((key, value) for (key, value) in dct.items() if key in keys)



def dict_key_translate(dct, mapping, keep_all_keys=True):
    '''Translate dict keys, optionally keeping only mapped keys.
    >>> d = dict(a=1,b=2,c=3)
    >>> m = (('a','x'), ('b','y'))
    >>> assert dict_key_translate(d, m) == {'y': 2, 'x': 1, 'c': 3}
    >>> assert dict_key_translate(d, m, keep_all_keys=False) == {'y': 2, 'x': 1}
    >>> assert dict_key_translate(d, m, False) == {'y': 2, 'x': 1}
    '''
    if keep_all_keys:
        mkeys = [old for (old,new) in mapping]  # translated keys
        mapping = list(mapping) + [(old,old) for old in dct.keys() if old not in mkeys]
    return dict((new, dct[old]) for (old,new) in mapping)



def test_d_funcs():
 try:
    d = dict(a=1,b=2,c=3)
    assert subdict(d, ('a', 'c')) == {'a': 1, 'c': 3} == d_from_keys(d, ['a', 'c'])
    m = (('a','x'), ('b','y'))

    assert dict_key_translate(d, m) == {'y': 2, 'x': 1, 'c': 3}
    assert dict_key_translate(d, m, keep_all_keys=False) == {'y': 2, 'x': 1}
    assert dict_key_translate(d, m, False) == {'y': 2, 'x': 1}
 finally: globals().update(locals())

test_d_funcs()


def dict_transform(dct, func):
    '''
    Apply func to each dict value.
    '''
    new_dct = {}
    for key in dct:
        new_dct[key] = func(dct[key])
    return new_dct


def ordered_items(dct, keys):
    '''Return dct.items ordered by keys.
    keys = ['action', 'ok', 'client_url', 'client']
    d2 = {'action': 'UPLOAD', 'client_url': '111.22.220.222', 'client': 'xyz', 'ok': 'OK'}
    >>> ordered_items(d2, keys)
    [('action', 'UPLOAD'), ('ok', 'OK'), ('client_url', '111.22.220.222'), ('client', 'dsi')]
    '''
    d2 = subdict(dct, keys)
    f = lambda (key, _): dict(zip(keys, range(len(keys))))[key]
    return sorted(d2.items(), key=f)





