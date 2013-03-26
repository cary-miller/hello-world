'''
xml tagging functions.
'''

def tag(name, **attrs):
    """Return a function that creates tag `name`
    to enclose string `content`.  Note: the returned
    function gets a sensible name.  This helps prevent
    confusion if several such functions are present in
    an interactive session.
    
    >>> td = tag('td')
    >>> print td('hello') + td(44)
    <td>hello</td><td>44</td>

    >>> print tag('html')('Smallish html document')
    <html>Smallish html document</html>
    
    >>> htm = tag('html', foo='goo', noo=22)
    >>> head = tag('head')
    >>> body = tag('body', bgcolor='hotpink')
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




def tags_from_lists(nested_list):
    '''
    Borrow the lisp idea of generating xml from s-expressions.
    Take input data that looks like s-expressions, ie. nested lists, and
    convert to nested tags w/wo attributes.
    sample data:
    === 1 tag ===
    (('tagname', 'content'))
    (('bodytext', 'yoohoo'), ('attr1', 'gosh'), ('attr2', 'blarney'))
    === 2 tag ===
    (('tagname', (('inner_tag1', 'inner1')))
    ... etc
    '''
    return nested_list



