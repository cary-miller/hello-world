import ast
import inspect
import copy



# AST is strictly for parsing source code.  An existing func or pyc file is
# byte code which is not parseable by ast.
# ... and apparently there is no reliable byte code decompiler, certainly
# not one in the standard lib.

# For accessing inner workings of existing objects ast will not work.
# ... But with inspect we can get the source code and use ast on that.


def f(msg, n):
    '''Original function.
    '''
    x = 33/n


def targ(msg, n):
    '''Goal:  a function like this.
    '''
    try:
        x = 33/n
        print msg
        return 99
    finally:
        evil = locals()
        globals().update(locals())



def globalizeA(fn):
    try:
        f = copy.deepcopy(fn)
    #    return f

        # parse the input func
        src = inspect.getsource(f)
        f_tree = ast.parse(src)

        if 1:
            # new statment(s) to go in finally block
            stmt1 = "evil = locals()"
            stmt2 = "globals().update(locals())"
            stmt_list = [stmt1, stmt2]
            end = [ast.parse(s).body[0] for s in stmt_list]

            # create ast node 
            tf = ast.TryFinally(lineno=1, col_offset=1)
            tf = ast.TryFinally()
            # if lineno or col_offset are omitted => error later
            # NOTE lineno and col_offset are dealt with by fix_missing_locations.

            tf.body = f_tree.body[0].body # original func body
            tf.finalbody =  end 

            fname = f.__name__  + '_glob'
            f_tree.body[0].name = fname
            f_tree.body[0].body = [tf]

        f_tree = ast.fix_missing_locations(f_tree)
        code_ob = compile(f_tree, '<string>', 'exec') # Module
        eval(code_ob,  fn.func_globals)   # bb is back
        return locals()[fname]
    finally:
        globals().update(locals())


def rm():
    '''Cleanup func to remove the stray variables that are now polluting
    the namespace.
    '''
    for name in evil:
        exec('del %s' %name, globals())

def globalize(f):
        fname = f.func_name
        fglob = f.func_globals
        lines = inspect.getsourcelines(f)[0]
        if lines[0].startswith('@globalize'):
            lines = lines[1:]
        t = ' try:\n'
        fin = [' finally:\n', '  evil=locals()\n', '  globals().update(locals())\n']
        res = [lines[0], t] + list(lines[1:]) + fin
        new_src = ''.join(res)
        exec(new_src, fglob)
        return eval(fname, fglob)

# shortcomings of this
#  1. exec AND eval
#  2. indentation
#  3. manual search for 'def '
# AST
#  1. executed in module of the decorator.



def parrot(f):
    return inspect.getsource(f)





def fn(c):
    a, b = 2, 3
    return a+b+c/0
    return a+b+c

globalize(fn)
#p = parrot(fn)


def paradox():
    try:
        raise Exception("Here")
    except:
        return "There"
    finally:
        return "Or maybe there"
    return "Or it that here?"

print paradox()


#@globalize
def fact(n):
    assert n==int(n) and n>=0
    if n==0: return 1
    return n * fact(n-1)



