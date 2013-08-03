# ############################################### #
# ################### Logging ################### #
# ############################################### #

'''
Syslog
Smaller numbers indicate more dire events.
0 == da worst.
4-7 == user level events  ???
'''

log_cutoff = 4 # WARNING
log_cutoff = 6 # INFO
log_cutoff = 7 # DEBUG

log_mode = 'silent'
log_mode = 'prod'
log_mode = 'dev'

def log_dev(msg): print msg
def log_prod(msg): print 'prod:', msg
def log_silent(msg): pass

log_func = dict([
    ('prod', log_prod),
    ('dev', log_dev),
    ('silent', log_silent),
    ])


def log(log_level=0, msg='', log_mode=log_mode):
    '''
    log_level (int):  Severity level of this
    message.
    log_cutoff (global int):  Log messages
    with this level or lower.
    log_mode (str):  'prod' or 'dev'
    log_mode (global str):
    Provides default but is
    overridable.
    '''
    if log_level <= log_cutoff:
        log_func[log_mode]( msg )


