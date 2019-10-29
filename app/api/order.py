from flask import request, jsonify
from app import db
from app.api import api
from app.models import Item, Order, Client


@api.route('/order', defaults={'id': None})
@api.route('/order/client/<int:id>', methods=['GET'])
def get_order(id):
    if id is not None:
        orders = Order.query.filter_by(client_id=id).order_by(Order.ordered).all()
        response = jsonify({'orders': [order.to_json() for order in orders]})
        response.status_code = 200
    else:
        orders = Order.query.all()
        response = jsonify({'orders': [order.to_json() for order in orders]})
        response.status_code = 200
    return response


@api.route('/order', methods=['POST'])
def save_order():
    order = Order.from_json(request.json)
    Item.from_json(request.json.get('items'), order)
    db.session.add(order)
    db.session.flush()  # Get the id before committing the object
    db.session.commit()
    response = jsonify(
        {'OK': 'The request was completed successfully.', 'order_id': order.id})
    response.status_code = 200
    # send_message(order)
    return response


def send_message(order):
    client = Client.query.get(order.client_id)
    if client.notifiable:
        account_sid = 'AC06b6d740e2dbe8c1c94dd41ffed6c3a3'
        auth_token = '2e22811c3a09a717ecd754b7fb527794'
        from twilio.rest import Client as Twilio_Client
        twilio_client = Twilio_Client(account_sid, auth_token)

        twilio_client.messages.create(
            body='Olá, ' + client.name +
                 ' .Você realizou uma compra no valor de R$ ' + str(order.total) + ' Volte sempre!',
            from_='+12054311596',
            to='+55' + client.phone_number
        )
