


class Quantity:

    def __init__(self, name):
        self.name = name

    def __set__(self, instance, value):
        print('set %s on %s' % (self.name, instance))
        instance.__dict__[self.name] = value
        return
        setattr(instance, self.name, value)

    def __get__(self, instance):
        print('get %s from %s' % (self.name, instance))
        return instance.__dict__[self.name]
        return getattr(instance, self.name)


class Order:
    weight = Quantity('weight')
    price = Quantity('price')
    
    def __init__(self, weight, price):
        self.weight = weight
        self.price = price


od = Order(2, 3)


