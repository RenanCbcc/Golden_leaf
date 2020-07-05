import decimal
import jwt
from flask import request, jsonify, current_app
from app import db
from app.api import api
from app.models import Item, Product, Order, Client, Clerk
from flask_inputs import Inputs
from wtforms.validators import DataRequired, ValidationError
from app.api.clerk import auth


def verify_order_token(form, field):
    secret = current_app.config['SECRET_KEY']
    try:
        data = jwt.decode(field.data, secret)
    except jwt.ExpiredSignatureError:
        # valid token, but expired
        raise ValidationError('O token expirou')
    except jwt.InvalidTokenError:
        # invalid token
        raise ValidationError('O token é inválido')

    valide_client_id(data)
    valide_clerk_id(data)

    return True


def valide_client_id(data: dict):    
    if 'client_id' not in data:
        raise ValidationError("O pagamento precisa ter um campo 'client_id'.")
    if not Client.query.filter_by(id=data['client_id']).first():
        raise ValidationError(f"Id '{data['client_id']}' do cliente é inválido.")


def valide_clerk_id(data: dict):
    if 'clerk_id' not in data:
        raise ValidationError("O pagamento precisa ter um campo 'clerk_id'.")
    if not Clerk.query.filter_by(id=data['clerk_id']).first():
        raise ValidationError(f"Id '{data['clerk_id']}' do atendente é inválido.")


class OrderInputs(Inputs):
    # Dont change this name!  Keep it as json!
    json = {
        'token': [DataRequired(message="Pedido precisa ter o token."), verify_order_token],
        'items': [DataRequired(message="Pedido preciter ter ao menus um item.")]
    }


class ItemInput():
    def __init__(self):
        self.error: str = "error"
        self.product: Product = None
        self.quantity: float = 0

    def is_float(self, value: str) -> bool:
        try:
            float(value)
            return True
        except:
            return False

    def validate_quantity(self, value: str) -> bool:
        if self.is_float(value):
            self.quantity = float(value)
            if self.quantity > 0.05 and self.quantity < 25.0:
                return True
            else:
                self.error = "Quantidade precisa estar entre 0.05 e 25.0"
                return False
        else:
            self.error = f"Quantidade '{value}' é inválida."
            return False

    def validate_product(self, product_id) -> bool:
        product = Product.query.filter_by(id=product_id).one_or_none()
        if product is None:
            self.error = f"Produto com id '{product_id}' é inválido."
            return False
        else:
            self.product = product
            return True

    def get_error(self) -> None:
        reponse = jsonify(self.error)
        reponse.status_code = 400
        return reponse


@api.route('/order', defaults={'id': None})
@api.route('/order/client/<int:id>', methods=['GET'])
def get_order(id):
    if id is not None:
        orders = Order.query.filter_by(client_id=id).order_by(Order.date).all()
        response = jsonify([order.to_json() for order in orders])
        response.status_code = 200
    else:
        orders = Order.query.all()
        response = jsonify([order.to_json() for order in orders])
        response.status_code = 200
    return response


@api.route('/order', methods=['POST'])
def save_order():
    orderInputs = OrderInputs(request)
    if orderInputs.validate():
        order = Order.from_json(request.json)
        order = add_items(order)
        # If all items are ok, the save them.
        db.session.add(order)
        db.session.flush()  # Get the id before committing the object.
        db.session.commit()
        response = jsonify(
            {'Sucesso': 'O pedido foi registrado com sucesso.', 'order_id': order.id})
        response.status_code = 200
        send_message(order)
        return response
    reponse = jsonify(orderInputs.errors)
    reponse.status_code = 400
    return reponse


@api.route('/order/<int:id>/items', methods=['GET'])
def items_order(id):
    order = Order.query.filter_by(id=id).one_or_none()
    if order is not None:
        all_items = Item.query.filter_by(order=order).all()
        response = jsonify([item.to_json() for item in all_items])
        response.status_code = 200
        return response
    else:
        response = jsonify({"Erro": "Pedido não encontrado.",
                            "Mensagem": f"O pedido com id: {id} não pode ser encontrado."})
        response.status_code = 404
        return response


def add_items(order: Order) -> Order:
    itemInput = ItemInput()
    for item in request.json.get('items'):
        var = item['product_id']
        if not itemInput.validate_product(item['product_id']):
            return itemInput.get_error()
        if not itemInput.validate_quantity(item['quantity']):
            return itemInput.get_error()
        extended_cost = itemInput.product.unit_cost * \
            decimal.Decimal(itemInput.quantity)
        order.total += extended_cost
        order.items.append(
            Item(itemInput.product.id, order, itemInput.quantity, extended_cost))
    return order


def send_message(order):    
    if order.client.notifiable:
        account_sid = current_app.config['ACOUNT_SID']
        auth_token = current_app.config['AUTH_TOKEN']
        from twilio.rest import Client as Twilio_Client
        twilio_client = Twilio_Client(account_sid, auth_token)

        twilio_client.messages.create(body='Olá, ' + client.name + ' .Você realizou uma compra no valor de R$ ' + str(order.total) + ' Volte sempre!',
                                      from_='+12054311596',
                                      to='+55' + client.phone_number)
