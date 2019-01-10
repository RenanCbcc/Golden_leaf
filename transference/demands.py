from abc import ABCMeta
from manager import db


class Demand(db.model):

    __tablename__ = 'orders'
    __id = db.Column(db.Integer, primary_key=True)
    __date = db.Column(db.DateTime)
    __client_id = db.Column(db.Integer, db.ForeignKey('client_id'))
    __clerk_id = db.Column(db.Integer, db.ForeignKey('clerk_id'))

    def __init__(self, date, client_id, clerk_id, items, id=0):
        self.__id = id
        self.__date = date
        self.__client_id = client_id
        self.__clerk_id = clerk_id
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
    def id_client(self):
        return self.__client_id

    @property
    def id_clerk(self):
        return self.__clerk_id

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, items):
        self.__items = items


class Item(db.model):
    __tablename__ = 'items'
    __quantity = db.Column(db.SmallInteger)
    __product_id = db.Column(db.Integer, db.ForeignKey('product_id'))
    __demand_id = db.Column(db.Integer, db.ForeignKey('demand_id'))

    def __init__(self, product_id, quantity, demand_id=0):
        self.__demand_id = demand_id
        self.__product_id = product_id
        self.__quantity = quantity

    @property
    def id_demand(self):
        return self.__id_demand

    @property
    def id_product(self):
        return self.__product_id

    @property
    def quantity(self):
        return self.__quantity

    @id_demand.setter
    def id_demand(self, id):
        self.__demand_id = id

    @id_product.setter
    def id_product(self, id):
        self.__product_id = id

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value
