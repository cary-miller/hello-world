


# ############################################################ #
# ###################### xml from data ####################### #
# ############################################################ #


def head_tail(seq):
    return seq[0], seq[1:]

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



tag_gen = ''' 
def %(name)s(*a):
    """
    >>> %(name)s(content, *attributes):
    attributes must be pairs, eg ['type', 'submit']
    """
    try:
        return tag("%(name)s", *head_tail(a))
    except IndexError: # no content
        return tag("%(name)s")
'''


for name in '''html head body title script style h1 p
    foo bar bat
    table tr td th
    form select option input button
    div pre hr
    '''.split():

    exec(tag_gen %locals())





op_tag = lambda name, val: tag('option', val, [('value', val),
('name', name)])
op_tag_list = lambda name, val_list: '\n'.join([
    op_tag(name, v) for v in val_list])

checkbox = lambda name, val: tag('input', val,  attributes=[ 
    ('type', "checkbox"), ('class', name), ('value', val)])

checkbox_list = lambda name, val_list: '\n'.join([
    checkbox(name, v) for v in val_list])    

radio = lambda name, val: tag('input', val,  attributes=[ 
    ('type', "radio"), ('name', name), ('value', val)])

radio_list = lambda name, val_list: '\n'.join([
    radio(name, v) for v in val_list])    


with open('data_structures.js') as fh: dscode = fh.read()
with open('basic.js') as fh: jscode = fh.read()
with open('basic.css') as fh: csscode = fh.read()

head = head( concat(
    title('proto'),
    script(' ', 
        ["type","text/javascript"],
        ["src","http://code.jquery.com/jquery-2.0.2.js"]),
    script(dscode,  ["type","text/javascript"]),
    script(jscode,  ["type","text/javascript"]),
    style(csscode,  ["type","text/css"]),
    
))



users = 'smith jones'.split()
casenames = 'case1 case2 case3 case4 case5'.split() 
user_options = op_tag_list('user', users)
case_options = op_tag_list('case', casenames)


columns = 'ticket date docid xxxid'.split()
column_checks = checkbox_list('col_check', columns) # for column subsetting.
column_radio = radio_list('col_radio', columns) # for filtering on column values
column_radio = radio('col_radio', 'any') # for filtering on column values






table1 = table(concat(
    tr(concat(
        td('Case'),
        td(select(case_options, ["id","da_case"])),
        td(''),
        )) ,
    tr(concat(
        td('User'),
        td(select(user_options, ["id","da_user"])),
        td(''),
        )) ,
#    tr(concat(
#        td('Columns'),
#        td(select(column_options, [["id","da_cols"]])),
#        td(''),
#        )) ,
    tr(concat(
        td(''),
        td(input('', ["type","submit"], ["value","Go!"],
["id","submit"])),
        td(''),
        )) ,
        ))


sort_controls = concat(p('Sort/Filter Controls'),
    table(concat(


    tr(concat(
        td('Chop head:'),
        td(),
        td(input('', ['type', 'text'], ['id', 'n_chop'])),
        td(input('', ["type","submit"], ["value","Chop!"],
            ["id","chop_submit"])),
        )),

    tr(concat(
        td('Filter on:'),
        td(div(column_radio , ["id","xfilter"])),
        td(input('', ['type', 'text'], ['id', 'filter_val'])),
        td(input('', ["type","submit"], ["value","Filter!"],
            ["id","filter_submit"])),
        )),


    tr(concat(
        td('Go back'),
        td(input('', ["type","submit"], ["value","Previous Result"],
            ["id","prev_result"])),
        td(input('', ["type","submit"], ["value","Back to xxxx Selection"],
            ["id","to_control1"])),

        )),

        )) # table
        ) # sort_controls



body = body( concat(
    h1('xxxx document report'),
    p('Info for docs that have been xxxxx for the yyyyyy.'),
    form( table1, ["id","da_form"], ["method","post"] ),
    hr(),
    div( sort_controls,  ["id","div_sort"], ["class","hidden"] ),
    hr(),
    div(concat(
        pre( 'output area', ['class', 'output1']),
        pre( 'secondary output area', ['class', 'output2'])
    ))
    ,

))

header =  "Content-type: text/html\n\n"
html_doc = header + html(head+body)
with open('basic.html', 'w') as fh: fh.write(html_doc)
#print html_doc



