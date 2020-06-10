from flask import jsonify, request, url_for
from app.api import api
from app.models import Client, db
from flask_inputs import Inputs
from wtforms.validators import DataRequired, Length, Regexp,ValidationError

def validate_client_id(form, field):
    if not Client.query.filter_by(id=field.data).first():
        raise ValidationError(f'Cliente com id {field.data} é inválido.')


class EditClientInputs(Inputs):
    #Dont change this name!  Keep it as json!
    json = {
        'id':[DataRequired(message="Cliente precisa ter um id."),validate_client_id],
        'phone_number':[DataRequired(message="Cliente precisa ter um número de telefone."), 
                        Length(min=11, max=11,message="O número de telefone precisa ter exatamente 11 caracteres.")],
        'address':[DataRequired(message="O cliente precisa ter um endereço."),
                   Length(min=10, max=56,message="O número precisa ter no mínino 10 caracteres e no máximo 56.")],                     
        'notifiable':[DataRequired(message="Cliente quer ou não receber notificações?")],
        'status':[DataRequired(message="Cliente precisa ter um status.")]
    }

class NewClientInputs(Inputs):
    #Dont change this name!  Keep it as json!
    json = {
        'name': [DataRequired(message="Cliente precisa ter um nome."), Regexp('^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$',0,
        'O nome deve conter somente letras.')],
        'phone_number':[DataRequired(message="Cliente precisa ter um número de telefone."), 
                        Length(min=11, max=11,message="O número de telefone precisa ter exatamente 11 caracteres.")],
        'address':[DataRequired(message="O cliente precisa ter um endereço."),
                   Length(min=10, max=56,message="O número precisa ter no mínino 10 caracteres e no máximo 56.")],                     
        'notifiable':[DataRequired(message="Cliente quer ou não receber notificações?")]
    }

@api.route('/client', methods=['GET'], defaults={'id': None})
@api.route('/client/<int:id>', methods=['GET'])
def get_client(id):
    if id is not None:
        client = Client.query.get_or_404(id)
        return jsonify(client.to_json())
    else:
        clients = Client.query.all()
        response = jsonify([client.to_json() for client in clients])
        response.status_code = 200
        return response


@api.route('/client', methods=['POST'])
def new_client():
    inputs = NewClientInputs(request)
    if inputs.validate():
        client = Client.from_json(request.json)
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_json()), 201, {'Location': url_for('api.get_client', id=client.id, _external=True)}
    reponse = jsonify(inputs.errors)
    reponse.status_code = 400
    return reponse

@api.route('/client', methods=['PUT'])
def edit_client():
    inputs = EditClientInputs(request)
    if inputs.validate():
        client = Client.query.get(request.json.get('id'))
        client.address = request.json.get('address')
        client.phone_number = request.json.get('phone_number')
        client.notifiable = request.json.get('notifiable')
        client.status = request.json.get('status')
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_json()), 200, {'Location': url_for('api.get_client', id=client.id, _external=True)}
    reponse = jsonify(inputs.errors)
    reponse.status_code = 400
    return reponse