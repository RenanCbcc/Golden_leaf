from flask import Blueprint, render_template, request, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


@errors.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html'), 500
