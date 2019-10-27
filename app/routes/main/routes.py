from flask import render_template
from flask_breadcrumbs import register_breadcrumb

from app.routes.main import blueprint_main


@blueprint_main.route('/')
@register_breadcrumb(blueprint_main, '.', 'Home')
def index():
    return render_template('index.html')


@blueprint_main.route('/about')
def about():
    return '<html><h1>TODO</h1></html>'
