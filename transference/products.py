from manager import db


class Product(db.Model):
    __tablename__ = 'products'
    __id = db.Column(db.Integer, primary_key=True)
    __title = db.Column(db.String(64))
    __name = db.Column(db.String(64))
    __price = db.Column(db.SmallInteger)
    __is_available = db.Column(db.Boolean)
    __code = db.Column(db.String(64))

    def __init__(self, title, name, price, code, is_available=True, id=0):
        self.__id = id
        self.__title = title
        self.__name = name
        self.__price = price
        self.__is_available = is_available
        self.__code = code

    @property
    def id(self):
        """
        :return: id
        """
        return self.__id

    @id.setter
    def id(self, value):
        """
        Sets an attribute
        :param value: id
        :return: void
        """
        self.__id = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, string):
        self.__title = string

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, string):
        self.__name = string

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, price):
        self.__price = price

    @property
    def is_available(self):
        return self.__is_available

    @is_available.setter
    def is_available(self, value):
        self.__is_available = value

    @property
    def code(self):
        return self.__code

    def __eq__(self, other):
        return self.__code == other.__code

    def __repr__(self):
        return '<Role %r>' % self.__name
