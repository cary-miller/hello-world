
def fetch_indices(seq, indices):
    '''
    >>> fetch_indices('abcdef', [3,2,1,1])
    ['d', 'c', 'b', 'b']
    '''
    return [seq[i] for i in indices]


def fetch_indices(seq, indices):
    return type(seq)(seq[i] for i in indices)


def fetch_indices_type_safe(seq, indices):
    '''
    >>> fetch_indices_type_safe('abcdef', [3,2,1,1])
    'dcbb'
    >>> fetch_indices_type_safe(list('abcdef'), [3,2,1,1]) 
    ['d', 'c', 'b', 'b']
    '''
    result = fetch_indices(seq, indices)
    if type(seq) is str:
        return ''.join(result)
    return type(seq)(result)


def fetch_cols(csv_string, indices, ifs=',', ils='\n', ofs=',', ols='\n'): 
    '''
    # ifs: input field separator
    # ils: input line separator
    # ofs: output field separator
    # ols: output line separator

    >>> csv_string="""
    foo,bar,bat,rat
    moo,mar,cat,tat
    soo,sar,sat,sit
    """
    >>> print fetch_cols(csv_string, [2,0])
    bat,foo
    cat,moo
    sat,soo

    >>> csv_string="""
    foo*bar*bat*rat
    moo*mar*cat*tat
    soo*sar*sat*sit
    """
    >>> fetch_cols(csv_string, [2,0], '*', ols='%%%', ofs='+') 
    'bat+foo%%%cat+moo%%%sat+soo'
    '''
    return ols.join(
        ofs.join(fetch_indices(line.split(ifs), indices))
            for line in csv_string.split(ils) if line)


