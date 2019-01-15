from abc import ABCMeta
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy import Column, Numeric, SmallInteger, Integer, Boolean, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import relationship, backref

"""
A proper class for use with the ORM must do four things:
• Inherit from the declarative_base object.
• Contain __tablename__ , which is the table name to be used in the database.
• Contain one or more attributes that are Column objects.
• Ensure one or more attributes make up a primary key.
"""

Base = declarative_base()


class Product(Base):
    __tablename__ = 'products'

    __id = Column(Integer(), primary_key=True)
    __title = Column(String(64))
    __name = Column(String(64))
    __price = Column(Numeric(6, 2), nullable=False)
    __is_available = Column(Boolean())
    __code = Column(String(64), nullable=False)

    __table_args__ = (CheckConstraint(__price >= 0.00, name='unit_cost_positive'),)

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

class Address(Base):
    __tablename__ = 'addresses'
    __id = Column(Integer(), primary_key=True)
    __street = Column(String(64))
    __number = Column(SmallInteger())
    __zip_code = Column(String(6))

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
        return "Rua: {}, {}".format(self.__street, self.__number)


class Item(Base):
    __tablename__ = 'items'

    __id = Column(Integer(), primary_key=True)
    __product_id = Column(Integer(), ForeignKey('product.product_id'))
    __demand_id = Column(Integer(), ForeignKey('demand.demand_id'))
    __quantity = Column(SmallInteger())

    def __init__(self, product_id, demand_id, quantity):
        self.__demand_id = demand_id
        self.__product_id = product_id
        self.__quantity = quantity

    @property
    def demand_id(self):
        return self.product_id

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


class User(Base):
    """
    Using Concrete Table Inheritance Mapping.
    """
    __metaclass__ = ABCMeta
    __abstract__ = True
    __id = Column(Integer(), primary_key=True)
    __name = Column(String(64), index=True)
    __phone_number = Column(String(9))
    __status = Column(Boolean())

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
        return self.__phone_number

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
    __identification = Column(String(11))
    __notifiable = Column(Boolean())
    __address_id = Column(Integer(), ForeignKey('addresses.id'))

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
    __email = Column(String(64), unique=True)
    __password = Column(String(32))

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


class Order(Base):
    __tablename__ = 'orders'
    __id = Column(Integer(), primary_key=True)
    __date = Column(DateTime(), default=datetime.now)
    __client_id = Column(Integer(), ForeignKey('clients.client_id'))
    __clerk_id = Column(Integer(), ForeignKey('clerks.clerk_id'))

    # client = relationship("Client", backref=backref('orders', order_by=__id))
    # clerk = relationship("Clerk", backref=backref('orders', order_by=__id))

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



from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)
