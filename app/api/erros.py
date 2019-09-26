from flask import jsonify
from werkzeug.routing import ValidationError

from app.api import api


@api.app_errorhandler(404)
def page_not_found(error):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response


@api.app_errorhandler(ValidationError)
def internal_server_error(message):
    response = jsonify({'error': 'Internal server error', 'message': message})
    response.status_code = 500
    return response


@api.errorhandler(400)
def validation_error(message):
    response = jsonify({'error': 'Bad request', 'message': message})
    response.status_code = 400
    return response


@api.errorhandler(401)
def unauthorized(message):
    response = jsonify({'error': 'Invalid credentials', 'message': message})
    response.status_code = 401
    return response


@api.errorhandler(403)
def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


@api.errorhandler(405)
def method_not_allowed(message):
    response = jsonify({'error': 'Method not allowed', 'message': message})
    response.status_code = 405
    return response
