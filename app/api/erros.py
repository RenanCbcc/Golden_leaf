from flask import jsonify
from werkzeug.routing import ValidationError

from app.api import api


@api.app_errorhandler(404)
def resource_not_found(error):
    response = jsonify({'error': 'Not found', 'message': error.description})
    response.status_code = 404
    return response


@api.app_errorhandler(500)
def internal_server_error(error):
    response = jsonify(
        {'error': 'Internal server error', 'message': error.description})
    response.status_code = 500
    return response


@api.errorhandler(400)
def validation_error(error):
    response = jsonify({'error': 'Bad request', 'message': error.description})
    response.status_code = 400
    return response


@api.errorhandler(401)
def unauthorized(error):
    response = jsonify(
        {'error': 'Invalid credentials', 'message': error.description})
    response.status_code = 401
    return response


@api.errorhandler(403)
def forbidden(error):
    response = jsonify({'error': 'forbidden', 'message': error.description})
    response.status_code = 403
    return response


@api.errorhandler(405)
def method_not_allowed(error):
    response = jsonify({'error': 'Method not allowed', 'message': error.description})
    response.status_code = 405
    return response
