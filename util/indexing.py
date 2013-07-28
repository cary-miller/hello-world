
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




def dups(lst):
    ''' 
    >>> dups(list('abcdeabcab'))
    ['a', 'b', 'c']
    '''
    return [item for item in set(lst) if lst.count(item) > 1]





def head_tail(lst):
    return (lst[0], lst[1:])
    # just like lisp would do #
    # except it applies to strings and any sequence

def tail_head(lst):
    return (lst[:-1], lst[-1])





def find_gaps(seq):
    ''' 
    Show gaps in seq by returning pairs surrounding missing
elements.
    >>> find_gaps([1,2,3,5,6,7,22,23])
    [(3, 5), (7, 22)]
    '''
    gap = []
    for i in range(1, len(seq)):
        if seq[i] != seq[i-1]+1:
            gap.append((seq[i-1], seq[i]))
    return gap 


