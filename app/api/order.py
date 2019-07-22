from flask import request, jsonify

from app import db
from app.api import api
from app.models.tables import Item, Order


@api.route('/order', defaults={'id': None})
@api.route('/order/<int:id>', methods=['GET'])
def get_order():
    if id is not None:
        order = Order.query.get_or_404(id)
        return jsonify(order.to_json())
    else:
        products = Order.query.all()
        response = jsonify({'products': [product.to_json() for product in products]})
        response.status_code = 200
        return response


@api.route('/order', methods=['POST'])
def save_order():
    order = Order(client_id=2, clerk_id=1)
    db.session.add(order)
    db.session.flush()  # Get the id before committing the object
    item = [Item(product_id=2, order=order, extended_cost=12.0, quantity=2),
            Item(product_id=2, order=order, extended_cost=15.0, quantity=3)]

    # product = Product.from_json(request.json)
    db.session.add_all(item)
    db.session.commit()
    return request.json, 201, {'Location': "www.goldenleaf.com"}
