from bokeh.plotting import figure, output_file, show
from bokeh.io import push_notebook, output_notebook
from bokeh.models import HoverTool
import pandas as pd
from collections import namedtuple
from datetime import datetime
from get_data import dataf


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


