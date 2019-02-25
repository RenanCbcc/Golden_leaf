from flask import request, jsonify, url_for
from app.api import api
from app.models.tables import Product, db


@api.route('/products', methods=['GET'])
def listing_products():
    products = Product.query.all()
    response = jsonify({'products': [product.to_json() for product in products]})
    response.status_code = 200
    return response


@api.route('/products', methods=['POST'])
def create_product():
    product = Product.from_json(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 201, {'Location': url_for('api.get_product', id=product.id, _external=True)}


@api.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_json())


@api.route('/products/<int:id>', methods=['PUT'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    product.title = request.json.get('title')
    product.name = request.json.get('name')
    product.price = request.json.get('price')
    product.code = request.json.get('code')
    product.is_available = request.json.get('is_available')
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 200, {'Location': url_for('api.get_product', id=product.id, _external=True)}
