from bokeh.plotting import figure, output_file, show
from bokeh.io import push_notebook, output_notebook
from bokeh.models import HoverTool
import pandas as pd
from collections import namedtuple
from datetime import datetime
from get_data import dataf
import numpy as np


exec(open('get_data.py').read())


def plottable_data(dataf):
    '''Setting up plottable data.   This seems quite ugly,  I'm sure there is
    a better way.
    # fifths
    '''
    h15 = dataf['h5.1'] / dataf['height']
    h25 = dataf['h5.2'] / dataf['height']
    h35 = dataf['h5.3'] / dataf['height']
    h45 = dataf['h5.4'] / dataf['height']
    return pd.DataFrame(dict(h15=h15, h25=h25, h35=h35, h45=h45))
    # plot lines.  One for each id.  Each line should be 2-4-6-8
    # anything that deviates is an error.   Use hover to get the id.


def fun(h5): pass
def fun(df):
#    df = h5.transpose()
    (nrows, ncols) = df.shape
    xs = [list(range(1,5))] * ncols
    ys = [df[name].values for name in df]
    ys = [row for row in df.iterrows()]
    globals().update(locals())
    
    # do without transpose so we can use the id for hover.

    p = figure(width=500, height=300, tools=[hover])
    p.multi_line(xs, ys,
            line_color="green", line_width=3,
#            legend=legend,
            alpha=0.3,
            )
#    output_notebook()
#    show(p)


def funx(h5):
    print(nrows, ncols)
    print(datetime.now())
    print([name for name in df])
#            ys=[df[name].values for name in df],
    print('x', len(xs))
    for x in xs: assert (len(x)) == 4
    print('y', len(ys))
    for y in ys: assert (len(y)) == 4
    print('finitor')


# this is one of the things we are here for.
hover = HoverTool(
        tooltips = [
#            ('id', '@id'),
#            ('1/4', '@h41'),
#            ('', '@h41'),
            ('', '@id'),
#            ('(x,y)', '($x, $y)'),
#            ('length', '$length'),
            ]
        )


#factors = list(dataf.index.values)
#h5 = plottable_data(dataf)
#fun(h5)


stuff = [("h5.1", .2), ("h5.2", .4), ("h5.3", .6), ("h5.4", .8)]
stuff = [("h4.1", .25), ("h2", .5), ("h4.2", .75)]
stuff = [("h3.1", .333), ("h3.2", .667)]
vstuff = [("v3.1", .333), ("v3.2", .667)]


def make_checker(dim):
    '''
    hcheck = make_checker("height")
    vcheck = make_checker("length")
    '''
    def check(df, col_name, mark, gap=.01):
        df['ratio'] = df[col_name] / df[dim]
        column = df['ratio']
        too_low =  column < mark - gap
        too_high = column > mark + gap
        result = df[too_low | too_high]['ratio']
        del dataf['ratio']
        return result
    return check


hcheck = make_checker("height")
vcheck = make_checker("length")
#print(dataf.head()['v2'])


#for pair in stuff:    print(pair, hcheck(dataf, *pair))

#for pair in vstuff:    print(pair, vcheck(dataf, *pair))
#dataf.head()['v3.2']


pair = ("v3.1", .33)
vcheck(dataf, *pair)
dataf.head()

(names, target_values) = '''
v2 v4.1 v4.2 v3.1 v3.2 v5.1 v5.2 v5.3 v5.4 h2 h4.1 h4.2 h3.1 h3.2 h5.1 h5.2 h5.3 h5.4
0.5 0.25 0.75 0.333 0.667 0.2 0.4 0.6 0.8 0.5 0.25 0.75 0.333 0.667 0.2 0.4 0.6 0.8
'''.split('\n')[1:-1]
names = names.split()
target_values = [float(val) for val in target_values.split()]
mapp = zip(names, target_values)
mapp = list(zip(names, target_values))


gap = 0.01

def check_row(row):
    bad = []
    (index, row_series) = row
#    print(index)
    for (col_name, target_value) in mapp:
        if col_name.startswith('v'):
            denom = row_series['length']
        else:
            denom = row_series['height']
        actual_value = row_series[col_name] / denom
        if np.isnan(actual_value):  # ok
            continue
#        if target_value == actual_value: flag = 'ok'
        if abs(target_value - actual_value) < gap:
            flag = 'ok'
        else:
            flag =  actual_value
        if flag != 'ok':
            bad.append((col_name, target_value, flag))
#            print(col_name, target_value, flag)
    if bad:
        return (index, bad)


good = []
bbad = []
for row in dataf.iterrows():
    bad = check_row(row)
    if bad:
        bbad.append(bad)
    else:
        good.append(row)


for row in good:
    (index, row_series) = row

good_indices = [row[0] for row in good]
good_series = [row[1] for row in good]
vs = [rs['v2'] for rs in good_series]
hs = [rs['h2'] for rs in good_series]
assert all(vs) == all(hs) == True


q = '4.1 4.2'.split()
t = '3.1 3.2'.split()
f = '5.1 5.4'.split()
tupify = lambda char, lst: tuple(char + thing for thing in lst)


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
        for key in dct[vh]:
            (a, b) = dct[vh][key]
            dslice = rs[a:b]
            dah = not any([np.isnan(thing) for thing in dslice])
            d[vh][key] = dah
    res[gi] = d



