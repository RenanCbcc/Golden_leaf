from flask import jsonify
from werkzeug.routing import ValidationError

from app.api import api


@api.app_errorhandler(404)
def page_not_found(error):
    response = jsonify({'error': 'Not found'})
    response.status_code = 404
    return response


@api.app_errorhandler(ValidationError)
def internal_server_error(error):
    response = response = jsonify({'error': 'Internal server error'})
    response.status_code = 500
    return response


@api.errorhandler(400)
def validation_error(error):
    response = jsonify({'error': 'Bad request'})
    response.status_code = 400
    return response


@api.errorhandler(403)
def forbidden(error):
    response = jsonify({'error': 'Forbidden'})
    response.status_code = 403
    return response


@api.errorhandler(405)
def method_not_allowed(error):
    response = jsonify({'error': 'Method not allowed'})
    response.status_code = 405
    return response
