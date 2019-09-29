from flask import jsonify
from werkzeug.routing import ValidationError

from app.api import api


@api.app_errorhandler(404)
def page_not_found(error):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response


@api.app_errorhandler(404)
def resource_not_found(error):
    response = jsonify({'error': 'Not found', 'message': 'The resource referenced in the URL was not found.'})
    response.status_code = 404
    return response


@api.app_errorhandler(ValidationError)
def internal_server_error(error):
    response = jsonify(
        {'error': 'Internal server error', 'message': 'An unexpected error has occurred while processing the request.'})
    response.status_code = 500
    return response


@api.errorhandler(400)
def validation_error(error):
    response = jsonify({'error': 'Bad request', 'message': 'The request is invalid or inconsistent.'})
    response.status_code = 400
    return response


@api.errorhandler(401)
def unauthorized(error):
    response = jsonify(
        {'error': 'Invalid credentials', 'message': 'The request does not include authentication information.'})
    response.status_code = 401
    return response


@api.errorhandler(403)
def forbidden(error):
    response = jsonify({'error': 'forbidden',
                        'message': 'The authentication credentials sent with the request are insufficient for the request.'})
    response.status_code = 403
    return response


@api.errorhandler(405)
def method_not_allowed(message):
    response = jsonify({'error': 'Method not allowed', 'message': message})
    response.status_code = 405
    return response
