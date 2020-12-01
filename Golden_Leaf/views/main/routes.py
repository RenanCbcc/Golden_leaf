from flask_breadcrumbs import register_breadcrumb
from Golden_Leaf.views.main import blueprint_main
from flask import render_template


@blueprint_main.route('/')
@register_breadcrumb(blueprint_main, '.', 'Home')
def index():
    return render_template('main/index.html')


@blueprint_main.route('/about')
def about():
    return '<html><h1>TODO</h1></html>'