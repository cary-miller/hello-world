from bokeh.plotting import figure, output_file, show
from bokeh.io import push_notebook, output_notebook
from bokeh.models import Range1d
from bokeh.models import Jitter
from bokeh.models.sources import ColumnDataSource
import bokeh
import sys
import numpy as np
#from get_data import dataf, pd, column_names 
#exec(open('/home/cary/.pythonrc').read())


exec(open('get_data.py').read())


def show_versions():
    print('Python version ' + sys.version)
    print('Pandas version ' + pd.__version__)
    print('Bokeh version ' + bokeh.__version__)
    print('Numpy version ' + np.__version__)


def plottable_data(dataf):
    df = dataf['length height v2 v4.1 v4.2 v3.1 v3.2'.split()]
    df = dataf['v2 v4.2 v5.4 vfr.1 h2 h3.2 h5.4 hfr.1'.split()]

    # perform own jittering.
#    n = len(dataf)
#    divisor = 100
#    v2ratio = dataf['v2'] / dataf['length'] + np.random.random(n)/divisor
#    h2ratio = dataf['h2'] / dataf['height'] + np.random.random(n)/divisor
#    h24 = h2ratio
#    h14 = dataf['h4.1'] / dataf['height'] + np.random.random(n)/divisor
#    h34 = dataf['h4.2'] / dataf['height'] + np.random.random(n)/divisor

    # nevermind the jitter
    v2ratio = dataf['v2'] / dataf['length']
    h2ratio = dataf['h2'] / dataf['height']
    h24 = h2ratio

    # quarters
    h14 = dataf['h4.1'] / dataf['height']
    h34 = dataf['h4.2'] / dataf['height']

    # thirds
    h13 = dataf['h3.1'] / dataf['height']
    h23 = dataf['h3.2'] / dataf['height']

    # fifths
    h15 = dataf['h5.1'] / dataf['height']
    h25 = dataf['h5.2'] / dataf['height']
    h35 = dataf['h5.3'] / dataf['height']
    h45 = dataf['h5.4'] / dataf['height']


    row_names = dataf.index
    factors = list(row_names.values)

    # old
    d2 = pd.DataFrame(dict(v2=v2ratio, h2=h2ratio, h14=h14, h24=h24, h34=h34,
        h41=dataf['h4.1']))
    
    # quarters same as old
    h4 = pd.DataFrame(dict(h14=h14, h24=h24, h34=h34))

    # thirds
    h3 = pd.DataFrame(dict(h13=h13, h23=h23))
    h3 = pd.DataFrame(dict(h13=h13, h23=h23, h41=dataf['h4.1']))

    # fifths
    h5 = pd.DataFrame(dict(h15=h15, h25=h25, h35=h35, h45=h45, h41=dataf['h4.1']))


    ds = ColumnDataSource(d2)
    ds = ColumnDataSource(h3)
    ds = ColumnDataSource(h5)
    return factors, ds
    # Put factors and ds into the global namespace in the ugliest way.


def f(x, color, legend):
    p.circle(x=x, y='id', source=ds, 
            size=15, fill_color=color, line_color="green", line_width=3,
            legend=legend,
            alpha=0.3)
            # plots with warning and errors.
            # NaNs are absent from the plot, naturally.


from bokeh.models import HoverTool
hover = HoverTool(
        tooltips = [
#            ('id', '@id'),
#            ('1/4', '@h41'),
            ('', '@h41'),
#            ('(x,y)', '($x, $y)'),
#            ('length', '$length'),
            ]
        )


factors, ds = plottable_data(dataf)
p = figure(y_range=factors, tools=[hover])


def halves():
    f('h2', 'orange', 'h 1/2')
    f('v2', 'blue', 'v 1/2')
    show(p)


def quarters():
    f('h14', 'blue', 'h 1/4')
    f('h24', 'red', 'h 1/2')
    f('h34', 'green', 'h 3/4')
#   output_file("quarters.html")
    output_notebook()
    show(p)


def thirds():
    f('h13', 'blue', 'h 1/3')
    f('h23', 'red', 'h 2/3')
#   output_file("quarters.html")
    output_notebook()
    show(p)


def fifths():
    f('h15', 'blue', 'h 1/5')
    f('h25', 'red', 'h 2/5')
    f('h35', 'yellow', 'h 3/5')
    f('h45', 'green', 'h 4/5')
#   output_file("quarters.html")
    output_notebook()
    show(p)




# show the results
#show(p)

# https://github.com/bokeh/bokeh/issues/1005
# Bokeh fails to plot when ColumnDataSource contains NaNs.
