from flask import jsonify, request, url_for, g
from flask_httpauth import HTTPBasicAuth
from app.models.tables import Clerk
from app.api.erros import unauthorized, forbidden, resource_not_found
from app.api import api

auth = HTTPBasicAuth()


@api.route('/login', methods=['GET', 'POST'])
def login(email, password):
    clerk = Clerk.query.filter_by(email=email).first()
    if not clerk:
        return resource_not_found()
    else:
        if Clerk.verify_password(password):
            g.current_user = clerk
            return jsonify(clerk.to_json())
        else:
            return unauthorized()


@auth.verify_password
def verify_password(email_or_token, password):
    if password == '':
        g.current_user = Clerk.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    clerk = Clerk.query.filter_by(email=email_or_token).first()
    if not clerk:
        return False
    g.current_user = clerk
    return Clerk.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized()


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.confirmed:
        return forbidden()


@api.route('/token')
def get_token():
    if g.token_used:
        return unauthorized()
    return jsonify({'token': g.current_user.generate_auth_token(expiration=3600), 'expiration': 3600})
