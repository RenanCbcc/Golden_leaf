from flask_breadcrumbs import register_breadcrumb
from app.routes.main import blueprint_main

"""
I only kep this to keep the breadcrumb working. Otherwise i got a 'Not registered menu'. 
"""
@blueprint_main.route('/')
@register_breadcrumb(blueprint_main, '.', 'Home')
def index():
    return '<html><h1>TODO</h1></html>'


@blueprint_main.route('/about')
def about():
    return '<html><h1>TODO</h1></html>'