from flask import render_template

from app.error import blueprint_error


@blueprint_error.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html'), 404


@blueprint_error.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html'), 500
