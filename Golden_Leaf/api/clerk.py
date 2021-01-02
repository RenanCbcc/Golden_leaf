from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth

from Golden_Leaf.api import api
from Golden_Leaf.models import Clerk

auth = HTTPBasicAuth()


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


@api.route('token', methods=['GET'])
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token(3600)
    return jsonify({'token': token, 'duration': 3600})


@api.route('clerk', methods=['POST'])
@auth.login_required
def get_clerk():
    return jsonify(g.current_user.to_json())
