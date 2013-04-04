#!/usr/bin/env python

import os, sys, shutil


def copydir(src_base,sd, dst_base,dd, recursive=True, destructive=False,
    ignore=None):
    '''
    # ignore is a function of two args (shutil.ignore_patterns)
    #  1.  the directory being copied
    #  2.  the list of files in the directory
    # Returns:
    #   sequence of directory and subset of (2)

    Walk the src_base+sd tree, copying its contents to dst_base+dd.

    src_base, dst_base both are directory names.
    sd, dd are directory names within the respective bases.

    Copy src_tree -> dst_tree  recursively and non-destructively.  
    Anything present in dst but not src, leave it alone.
    If present in src , copy to dst (overwriting if already present).
    Thus:  walk the src tree (no need to walk the dst tree)
    The only differential behavior is for subdirs.
    If subdir exists in dst then go into it recursively.
    If subdir not in dst, copy it recursively.
    '''
    src = os.path.join(src_base, sd)
    dst = os.path.join(dst_base, dd)

    if not os.path.exists(dst): # copy the whole tree
        shutil.copytree(src,dst, ignore=ignore)
    else: # go through one file at a time so as to not erase files in dst but not src.
        for fname in set(os.listdir(src)).difference(ignore(src, os.listdir(src))):
            fullname = os.path.join(src, fname)
            newname =  os.path.join(dst, fname)
            if os.path.isfile(fullname):
                shutil.copyfile(fullname, newname)
            elif os.path.isdir(fullname):
                copydir(src,fname, dst,fname )


def test():
    '''Testing copydir function.
    '''
    dst_base = '/Users/marymiller/scratch/'
    src_base = '/Users/marymiller/tg2env/exa/exa/'
    common = 'templates'
    sd = common
    dd = common
    #copydir(src_base,sd, dst_base,dd)

    #copydir(*sys.argv[1:5])

    ignore = shutil.ignore_patterns('*.pyc', '*~', '*.swp', '*.swo')
    
    src_base = '/Users/marymiller/tg2env/exa/'
    copydir(src_base, 'exa/public/css', dst_base, 'css', ignore=ignore)
    copydir(src_base, 'exa/public/', dst_base, 'exa/public', ignore=ignore)


def re_os_path_walk():
    # os.path.walk:  for each dir in arg[0], function cb is called with
    # arguments as shown; first arg being an arbitrary arg, second the dir
    # name, third the list of file names in that dir.


    def cb(arg, directory, files):
        for file in files:
            print os.path.join(directory, file), repr(arg)

    def dvsf(fun, directory, files):
        for fname in files:
            fullname = os.path.join(directory, fname)
            print fullname, fun(fullname)

    def dirfilter(path):
        d={True:'dcopy', False:'cp'}
        return d[os.path.isdir(path)]

    func = dvsf
    #os.path.walk(pname, func, os.path.isdir)
    #os.path.walk(pname, func, dirfilter)


if __name__=='__main__':
    try:
        pname = sys.argv[1]
    except:
        pname = '/Users/marymiller'
        pname = '/Users/marymiller/stapleton'
        pname = '/Users/marymiller/tgenv/exa/exa/'





