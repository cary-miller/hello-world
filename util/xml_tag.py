
import xml.etree.cElementTree as etree
import re
import urllib  # for quote/unquote_plus

def readable(s): return s.replace('>', '>\n  ')
def pp_xml(xmldoc): readable(xmldoc)

def decode(s):
    ''' 
    >>> decode('foo%26bar.%2C/bat')
    'foo&bar.,/bat'
    '''
    return urllib.unquote_plus(s)


def encode(s):
    ''' 
    >>> encode('foo&bar.,/bat')
    'foo%26bar.%2C/bat'
    '''
    return urllib.quote(s)



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


def f(*a):
    '''A dorky little function that does some finicky actions on its
inputs.
    The point is to transform arguments to another function.  The
target
    function accepts a string and an arbitrary number of lists as
positional
    args.  This func accepts arbitrary number of strings and
arbitrary
    number of lists; concatenates the strings and returns a list of
      1.  The concatenated strings
      2.  The unaltered lists
    suitable for input as arguments to that other function.

    >>> f('ab', [7], 'cd', 'ef', [8], [9])
    ['abcdef', [7], [8], [9]]

    ''' 
    res = ''
    pos = []
    delim = '\n'
    for arg in a:
        if type(arg) in (str, unicode):
            got_string = True
            res += delim + arg
        elif type(arg) in (list, ):
            pos.append(arg)
        else:
            raise Exception('bad type')
    if got_string:
        return [res] + pos
    return pos
    # a nice variation on this would be to join the strings using
    # some
    # joiner like \n.
    #
    # Extremely rigid, but in this case that is exactly what I want.
    # It
    # does type checking on the args.  If ever args fail to conform
    # to
    # expectations we want to fail noisily.
    #
    # The one way in which it is floppy is it allows mixed ordering
    # of
    # strings & lists.  That could maybe allow abuse, or it might be
    # a good
    # thing.
    #
    # Damn!
    # Maybe want more like:
    '''
    >>> f('p', [7], '<hr/>', '<hr/>', [8], [9])
    ['p', '<hr/><hr/>', [7], [8], [9]]
    or 
    ['p', [7], [8], [9], '<hr/><hr/>']
    '''
    # Need to try it out.


def shiptag(name, content, attributes=None):
    return '<%(name)s>%(content)s</%(name)s>' %locals()






def shiptag(name, **attrs):
    """Return a function that creates shiptag `name`
    to enclose string `content`.  Note: the returned
    function gets a sensible name.  This helps prevent
    confusion if several such functions are present in
    an interactive session.
    
    >>> td = shiptag('td')
    >>> print td('hello') + td(44)
    <td>hello</td><td>44</td>

    >>> print shiptag('html')('Smallish html document')
    <html>Smallish html document</html>
    
    >>> htm = shiptag('html', foo='goo', noo=22)
    >>> head = shiptag('head')
    >>> body = shiptag('body', bgcolor='hotpink')
    >>> print htm('\n'.join( [head('Head'), body('Body')] ))
    <html noo=22 foo="goo">
    <head>Head</head>
    <body bgcolor="hotpink">Body</body></html>

    """
    att_list=[]
    for key in attrs:
        if type(attrs[key]) == type(""):
            v = '"' + attrs[key] + '"'
        else:
            v = str(attrs[key])
        att = "%s=%s" %(key, v)
        att_list.append(att)
    if att_list == []: att_list=''
    else:              att_list = ' '+ ' '.join(att_list)
    def f(content):
        """Input: content is a string.
        If the user passes content other than a string
        it will be silently converted to a string.
        """
        return "<%s%s>%s</%s>" %(name,att_list,content,name)
    f.__name__ = name
    return f





