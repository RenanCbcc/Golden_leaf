from flask import request, jsonify, url_for
from app.api import api
from app.models.tables import Product, db


@api.route('/product', defaults={'id': None})
@api.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    if id is not None:
        product = Product.query.get_or_404(id)
        return jsonify(product.to_json())
    else:
        products = Product.query.all()
        response = jsonify({'products': [product.to_json() for product in products]})
        response.status_code = 200
        return response


@api.route('/product', methods=['POST'])
def create_product():
    product = Product.from_json(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 201, {'Location': url_for('api.get_product', id=product.id, _external=True)}


@api.route('/product/<int:id>', methods=['PUT'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    product.brand = request.json.get('brand')
    product.description = request.json.get('description')
    product.unit_cost = request.json.get('unit_cost')
    product.code = request.json.get('code')
    product.is_available = request.json.get('is_available')
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 200, {'Location': url_for('api.get_product', id=product.id, _external=True)}
