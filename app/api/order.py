from flask import request, jsonify
from app import db
from app.api import api
from app.models import Item,Product, Order, Client,Clerk
from flask_inputs import Inputs
from wtforms.validators import  DataRequired, Length, NumberRange,ValidationError


def is_float(value):
  try:
    float(value)
    return True
  except:
    return False

def valide_client_id(form, field):
    if not Client.query.filter_by(id=field.data).first():
        raise ValidationError(f"Id '{field.data}' do cliente é inválido.")


def valide_clerk_id(form, field):
    if not Clerk.query.filter_by(id=field.data).first():
        raise ValidationError(f"Id '{field.data}' do atendente é inválido.")


class OrderInputs(Inputs):
    #Dont change this name!  Keep it as json!
    json = {
        'clerk_id': [DataRequired(message="Pedido precisa ter um atendente."),valide_clerk_id],
        'client_id': [DataRequired(message="Pedido precisa ter um cliente."),valide_client_id],      
    }

def valide_product_quantity(form, field):
    if is_float(field.data):
        quantity = float(field.data)
        raise ValidationError(f"Quantidade '{field.data}' é inválida.")
    if quantity < 0.05 or unit_cost > 25.0:
            raise ValidationError("Quantidade precisa estar entre 0.05 e 25.0")
    else:
            return
    raise ValidationError(f"Quantidade '{field.data}' para o produto inválida.")


def valide_product_id(form, field):
    if not Product.query.filter_by(id=field.data).first():
        raise ValidationError(f'Produto com {field.data} é inválido.')

class ItemsInputs(Inputs):
    #Dont change this name!  Keep it as json!
    json = {
        'product_id': [DataRequired(message="Pedido precisa ter um produto."),valide_product_id],
        'quantity': [DataRequired(message="Produto precisa ter um quantidade."),valide_product_quantity],      
    }


@api.route('/order', defaults={'id': None})
@api.route('/order/client/<int:id>', methods=['GET'])
def get_order(id):
    if id is not None:
        orders = Order.query.filter_by(client_id=id).order_by(Order.ordered).all()
        response = jsonify({'orders': [order.to_json() for order in orders]})
        response.status_code = 200
    else:
        orders = Order.query.all()
        response = jsonify([order.to_json() for order in orders])
        response.status_code = 200
    return response


@api.route('/order', methods=['POST'])
def save_order():
    inputs = OrderInputs(request)
    if inputs.validate():
        order = Order.from_json(request.json)
        ItemsInputs()
        Item.from_json(request.json.get('items'), order)
        db.session.add(order)
        db.session.flush()  # Get the id before committing the object.
        db.session.commit()
        response = jsonify({'OK': 'The request was completed successfully.', 'order_id': order.id})
        response.status_code = 200
        # send_message(order)
        return response
    reponse = jsonify(inputs.errors)
    reponse.status_code = 400
    return reponse

def send_message(order):
    client = Client.query.get(order.client_id)
    if client.notifiable:
        account_sid = 'AC06b6d740e2dbe8c1c94dd41ffed6c3a3'
        auth_token = '2e22811c3a09a717ecd754b7fb527794'
        from twilio.rest import Client as Twilio_Client
        twilio_client = Twilio_Client(account_sid, auth_token)

        twilio_client.messages.create(body='Olá, ' + client.name + ' .Você realizou uma compra no valor de R$ ' + str(order.total) + ' Volte sempre!',
            from_='+12054311596',
            to='+55' + client.phone_number)
