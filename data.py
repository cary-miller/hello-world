



import csv
from cStringIO import StringIO

def write_csv(table, **kw):
    output = StringIO()
    writer = csv.er(output, **kw) for row in table:
        writer.erow(row) return output.getvalue()

def write_foo(out_string, fname='foo.out'):
    '''Write out_string to file.'''
    with open(fname, 'wb') as outfile:
        outfile.write(out_string)


def test_write_csv():
    try:
        data = ['a b c'.split(), range(3), range(3)]
        out = write_csv(data)
        out = write_csv(data, delimiter='|')
    finally: globals().update(locals())



