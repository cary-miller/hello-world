
identity = lambda x:x
def round_deco(round_func=identity, r_param=0):
    def deco(f):
        if round_func == identity:
            return f
        g = lambda p: round(f(p), r_param)
        if round_func == int:
            return lambda p: int(g(p))
        return g
    return deco

r0 = round_deco(round, 0)
r1 = round_deco(round, 1)
r2 = round_deco(round, 2)
r3 = round_deco(round, 3)
rn = round_deco()
ri = round_deco(int)

# I can't remember Farenheit-Celcius conversions so here they
# are.

def fc(f): return (f-32) * (10./18)
def cf(c): return (c*18./10)+32

x = r1(fc)(33)


