from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth
from app.models import Clerk
from app.api.erros import unauthorized
from app.api import api

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


@auth.error_handler
def auth_error():
    return unauthorized()


@api.route('token')
@auth.login_required
def get_auth_token():
    token = g.current_user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@api.route('clerk')
@auth.login_required
def get_resource():
    return jsonify(g.current_user.to_json())
