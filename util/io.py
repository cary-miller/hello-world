import csv
from cStringIO import StringIO
from urllib2 import Request, urlopen



def write_csv(table, **kw):
    '''Return a table (list of lists) as a csv string.
    '''
    output = StringIO()
    writer = csv.writer(output, **kw) 
    for row in table:
        writer.writerow(row) 
    return output.getvalue()



def string2file(out_string, fname='foo.out'):
    '''Write out_string to file.'''
    with open(fname, 'wb') as outfile:
        outfile.write(out_string)



def url2string(url):
    """Return the contents of url as a string."""
    res = StringIO()
    req = Request(url)
    fd = urlopen(req)
    while 1:
        data = fd.read(1024)
        if not data: break
        res.write(data)
    return res.getvalue().decode('utf-8')



if __name__ == '__main__':

    def test_write_csv():
        try:
            data = ['a b c'.split(), range(3), range(3)]
            out = write_csv(data)
            out = write_csv(data, delimiter='|')
        finally: globals().update(locals())


    def test_url2string():
        urlc = 'https://github.com/cary-miller'
        # urlc contains non-ascii unicode which stores fine but causes an
        # exception on printing in the absence of .decode('utf-8').
        urlb = 'http://cary.webfactional.com/wb'
        urlg = 'http://www.google.com'

        print url2string(urlc)
        print url2string(urlb)
        print url2string(urlg)

    test_write_csv()
    test_url2string()
