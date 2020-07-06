from __future__ import annotations
import decimal
import enum
import jwt
from abc import ABCMeta
from datetime import datetime
from flask_login import UserMixin, current_user
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.routing import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import login_manager, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app, url_for, abort
from flask_admin.contrib.sqla import ModelView
from typing import Union


@login_manager.user_loader
def load_user(id):
    return Clerk.query.get(id)


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


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
    phone_number = db.Column(db.String(13), nullable=False)

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number


class Client(User):
    __tablename__ = 'clients'
    __mapper_args__ = {'concrete': True}
    identification = db.Column(db.String(9), unique=True)
    notifiable = db.Column(db.Boolean)
    address = db.Column(db.String(64))
    status = db.Column(db.Boolean)

    def __init__(self, name, phone_number, identification, address, notifiable, status=True):
        super().__init__(name, phone_number)
        self.identification = identification
        self.notifiable = notifiable
        self.address = address
        self.status = status

    def to_json(self):
        json_client = {
            'id': self.id,
            'name': self.name,
            'phone_number': self.phone_number,
            'identification': self.identification,
            'address': self.address,
            'notifiable': self.notifiable,
            'status': self.status
        }
        return json_client

    @staticmethod
    def from_json(json_client):
        import uuid
        identification = uuid.uuid4().time_low

        name = json_client.get('name')
        phone_number = json_client.get('phone_number')
        address = json_client['address']
        notifiable = json_client.get('notifiable')
        client = Client(name, phone_number, str(
            identification)[0:9], address, notifiable)
        return client


def __eq__(self, other):
    return self.identification == other.identification


def __repr__(self):
    return '<Cliente %r %r %r %r>' % (self.name, self.identification, self.phone_number, self.status)


class Clerk(User, UserMixin):
    __tablename__ = 'clerks'
    image_file = db.Column(db.String(24), default='default.png')
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    __mapper_args__ = {
        'concrete': True
    }

    def __init__(self, name: str, phone_number: str, email: str, password: str):
        super().__init__(name, phone_number)
        self.email: str = email
        self.password: str = password

    def get_token(self, expires_sec=600) -> str:
        """
        The token is an encrypted version of a dictionary that has the id of the user
        :param expires_sec:
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'clerk_id': self.id}).decode('utf-8')

    def generate_auth_token(self, expiration=600) -> str:
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'clerk_id': self.id}).decode('ascii')

    @staticmethod
    def verify_auth_token(token: str) -> Union[Clerk, None]:
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        clerk = Clerk.query.get(data['clerk_id'])
        return clerk

    @property
    def password(self) -> None:
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def to_json(self) -> str:
        json_clerk = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone_number': self.phone_number
        }
        return json_clerk

    def __repr__(self) -> str:
        return '<Atendente %r %r>' % (self.name, self.email)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))
    image_file = db.Column(db.String(32), default='default.jpg')
    unit_cost = db.Column(db.Numeric(6, 2), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False)
    code = db.Column(db.String(13), unique=True, nullable=False)
    category_id = db.Column(db.Integer, ForeignKey(
        'categories.id'), nullable=False)

    category = relationship("Category", backref=backref(
        'products', order_by=description))

    __table_args__ = (CheckConstraint(
        unit_cost >= 0.00, name='unit_cost_positive'),)

    def __init__(self, category_id, description: str, unit_cost, code: str, is_available=True):
        # This field is 'virtual'.  It was declared in Category model as a backref
        self.category_id = category_id
        self.description = description
        self.unit_cost = unit_cost
        self.is_available = is_available
        self.code = code

    def to_json(self) -> str:
        json_product = {
            'id': self.id,
            'category_id': self.category_id,
            'description': self.description,
            'unit_cost': str(self.unit_cost),
            'is_available': self.is_available,
            'code': self.code
        }
        return json_product

    @staticmethod
    def from_json(json_product) -> Product:
        category_id = json_product.get('category_id')
        description = json_product.get('description')
        unit_cost = decimal.Decimal(json_product.get('unit_cost'))
        code = json_product.get('code')
        return Product(category_id, description, unit_cost, code)

    def __eq__(self, other) -> bool:
        return self.code == other.code

    def __repr__(self) -> str:
        return '<Product %r %r %r>' % (self.description, self.unit_cost, self.is_available)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True, nullable=False)

    def __init__(self, title: str):
        self.title = title

    def to_json(self) -> str:
        json_product = {
            'id': self.id,
            'title': self.title
        }
        return json_product

    @staticmethod
    def from_json(json_category) -> Category:
        title = json_category.get('title')
        return Category(title)

    def __repr__(self) -> str:
        return '<Category %r>' % self.title


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey('clients.id'), nullable=False)
    clerk_id = db.Column(db.Integer, ForeignKey('clerks.id'), nullable=False)
    payment_id = db.Column(db.Integer, ForeignKey(
        'payments.id'), nullable=True)
    date = db.Column(db.DateTime, index=True, default=datetime.now)
    total = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.Enum(Status), default=Status.PENDENTE)

    client = relationship("Client", backref=backref('orders', order_by=id))
    clerk = relationship("Clerk", backref=backref('orders', order_by=id))

    payment = relationship("Payment", backref=backref(
        'orders', order_by=id), lazy=True)

    def __init__(self, client_id, clerk_id):
        self.client_id = client_id
        self.clerk_id = clerk_id
        self.status = Status.PENDENTE
        self.payment = None
        self.total: float = 0

    def to_json(self) -> str:
        return {
            'id': self.id,
            'client': self.client.name,
            'clerk': self.clerk.name,
            'total': str(self.total),
            'date': self.date.strftime("%d/%m/%Y %H:%M:%S"),
            'status': self.status.name
        }

    @staticmethod
    def from_json(content) -> Order:
        secret = current_app.config['SECRET_KEY']
        data = jwt.decode(content.get('token'), secret)
        client_id = data['client_id']
        clerk_id = data['clerk_id']
        return Order(client_id, clerk_id)

    def __repr__(self):
        return '<Pedido %r %r %r >' % (self.ordered, self.client.name, self.clerk.name)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey(
        'products.id'), nullable=False)
    quantity = db.Column(db.Numeric(5, 2), nullable=False)
    extended_cost = db.Column(db.Numeric(7, 2), nullable=False)

    order = relationship("Order", backref=backref(
        'items', order_by=id), lazy=True)
    product = relationship("Product", uselist=False)

    __table_args__ = (CheckConstraint(
        quantity >= 0.01, name='quantity_positive'),)

    def __init__(self, product_id, order, quantity, extended_cost):
        self.product_id = product_id
        self.order = order
        self.quantity = quantity
        self.extended_cost = extended_cost

    def to_json(self) -> str:
        return {
            'description': self.product.description,
            'unit_cost': str(self.product.unit_cost),
            'quantity': str(self.quantity),
            'extended_cost': str(self.extended_cost)
        }

    def __repr__(self) -> str:
        return '<Item: %r Quantidade %r>' % (self.product.description, self.quantity)


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey('clients.id'), nullable=False)
    clerk_id = db.Column(db.Integer, ForeignKey('clerks.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), default=0)
    date = db.Column(db.DateTime, index=True, default=datetime.now)

    client = relationship("Client", uselist=False)
    clerk = relationship("Clerk", uselist=False)

    def __init__(self, client: int, clerk: int, amount: decimal):
        self.client_id = client
        self.clerk_id = clerk
        self.amount = amount

    @staticmethod
    def from_json(content) -> Payment:
        secret = current_app.config['SECRET_KEY']
        data = jwt.decode(content.get('payment'), secret)
        client_id = data['client_id']        
        clerk_id = data['clerk_id']
        amount = data['amount']
        return Payment(client_id, clerk_id, decimal.Decimal(amount))

    def to_json(self) -> str:
        return {
            'client': self.client.name,
            'clerk': self.clerk.name,
            'amount': str(self.amount),
            'date': self.date.strftime("%d/%m/%Y %H:%M:%S")
        }
