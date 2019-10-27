from flask import render_template

from app.routes.error import blueprint_error


@blueprint_error.app_errorhandler(404)
def page_not_found(error):
    return render_template('error/404.html', error=error), 404


@blueprint_error.app_errorhandler(500)
def internal_server_error(error):
    return render_template('error/500.html', error=error), 500


@blueprint_error.app_errorhandler(400)
def bad_request(error):
    return render_template('error/400.html', error=error), 400


@blueprint_error.app_errorhandler(403)
def forbidden(error):
    return render_template('error/403.html', error=error), 403


@blueprint_error.app_errorhandler(401)
def unauthorized(error):
    return render_template('error/401.html', error=error), 401
