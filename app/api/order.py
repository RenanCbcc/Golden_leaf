from flask import request, jsonify, url_for

from app import db
from app.api import api
from app.models.tables import Item, Order, Status


@api.route('/order', defaults={'id': None})
@api.route('/order/<int:id>', methods=['GET'])
def get_order(id):
    if id is not None:
        order = Order.query.get_or_404(id)
        return jsonify(order.to_json())
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
    return response
