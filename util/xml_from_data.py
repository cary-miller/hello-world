


# ############################################################ #
# ###################### xml from data ####################### #
# ############################################################ #



def dict2xml(d):
    return '\n'.join( '<%s>%s</%s>' %(key,value,key)
        for (key,value) in d.items() )

ud = dict(Title='foo', Comments='yoohoo')
ud = dict(Title='foo bar etc', Comments='WOW yoohoo')

ud2 = dict(
    file=dict(ext='txt', category='green', _='foof'),
    Title='boo',
    Barf='marf',
    bile=dict(ext='pdf', category='blue'),
    # problem:  cannot duplicate keys.
    # but must be able to to give multiple tags.
    # So might(will) have to require different input than dict of dict
    # to generate dup tags like <file>
    # Something more naturally structured like xml.
    # [key, [(k1,v1), ..., (kn,vn), value]]
    # [key, [(k1,v1), ..., (kn,vn)]]
    # with value optional and able to appear anywhere.  or
    # [(key, value), [(k1,v1), ..., (kn,vn)]]
    # [(key), [(k1,v1), ..., (kn,vn)]]
    # or if we're going to always have the key first not need for
    # separate attribute list.
)

def attr_tag(key, d):
    value = d.pop('_', '')
    res = [ '<%s ' %key ]
    res.extend([ pair2attr(akey,avalue) for akey,avalue in d.items()])
    res.append( '>%s</%s>'  %(value,key) )
    return ' '.join(res)


def tag(key):
    return '<%s/>' %key

def pair2tag(key, value):
    return '<%s>%s</%s>' %(key,value,key)

def pair2attr(key, value):
    return '%s="%s"' %(key,value)

def dict2xml_plus(d):
    for key, value in d.items():
        if type(value) != dict:
            print pair2tag(key, value)
        else:
            print attr_tag(key, value)



def lst2partway(lst):
    '''Create xml tags from a list
    [("key", "value"), ("k1","v1"), ("kn","vn")]  
    [(key, value), (k1,v1), ..., (kn,vn)]  
        <key k1="v1" ...  kn="vn">value</key>
    [(key), (k1,v1), ..., (kn,vn)] 
        <key k1="v1" ...  kn="vn" />
    [(key, value)] 
        <key>value</key>
    [(key)] 
        <key/>
    '''
    kv,attrs = head_tail(lst)
    al = [pair2attr(key, value) for (key,value) in attrs]
    if type(kv) == tuple:
        k,v = head_tail(kv)
        v=v[0]
    else:
        k,v = kv, ''
    return [k] + al + [v]






def strlist2tag(s_list):
    '''input:  ['tag', 'a1="v1", 'val']
    '''
    key, tail = head_tail(s_list)
    attrs, value = tail_head(tail)
    s_att = ' '.join(attrs)
    if value:
        print 'v:', value
        assert type(value) == tuple
        assert len(value) == 1
        value = value[0]
        return '<%(key)s %(s_att)s>%(value)s</%(key)s>' %locals()
    return '<%(key)s %(s_att)s />' %locals()


def lst2tag(lst):
    '''input: [("key", "value"), ("k1","v1"), ("kn","vn")]  
    '''
    kv, attrs = head_tail(lst)
    k,v = head_tail(kv)
    print 'x:',  k,v
    if type(v) in (list, tuple) and len(v)>0:
        print 'urg', v
        v = lst2tag(v[0])
    globals().update(locals())
    lst = [(k,v)] + attrs
    return strlist2tag(lst2partway(lst))






def data2xml(lst_data):
    '''
    tag1 = [('name', 'Cary')]
    tag2 = [('job', 'programador'), ('shift', 'day')]
    doc1 = [tag1, tag2]
    tag3 = [('worker', doc1)]
    tag4 = [('next', 'now')]
    tag5 = [('now', 'then')]
    doc2 = [tag1, tag5, tag3]
    doc3 = [tag3]
    '''
    result = []
    for sublist in lst_data:
        result.append( lst2tag(sublist) )
    return '\n'.join( result )



def test_dict2xml_plus():
    d = dict(foo=2, bar=3, lar=dict(x=4, y=22))
    print dict2xml_plus(d)



def test_something():
    update_dict = dict(
        FileExtension='.foobar',
        Filetype='.barfoo'
        )
    print dict2xml(update_dict)



# ########################## AST ########################## #
import tokenize
import inspect
def parrot(f): return inspect.getsource(f)
from cStringIO import StringIO
# http://stackoverflow.com/questions/3069695/can-i-use-python-ast-module-for-this
# Maybe use tokenize instead.??
import re




def tag(name, content=None, attributes=None):
    '''
    >>> attributes = [['bum', 'nub'], ['rum', 'blum']]

    >>> tag('foo', 'bark')
    '<foo>bark</foo>'

    >>> tag('foo', ['bark'])
    '<foo>bark</foo>'

    >>> tag('foo', ['bark', 'nark'])
    '<foo>bark</foo><foo>nark</foo>'

    >>> tag('foo', 'bark', attributes)
    '<foo bum="nub" rum="blum">bark</foo>'

    >>> tag('foo')
    '<foo/>'

    >>> tag('foo', attributes=attributes)
    '<foo bum="nub" rum="blum"/>'
    '''
    att = ''
    if attributes:
        att = ' ' + ' '.join('%s="%s"' %(name,val) for [name,val] in
attributes)
    if content is None:
        return '<%(name)s%(att)s/>' %locals()
    if type(content) is list:
        return '\n'.join([tag(name, sub, attributes) for sub in
content])
    return '<%(name)s%(att)s>%(content)s</%(name)s>' %locals()


def concat(*lst): return '\n'.join(lst)



