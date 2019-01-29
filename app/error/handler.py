from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def page_not_found():
    return render_template('error/404.html'), 404


@errors.app_errorhandler(500)
def internal_server_error():
    return render_template('error/500.html'), 500


@errors.app_errorhandler(400)
def page_not_found():
    return render_template('error/400.html'), 400
