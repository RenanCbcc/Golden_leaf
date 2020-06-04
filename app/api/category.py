from flask import jsonify, request, url_for, abort
from app.api import api
from app.models import Category,db
from flask_inputs import Inputs
from wtforms.validators import DataRequired,Regexp,ValidationError

def validate_category_title(form, field):
    if Category.query.filter_by(title=field.data).first():
        raise ValidationError(f'Categoria com título {field.data} já existe.')


def validate_category_id(form, field):
    if not Category.query.filter_by(id=field.data).first():
        raise ValidationError(f'Categoria {field.data} é inválida.')

class NewCategoryInputs(Inputs):
    #Dont change this name!  Keep it as json!
    json = {        
        'title': [DataRequired(), Regexp('^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s\/\-\.]*)$',
        0,
        'O nome da categoria deve conter somente letras'),validate_category_title]
    }


class EditCategoryInputs(Inputs):
    #Dont change this name!  Keep it as json!
    json = {
        'id':[DataRequired(message="Categoria precisa ter um id."),validate_category_id],
        'title': [DataRequired(), Regexp('^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s\/\-\.]*)$',
        0,
        'O nome da categoria deve conter somente letras'),validate_category_title]
    }

@api.route('/category', methods=['GET'], defaults={'id': None})
@api.route('/category/<int:id>', methods=['GET'])
def get_category(id):
    if id is not None:
        category = Category.query.get_or_404(id)
        return jsonify(category.to_json())
    categories = Category.query.all()
    response = jsonify([category.to_json() for category in categories])
    response.status_code = 200    
    return response


@api.route('/category', methods=['POST'])
def create_category():
    inputs = NewCategoryInputs(request)
    if inputs.validate():
        category = Category.from_json(request.json)
        db.session.add(category)
        db.session.commit()
        return jsonify(category.to_json()), 201,{'Location': url_for('api.get_category', id=category.id, _external=True)}
    reponse = jsonify(inputs.errors)
    reponse.status_code = 400
    return reponse

@api.route('/category', methods=['PUT'])
def edit_category():
    inputs = EditCategoryInputs(request)
    if inputs.validate():
        category = Category.query.get(id)    
        category.title = request.json.get('title')
        db.session.add(category)
        db.session.commit()
        return jsonify(category.to_json()), 200, {'Location': url_for('api.get_category', id=category.id, _external=True)}
    reponse = jsonify(inputs.errors)
    reponse.status_code = 400
    return reponse


