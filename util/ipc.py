import commands




def bash(cmd):
    '''
    Run a bash command and return the result as a string or raise an
    exception.
    cmd = """
        cat /var/log/kernel.log |
        sed 's/MA.*Book//'  |
        grep wifi |
        sed 's/ /,/3' |
        sed 's/: /,/' |
        grep -i airport
    """
    csv_string = bash(cmd)
    from indexing import fetch_cols
    new_csv = fetch_cols(csv_string, [2,0])
    '''
    return_code, result = commands.getstatusoutput(cmd.replace('\n', ''))
    if return_code == 0:
        return result
    raise Exception(return_code)




