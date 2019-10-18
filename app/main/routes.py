from flask import Blueprint, render_template
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root

from app.main import main


@main.route('/')
@register_breadcrumb(main, '.', 'Home')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return '<html><h1>TODO</h1></html>'
