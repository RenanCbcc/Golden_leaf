from flask import request, jsonify, url_for
from app.api import api
from app.api.erros import resource_not_found
from app.models import Product, db
from flask_inputs import Inputs
from wtforms.validators import  DataRequired, Length, NumberRange, Regexp


class ProductInputs(Inputs):
    #Dont change this name!  Keep it as json!
    json = {
        'category_id': [DataRequired(message="Produto precisa estar em uma categoria.")],
        'description': [Length(min=3, max=128,message="Descrição precisa ter entre 3 e 128 caracteres."), 
                        Regexp('^([A-Za-z0-9\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s\.\-]*)$')],
        'brand':[Length(min=3, max=32,message="Marca precisa ter entre 3 e 32 caracteres."),
                 Regexp('^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$')],
        'unit_cost':[DataRequired(message="Produto precisa ter um preço."), 
                     NumberRange(min=0.5, max=100.0,message="Preço do produto precisa estar entre R$ 0.5 e R$ 100.00")],
        'code':[DataRequired(), Length(min=9, max=13, message="Código do produto precisa ter entre 9 e 13 dígitos.")]
    }

@api.route('/product', defaults={'id': None})
@api.route('/product/<int:id>', methods=['GET'])
def get_product(id):
    if id is not None:
        product = Product.query.get_or_404(id)
        return jsonify(product.to_json())
    else:
        products = Product.query.all()
        response = jsonify([product.to_json() for product in products])
        response.status_code = 200
        return response


@api.route('/product/code/<int:code>', methods=['GET'])
def get_product_by_code(code):
    product = Product.query.filter_by(code=code).one_or_none()
    if product is not None:
        response = jsonify({'id': product.id, 'description': product.description, 'unit_cost': str(product.unit_cost),
             'code': product.code})
        response.status_code = 200
        return response
    else:
        response = jsonify({"error": "Not found"})
        response.status_code = 404
        return response


@api.route('/product', methods=['POST'])
def new_product():
    inputs = ProductInputs(request)
    if inputs.validate():
        product = Product.from_json(request.json)
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_json()), 201, {'Location': url_for('api.get_product', id=product.id, _external=True)}
    reponse = jsonify(inputs.errors)
    reponse.status_code = 400
    return reponse

@api.route('/product/<int:id>', methods=['PUT'])
def edit_product(id):
    inputs = ProductInputs(request)
    if inputs.validate():    
        product = Product.query.get_or_404(id)
        product.brand = request.json.get('brand')
        product.description = request.json.get('description')
        product.unit_cost = request.json.get('unit_cost')
        product.code = request.json.get('code')
        product.is_available = request.json.get('is_available')
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_json()), 200, {'Location': url_for('api.get_product', id=product.id, _external=True)}
    reponse = jsonify(inputs.errors)
    reponse.status_code = 400
    return reponse

@api.route('/product/unit_cost/<id>')
def product_cost(id):
    product = Product.query.filter_by(id=id).one()
    if product is not None:
        response = jsonify({'id': product.id, 'unit_cost': str(product.unit_cost)})
        response.status_code = 200
        return response
    else:
        return resource_not_found()


@api.route('/product/category/<id>')
def product(id):
    products = Product.query.filter_by(category_id=id).all()
    response = jsonify({'products': [
        {'id': product.id, 'description': product.description, 'unit_cost': str(product.unit_cost)} for product in
        products]})
    return response
