


# constants #
q = '4.1 4.2'.split()
t = '3.1 3.2'.split()
f = '5.1 5.4'.split()
tupify = lambda char, lst: tuple(char + thing for thing in lst)


# constants #
dct = dict(
    vertical = dict(
        quarter = tupify('v', q),
        third = tupify('v', t),
        fifth = tupify('v', f),
        )
    ,
    horizontal = dict(
        quarter = tupify('h', q),
        third = tupify('h', t),
        fifth = tupify('h', f),
    )
)


res = {}
gi, rs = good[0]
for thing in good:
    gi, rs = thing
#    print(gi)
    d = dict()
    for vh in dct:
        d[vh] = dict()
        d[vh] = list()
        for key in dct[vh]:
            (a, b) = dct[vh][key]
            dslice = rs[a:b]
            dah = not any([np.isnan(thing) for thing in dslice])
            if dah:
                d[vh].append(key)
    res[gi] = d



