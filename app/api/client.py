from flask import jsonify, request, url_for
from app.api import api
from app.models import Client, db
from flask_inputs import Inputs
from wtforms.validators import DataRequired, Length, Regexp

class ClientInputs(Inputs):
    #Dont change this name!  Keep it as json!
    json = {
        'name': [DataRequired(), Regexp(
        '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$',0,
        'O nome deve conter somente letras.')],
        'identification': [DataRequired(message="Cliente precisa ter um identificação (RG)."),
                           Length(min=9, max=9,message="Identificação do cliente precisa ter exatamente 9 caracteres.")],
        'phone_number':[DataRequired(message="Cliente precisa ter um número de telefone."), 
                        Length(min=11, max=11,message="O número precisa ter exatamente 9 caracteres.")],
        'address':[DataRequired(message="O cliente precisa ter um endereço."),
                   Length(min=10, max=56,message="O número precisa ter no mínino 10 caracteres e no máximo 56.")],                     
        'notifiable':[DataRequired()]
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
    inputs = ClientInputs(request)
    if inputs.validate():
        client = Client.from_json(request.json)
        db.session.add(client)
        db.session.commit()
        return jsonify(client.to_json()), 201, {'Location': url_for('api.get_client', id=client.id, _external=True)}
    reponse = jsonify(inputs.errors)
    reponse.status_code = 400
    return reponse

@api.route('/client/<int:id>', methods=['PUT'])
def edit_client(id):
    inputs = ClientInputs(request)
    if inputs.validate():
        client = Client.query.get_or_404(id)
        client.name = request.json.get('name')
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