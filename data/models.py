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


class User(Base):
    """
    Using Concrete Table Inheritance Mapping.
    """
    __metaclass__ = ABCMeta
    __abstract__ = True
    id = Column(Integer(), primary_key=True)
    name = Column(String(64), index=True)
    phone_number = Column(String(9))
    status = Column(Boolean())

    def __init__(self, id, name, phone_number, status):
        self.id = id
        self.name = name
        self.status = status
        self.phone_number = phone_number


class Client(User):
    __tablename__ = 'clients'
    __mapper_args__ = {'concrete': True}
    identification = Column(String(11))
    notifiable = Column(Boolean())
    address_id = Column(Integer(), ForeignKey('addresses.id'))

    address = relationship("Address", uselist=False)

    def __init__(self, name, phone_number, identification, address, notifiable=True, status=True, id=0):
        super().__init__(id, name, phone_number, status)
        self.identification = identification
        self.notifiable = notifiable
        self.address_id = address

    def __eq__(self, other):
        return self.identification == other.identification

    def __repr__(self):
        return '<Cliente %r %r %r %r>' % (self.name, self.identification, self.phone_number, self.status)


class Clerk(User):
    __tablename__ = 'clerks'
    email = Column(String(64), unique=True)
    password = Column(String(32))

    __mapper_args__ = {
        'concrete': True
    }

    def __init__(self, name, phone_number, email, password, status=True, id=0):
        super().__init__(id, name, phone_number, status)
        self.email = email
        self.password = password

    def __repr__(self):
        return '<Atendente %r %r %r>' % (self.name, self.email, self.status)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer(), primary_key=True)
    street = Column(String(64))
    number = Column(SmallInteger())
    zip_code = Column(String(6))

    def __init__(self, street, number, zip_code, id=0):
        self.id = id
        self.street = street
        self.number = number
        self.zip_code = zip_code

    def __str__(self):
        return "Rua: {}, {}".format(self.street, self.number)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer(), primary_key=True)
    title = Column(String(64))
    name = Column(String(64))
    price = Column(Numeric(6, 2), nullable=False)
    is_available = Column(Boolean())
    code = Column(String(64), nullable=False)

    __table_args__ = (CheckConstraint(price >= 0.00, name='unit_cost_positive'),)

    def __init__(self, title, name, price, code, is_available=True, id=0):
        self.id = id
        self.title = title
        self.name = name
        self.price = price
        self.is_available = is_available
        self.code = code

    def __eq__(self, other):
        return self.code == other.code

    def __repr__(self):
        return '<Product %r %r %r %r>' % (self.title, self.name, self.price, self.is_available)


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer(), primary_key=True)
    date = Column(DateTime(), default=datetime.now)
    client_id = Column(Integer(), ForeignKey('clients.id'))
    clerk_id = Column(Integer(), ForeignKey('clerks.id'))

    client = relationship("Client", backref=backref('orders', order_by=client_id))
    clerk = relationship("Clerk", backref=backref('orders', order_by=clerk_id))

    def __init__(self, date, client_id, clerk_id, items, id=0):
        self.id = id
        self.date = date
        self.client_id = client_id
        self.clerk_id = clerk_id
        self.items = items

    def __repr__(self):
        return '<Pedido %r >' % self.date


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer(), primary_key=True)
    product_id = Column(Integer(), ForeignKey('products.id'))
    order_id = Column(Integer(), ForeignKey('orders.id'))
    quantity = Column(SmallInteger())

    order = relationship("Order", backref=backref('items', order_by=order_id))
    product = relationship("Product", uselist=False)

    def __init__(self, product_id, demand_id, quantity):
        self.demand_id = demand_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return '<Item %r >' % self.quantity



