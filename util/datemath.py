import datetime
import time



def add_months(dt, n):
    '''Add n months to datetime (or subclass), dt.
    '''
    t = type(dt)  # This is slick.  It means that the type of dt is the
    # type that is returned,  meaning this works seamlessly with
    # subclasses of datetime.
    new_month = (dt.month-1+n)%12+1
    delta_year = int((dt.month-1+n)/12)
    return t(dt.year+delta_year, new_month, dt.day)



def last_day_of_month(dt):
    new = add_months(dt, 1)
    return type(dt)(new.year, new.month, 1) - datetime.timedelta(1)



def pds_date(dt=None):
    '''
    Go two months back to the last day of the month.
    '''
    dt = dt or datetime.datetime.today()
    if type(dt) == my_dt:
        return dt.add_months(-2).last_day_of_month()
    return last_day_of_month( add_months(dt, -2) )




class my_dt(datetime.datetime):
    def monthdelta(self, n):
        return add_months(self, n)
    def add_months(self, n):
        return add_months(self, n)
    def last_day_of_month(self):
        return last_day_of_month(self)
        

if 0:
    dt = datetime.datetime.today()
    d1 = add_months(dt, -2)   # datetime

    dt = my_dt.today()
    d2 = dt.monthdelta(-2)    # my_dt
    d3 = add_months(dt, -2)   # my_dt 
    d4 = dt.add_months(-2)    # my_dt 

    m1 = d3.add_months(-3).last_day_of_month()
    m2 = last_day_of_month(add_months(d3,-3))
    assert m1 == m2

    d5 = d2 + datetime.timedelta(44)   # datetime



# Does one want a monthdelta object ?
class monthdelta(datetime.datetime): pass
class monthdelta(datetime.timedelta): pass
class monthdelta(object):
    def __init__(self, dt, n):
        '''
        dt: datetime
        n:  integer
        '''
        return


