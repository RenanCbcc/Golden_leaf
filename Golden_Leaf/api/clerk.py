from flask import jsonify, request, g
from flask_httpauth import HTTPBasicAuth
from flask_inputs import Inputs
from wtforms.validators import DataRequired, Length, Regexp,ValidationError
from Golden_Leaf.api import api
from Golden_Leaf.models import Clerk, db
from Golden_Leaf.utils import save_picture, save_picture_from
auth = HTTPBasicAuth()


def validate_clerk_id(form, field):
    if not Clerk.query.filter_by(id=field.data).first():
        raise ValidationError(f'Atendente com id {field.data} é inválido.')


class EditClerkInputs(Inputs):
    #Dont change this name!  Keep it as json!
    json = {
        'id':[DataRequired(message="Atendente precisa ter um id."),validate_clerk_id],
        'phone_number':[DataRequired(message="Atendente precisa ter um número de telefone celular."),
                                                      Regexp('[1-9]{2}[1-9]{4,5}[0-9]{4}',0,'O número deve deve estar no formato: (xx)xxxxx-xxxx.'),
                                                      Length(min=11, max=11,message="O número precisa ter exatamente 11 caracteres.")],
        
    }



@auth.verify_password
def verify_password(email_or_token, password):
    # first try to authenticate by token
    clerk = Clerk.verify_auth_token(email_or_token)
    if not clerk:
        # try to authenticate with username/password
        clerk = Clerk.query.filter_by(email=email_or_token).first()
        if not clerk or not clerk.verify_password(password):
            return False
    g.current_user = clerk
    return True


@api.route('/clerk', methods=['PUT'])
@auth.login_required
def edit_clerk():
    form = EditClerkInputs(request)
    if form.validate(): 
        clerk = Clerk.query.get(request.json.get('id'))
        clerk.phone_number = request.json.get('phone_number')
        
        if request.json.get('image_file'):
            picture_file = save_picture_from(request.json.get('image_file'))            
            clerk.image_file = picture_file
        db.session.add(clerk)
        db.session.commit()
        response = jsonify({"Ok": "Tudo certo!" })
        response.status_code = 200
        return response
    reponse = jsonify(inputs.errors)
    reponse.status_code = 400
    return reponse


@api.route('/clerk', methods=['POST'])
@auth.login_required
def get_clerk():
    return jsonify(g.current_user.to_json())
