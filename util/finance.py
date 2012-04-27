def mortgage_payment(principal,interest,years):
    '''
    principal in dollars:  1000000
    interest in human:     8.4
    years as integer:      10
    '''
    months=years*12.0
    if interest == 0:  return principal/months
    rate = interest/1200.0
    payment =  (rate + rate/((1+rate)**months -1)) * principal
    return  int(payment)


