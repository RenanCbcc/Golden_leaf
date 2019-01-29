from abc import ABCMeta
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager, db

"""
A proper class for use with the ORM must do four things:
• Contain __tablename__ , which is the table name to be used in the database.
• Contain one or more attributes that are Columns objects.
• Ensure one or more attributes make up a primary key.
"""


@login_manager.user_loader
def load_user(id):
    return Clerk.query.get(int(id))


class User(db.Model):
    """
    Using Concrete Table Inheritance Mapping.
    """
    __metaclass__ = ABCMeta
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    phone_number = db.Column(db.String(9))
    status = db.Column(db.Boolean)

    def __init__(self, name, phone_number, status):
        self.name = name
        self.status = status
        self.phone_number = phone_number


class Client(User):
    __tablename__ = 'client'
    __mapper_args__ = {'concrete': True}
    identification = db.Column(db.String(11))
    notifiable = db.Column(db.Boolean)
    address_id = db.Column(db.Integer, ForeignKey('addresses.id'))
    address = db.relationship("Address", back_populates="dweller", lazy=False)

    def __init__(self, name, phone_number, identification, address, notifiable, status=True):
        super().__init__(name, phone_number, status)
        self.identification = identification
        self.notifiable = notifiable
        self.address = address

    def __eq__(self, other):
        return self.identification == other.identification

    def __repr__(self):
        return '<Cliente %r %r %r %r>' % (self.name, self.identification, self.phone_number, self.status)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(64))
    detail = db.Column(db.String(64))
    zip_code = db.Column(db.String(6))
    dweller = relationship("Client", uselist=False, back_populates="address")

    def __init__(self, street, detail, zip_code):
        self.street = street
        self.detail = detail
        self.zip_code = zip_code

    def __str__(self):
        return "Rua: {}, {}".format(self.street, self.detail)


class Clerk(User, UserMixin):
    __tablename__ = 'clerks'
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))

    __mapper_args__ = {
        'concrete': True
    }

    def __init__(self, name, phone_number, email, password, status=True):
        super().__init__(name, phone_number, status)
        self.email = email
        self.password = password

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Atendente %r %r %r>' % (self.name, self.email, self.status)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True)
    name = db.Column(db.String(32))
    price = db.Column(db.Numeric(6, 2), nullable=False)
    is_available = db.Column(db.Boolean)
    code = db.Column(db.String(13), nullable=False)

    __table_args__ = (CheckConstraint(price >= 0.00, name='unit_cost_positive'),)

    def __init__(self, title, name, price, code, is_available=True):
        self.title = title
        self.name = name
        self.price = price
        self.is_available = is_available
        self.code = code

    def __eq__(self, other):
        return self.code == other.code

    def __repr__(self):
        return '<Product %r %r %r %r>' % (self.title, self.name, self.price, self.is_available)


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    client_id = db.Column(db.Integer, ForeignKey('client.id'))
    clerk_id = db.Column(db.Integer, ForeignKey('clerks.id'))

    client = db.relationship("Client", backref=backref('orders', order_by=client_id))
    clerk = db.relationship("Clerk", backref=backref('orders', order_by=clerk_id))

    def __init__(self, date, client_id, clerk_id, items):
        self.date = date
        self.client_id = client_id
        self.clerk_id = clerk_id
        self.items = items

    def __repr__(self):
        return '<Pedido %r >' % self.date


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('product.id'))
    order_id = db.Column(db.Integer, ForeignKey('orders.id'))
    quantity = db.Column(db.Integer)

    order = db.relationship("Order", backref=backref('items', order_by=order_id))
    product = db.relationship("Product", uselist=False)

    def __init__(self, product_id, demand_id, quantity):
        self.demand_id = demand_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return '<Item %r >' % self.quantity
