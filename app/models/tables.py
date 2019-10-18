import decimal
from abc import ABCMeta
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.routing import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from flask import current_app, url_for, abort
import enum


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
    phone_number = db.Column(db.String(13), nullable=False)

    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number


class Client(User):
    __tablename__ = 'clients'
    __mapper_args__ = {'concrete': True}
    identification = db.Column(db.String(11), unique=True)
    notifiable = db.Column(db.Boolean)
    address_id = db.Column(db.Integer, ForeignKey('addresses.id'))
    address = db.relationship("Address", back_populates="dweller", lazy=False)
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
            'address': url_for('api.get_client_address', id=self.id),
            'notifiable': self.notifiable,
            'status': self.status
        }
        return json_client

    @staticmethod
    def from_json(content):
        if content['name'] == "" or content['phone_number'] == "" or content['identification'] == "":
            abort(400, "Cliente não pode ter valores nulos")
        client = Client(content.get('name'), content.get('phone_number'), content.get('identification'),
                        Address.from_json(content['address']), content.get('notifiable'))
        return client


def __eq__(self, other):
    return self.identification == other.identification


def __repr__(self):
    return '<Cliente %r %r %r %r>' % (self.name, self.identification, self.phone_number, self.status)


class Clerk(User, UserMixin):
    __tablename__ = 'clerks'
    image_file = db.Column(db.String(24), default='default.jpg')
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)

    __mapper_args__ = {
        'concrete': True
    }

    def __init__(self, name, phone_number, email, password):
        super().__init__(name, phone_number)
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

    def generate_auth_token(self, expiration=2400):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        clerk = Clerk.query.get(data['id'])
        return clerk

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        json_clerk = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'phone_number': self.phone_number
        }
        return json_clerk

    def __repr__(self):
        return '<Atendente %r %r>' % (self.name, self.email)


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(64), nullable=False)
    zip_code = db.Column(db.String(6), nullable=False)
    dweller = relationship("Client", uselist=False, back_populates="address")

    def __init__(self, street, zip_code):
        self.street = street
        self.zip_code = zip_code

    def to_json(self):
        json_address = {
            'id': self.id,
            'street': self.street,
            'zip_code': self.zip_code,

        }
        return json_address

    @staticmethod
    def from_json(content):
        if content['street'] == "" or content['zip_code'] == "":
            raise ValidationError("Endereço não pode ter valores nulos")
        address = Address(content.get('street'), content.get('zip_code'))
        return address

    def __str__(self):
        return "Rua: {}, {}".format(self.street, self.zip_code)


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32), nullable=False)
    description = db.Column(db.String(64))
    image_file = db.Column(db.String(32), default='default.jpg')
    unit_cost = db.Column(db.Numeric(6, 2), nullable=False)
    is_available = db.Column(db.Boolean, nullable=False)
    code = db.Column(db.String(13), unique=True, nullable=False)
    category_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=False)

    category = relationship("Category", backref=backref('products', order_by=description))

    __table_args__ = (CheckConstraint(unit_cost >= 0.00, name='unit_cost_positive'),)

    def __init__(self, category, brand, description, unit_cost, code, is_available=True):
        self.category = category  # This field is 'virtual' and was declared in Category as a backref
        self.brand = brand
        self.description = description
        self.unit_cost = unit_cost
        self.is_available = is_available
        self.code = code

    def to_json(self):
        json_product = {
            'id': self.id,
            'brand': self.brand,
            'description': self.description,
            'unit_cost': str(self.unit_cost),
            'is_available': self.is_available,
            'code': self.code
        }
        return json_product

    @staticmethod
    def from_json(json_product):

        brand = json_product.get('brand')
        description = json_product.get('name')
        unit_cost = decimal.Decimal(json_product.get('unit_cost'))
        code = json_product.get('code')

        if brand is None or brand == '':
            raise ValidationError('Produto tem com marca inválida')
        if description is None or description == '':
            raise ValidationError('Produto tem com descriçao inválida')
        if code is None or len(code) is not 13:
            raise ValidationError('Código de produto inválido')
        if unit_cost is None or unit_cost <= 0:
            raise ValidationError('Produto co preço inválido')

        return Product(brand, description, unit_cost, code)

    def __eq__(self, other):
        return self.code == other.code

    def __repr__(self):
        return '<Product %r %r %r %r>' % (self.brand, self.description, self.unit_cost, self.is_available)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), index=True, nullable=False)

    def __init__(self, title):
        self.title = title

    def to_json(self):
        json_product = {
            'id': self.id,
            'title': self.title
        }
        return json_product

    @staticmethod
    def from_json(json_product):
        title = json_product.get('title')

        if title is None or title == '':
            raise ValidationError('Categoria tem com título inválido')

        return Category(title)

    def __repr__(self):
        return '<Category %r>' % self.title


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey('clients.id'), nullable=False)
    clerk_id = db.Column(db.Integer, ForeignKey('clerks.id'), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.now)
    cost = db.Column(db.Numeric(10, 2), default=0)
    status = db.Column(db.Enum(Status), default=Status.PENDENTE)

    client = relationship("Client", backref=backref('orders', order_by=id))
    clerk = relationship("Clerk", backref=backref('orders', order_by=id))

    def to_json(self):
        json_product = {
            'id': self.id,
            'client_id': self.client_id,
            'clerk_id': self.clerk_id,
            'cost': self.cost,
            'date': self.date,
            'status': self.status,
            'items': self.items
        }
        return json_product

    @staticmethod
    def from_json(content):
        client = Client.query.get(content.get('client_id'))
        clerk = Clerk.query.get(content.get('clerk_id'))
        return Order(client=client, clerk=clerk, status=Status[content.get('status')])

    def __repr__(self):
        return '<Pedido %r %r %r >' % (self.date, self.client.name, self.clerk.name)


class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Numeric(5, 2), nullable=False)
    extended_cost = db.Column(db.Numeric(7, 2), nullable=False)

    order = relationship("Order", backref=backref('items', order_by=id), lazy=True)
    product = relationship("Product", uselist=False)

    __table_args__ = (CheckConstraint(quantity >= 0.01, name='quantity_positive'),)

    def __init__(self, product_id, order, quantity, extended_cost):
        self.product_id = product_id
        self.order = order
        self.quantity = quantity
        self.extended_cost = extended_cost

    def to_json(self):
        json_item = {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'extended_cost': self.extended_cost
        }
        return json_item

    @staticmethod
    def from_json(items_json, order):
        order.cost = 0
        for item in items_json:
            product_id = item['product_id']
            product = Product.query.filter_by(id=product_id).one_or_none()
            if product is None:
                raise ValidationError('Item com produto inválida')
            quantity = item['quantity']
            if quantity is None or quantity == '':
                raise ValidationError('Item com quantidade inválida')
            extended_cost = product.unit_cost * decimal.Decimal(quantity)
            order.cost += extended_cost
            order.items.append(Item(product_id, order, quantity, extended_cost))

    def __repr__(self):
        return '<Item: %r Quantidade %r>' % (self.product.description, self.quantity)


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, ForeignKey('clients.id'), nullable=False)
    clerk_id = db.Column(db.Integer, ForeignKey('clerks.id'), nullable=False)
    date = db.Column(db.DateTime, index=True, default=datetime.now)
    total = db.Column(db.Numeric(10, 2), default=0)
    client = relationship("Client", uselist=False)
    clerk = relationship("Clerk", uselist=False)
