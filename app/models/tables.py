import decimal
from abc import ABCMeta
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.routing import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
import enum

"""
A proper class for use with the ORM must do four things:
• Contain __tablename__ , which is the table name to be used in the database.
• Contain one or more attributes that are Columns objects.
• Ensure one or more attributes make up a primary key.
"""


@login_manager.user_loader
def load_user(id):
    return Clerk.query.get(id)


class Status(enum.Enum):
    PAGO = "Pago"
    PENDENTE = "Pendente"


class User(db.Model):
    """
    Using Concrete Table Inheritance Mapping.
    """
    __metaclass__ = ABCMeta
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    phone_number = db.Column(db.String(9), nullable=False)
    # TODO Does this field make sense to clerk?
    status = db.Column(db.Boolean)

    def __init__(self, name, phone_number, status):
        self.name = name
        self.status = status
        self.phone_number = phone_number


class Client(User):
    __tablename__ = 'clients'
    __mapper_args__ = {'concrete': True}
    identification = db.Column(db.String(11), unique=True)
    notifiable = db.Column(db.Boolean)
    address_id = db.Column(db.Integer, ForeignKey('addresses.id'))
    address = db.relationship("Address", back_populates="dweller", lazy=False)
    orders = relationship("Order", back_populates="client")

    def __init__(self, name, phone_number, identification, address, notifiable, status=True):
        super().__init__(name, phone_number, status)
        self.identification = identification
        self.notifiable = notifiable
        self.address = address

    def __eq__(self, other):
        return self.identification == other.identification

    def __repr__(self):
        return '<Cliente %r %r %r %r>' % (self.name, self.identification, self.phone_number, self.status)


class Clerk(User, UserMixin):
    __tablename__ = 'clerks'
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    orders = relationship("Order", back_populates="clerk")

    __mapper_args__ = {
        'concrete': True
    }

    def __init__(self, name, phone_number, email, password, status=True):
        super().__init__(name, phone_number, status)
        self.email = email
        self.password = password

    def get_token(self, expires_sec=1800):
        """
        The token is an encrypted version of a dictionary that has the id of the user
        :param expires_sec:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'clerk_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            clerk_id = s.loads(token)['clerk_id']
        except:
            return None
        return Clerk.query.get(clerk_id)

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


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.now)
    status = db.Column(db.Enum(Status), default=Status.PENDENTE)

    client_id = db.Column(db.Integer, ForeignKey('clients.id'))
    client = relationship("Client", back_populates="orders")

    clerk_id = db.Column(db.Integer, ForeignKey('clerks.id'))
    clerk = relationship("Clerk", back_populates="orders")

    def __init__(self, date, client, clerk, items):
        self.date = date
        self.client = client
        self.clerk = clerk
        self.items = items

    def __repr__(self):
        return '<Pedido %r %r %r >' % (self.date, self.client.name, self.clerk.name)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(64), nullable=False)
    detail = db.Column(db.String(64))
    zip_code = db.Column(db.String(6), nullable=False)
    dweller = relationship("Client", uselist=False, back_populates="address")

    def __init__(self, street, detail, zip_code):
        self.street = street
        self.detail = detail
        self.zip_code = zip_code

    def __str__(self):
        return "Rua: {}, {}".format(self.street, self.detail)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True, nullable=False)
    name = db.Column(db.String(32), nullable=False)
    price = db.Column(db.Numeric(6, 2), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False)
    code = db.Column(db.String(13), unique=True, nullable=False)

    __table_args__ = (CheckConstraint(price >= 0.00, name='unit_cost_positive'),)

    def __init__(self, title, name, price, code, is_available=True):
        self.title = title
        self.name = name
        self.price = price
        self.is_available = is_available
        self.code = code

    def to_json(self):
        json_product = {
            'id': self.id,
            'title': self.title,
            'name': self.name,
            'price': str(self.price),
            'is_available': self.is_available,
            'code': self.code
        }
        return json_product

    @staticmethod
    def from_json(json_product):

        title = json_product.get('title')
        name = json_product.get('name')
        price = decimal.Decimal(json_product.get('price'))
        code = json_product.get('code')

        if name is None or name == '':
            raise ValidationError('Produto tem com nome inválido')
        if code is None or len(code) is not 11:
            raise ValidationError('Código de produto inválido')
        if price is None or price <= 0:
            raise ValidationError('Produto co preço inválido')

        return Product(title, name, price, code)

    def __eq__(self, other):
        return self.code == other.code

    def __repr__(self):
        return '<Product %r %r %r %r>' % (self.title, self.name, self.price, self.is_available)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, ForeignKey('product.id'))
    order_id = db.Column(db.Integer, ForeignKey('orders.id'))
    quantity = db.Column(db.Numeric(5, 2))

    order = db.relationship("Order", backref=backref('items', order_by=order_id))
    product = db.relationship("Product", uselist=False)

    def __init__(self, product_id, demand_id, quantity):
        self.demand_id = demand_id
        self.product_id = product_id
        self.quantity = quantity

    def __repr__(self):
        return '<Item %r %r Quantidade %r>' % (self.product.title, self.product.name, self.quantity)
