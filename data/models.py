from flask_sqlalchemy import SQLAlchemy
from abc import ABCMeta

db = SQLAlchemy()


class User(db.Model):
    """
    Using Concrete Table Inheritance Mapping.
    """
    __metaclass__ = ABCMeta
    __abstract__ = True
    __id = db.Column(db.Integer, primary_key=True)
    __name = db.Column(db.String(64))
    __phone_number = db.Column(db.String(9))
    __status = db.Column(db.Boolean)

    def __init__(self, id, name, phone_number, status):
        self.__id = id
        self.__name = name
        self.__status = status
        self.__phone_number = phone_number

    @property
    def id(self):
        """
        :return: id
        """
        return self.__id

    @id.setter
    def id(self, id):
        """
        Sets an attribute
        :param value: id
        :return: void
        """
        self.__id = id

    @property
    def name(self):
        """
        This method returns the name of the client as a string.
        :return: name
        """
        return self.__name

    @name.setter
    def name(self, string):
        """
        This method sets the name of the client.
        :param string: name
        :return:void
        """
        self.__name = string

    @property
    def phone_number(self):
        return self.__phone_number_id

    @phone_number.setter
    def phone_number(self, number):
        self.__phone_number = number

    @property
    def status(self):
        """
        :return: status
        """
        return self.__status

    @status.setter
    def status(self, boolean):
        """
        :param boolean:
        :return: status
        """
        self.__status = boolean


class Client(User):
    __tablename__ = 'clients'
    __identification = db.Column(db.String(11))
    __notifiable = db.Column(db.Boolean)
    __address_id = db.Column(db.Integer, db.ForeignKey('address.id'))

    __mapper_args__ = {
        'concrete': True
    }

    def __init__(self, name, phone_number, identification, address, notifiable=True, status=True, id=0):
        super().__init__(id, name, phone_number, status)
        self.__identification = identification
        self.__notifiable = notifiable
        self.__address_id = address

    @property
    def identification(self):
        """
        :return: identification
        """
        return self.__identification

    @property
    def notifiable(self):
        return self.__notifiable

    @notifiable.setter
    def notifiable(self, boolean):
        self.__notifiable = boolean

    @property
    def address_id(self):
        return self.__address_id

    @address_id.setter
    def address_id(self, address):
        self.__address_id = address

    def __eq__(self, other):
        return self.__identification == other.identification

    def __repr__(self):
        return '<Cliente %r %r %r %r>' % (self.__name, self.__identification, self.__phone_number, self.__status)


class Clerk(User):
    __tablename__ = 'clerks'
    __email = db.Column(db.String(64), unique=True)
    __password = db.Column(db.String(32))

    __mapper_args__ = {
        'concrete': True
    }

    def __init__(self, name, phone_number, email, password, status=True, id=0):
        super().__init__(id, name, phone_number, status)
        self.__email = email
        self.__password = password

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, string):
        self.__name = string

    @property
    def email(self):
        """
        This method returns the email of the clerk as a string.
        :return: email
        """
        return self.__email

    @email.setter
    def email(self, string):
        """
        This method sets the email of the clerk.
        :param string: email
        :return: void
        """
        self.__email = string

    @property
    def password(self):
        """
        This method returns the password of the clerk as a string.
        :return: password
        """
        return self.__password

    @password.setter
    def password(self, string):
        """
        This method sets the password of the clerk.
        :param string: password
        :return: void
        """
        self.__password = string

    def __repr__(self):
        return '<Atendente %r %r %r>' % (self.__name, self.__email, self.__status)


class Address(db.Model):
    __tablename__ = 'Addresses'
    __id = db.Column(db.Integer, primary_key=True)
    __street = db.Column(db.String(64))
    __number = db.Column(db.SmallInteger)
    __zip_code = db.Column(db.String(6))

    def __init__(self, street, number, zip_code, id=0):
        self.__id = id
        self.__street = street
        self.__number = number
        self.__zip_code = zip_code

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def street(self):
        return self.street

    @street.setter
    def street(self, string):
        self.__street = string

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, number):
        self.__number = number

    @property
    def zip_code(self):
        return self.__zip_code

    @zip_code.setter
    def zip_code(self, string):
        self.__zip_code = string

    def __str__(self):
        return "Rua: {}, {}".format(self.__place, self.__number)


class Demand(db.model):
    __tablename__ = 'order'
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
    def client_id(self):
        return self.__client_id

    @property
    def clerk_id(self):
        return self.__clerk_id

    @property
    def items(self):
        return self.__items

    @items.setter
    def items(self, items):
        self.__items = items


class Item(db.model):
    __tablename__ = 'items'
    __product_id = db.Column(db.Integer, db.ForeignKey('product_id'))
    __quantity = db.Column(db.SmallInteger)
    __demand_id = db.Column(db.Integer, db.ForeignKey('demand_id'))

    def __init__(self, product_id, quantity, demand_id=0):
        self.__demand_id = demand_id
        self.__product_id = product_id
        self.__quantity = quantity

    @property
    def demand_id(self):
        return self.__id_demand

    @property
    def product_id(self):
        return self.__product_id

    @property
    def quantity(self):
        return self.__quantity

    @demand_id.setter
    def demand_id(self, id):
        self.__demand_id = id

    @product_id.setter
    def product_id(self, id):
        self.__product_id = id

    @quantity.setter
    def quantity(self, value):
        self.__quantity = value


class Product(db.Model):
    __tablename__ = 'product'
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
        return '<Product %r %r %r %r>' % (self.__title, self.__name, self.__price, self.__is_available)
