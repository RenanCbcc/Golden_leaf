class Demand(object):
    def __init__(self, date, time, id_client, id_clerk, items, id=0):
        self.__id = id
        self.__date = date
        self.__time = time
        self.__id_client = id_client
        self.__id_clerk = id_clerk
        self.__items = items

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def date(self):
        return self.__date

    @property
    def time(self):
        return self.__time

    @property
    def id_client(self):
        return self.__id_client

    @property
    def id_clerk(self):
        return self.__id_clerk

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, items):
        self.__items = items


class Item(object):
    def __init__(self, id_product, quantity, id_demand=0):
        self.__id_demand = id_demand
        self.__id_product = id_product
        self.__quantity = quantity

    @property
    def id_demand(self):
        return self.__id_demand

    @property
    def id_product(self):
        return self.__id_product

    @property
    def quantity(self):
        return self.__quantity

    @id_demand.setter
    def id_demand(self, id):
        self.__id_demand = id

    @id_product.setter
    def id_product(self, id):
        self.__id_product = id

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value
