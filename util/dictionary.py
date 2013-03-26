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




