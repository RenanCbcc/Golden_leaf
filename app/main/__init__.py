# A blueprint needs to be a package. That's why all folders needs to have a __init__.py
from flask import Blueprint
from flask_breadcrumbs import default_breadcrumb_root

main = Blueprint('main', __name__)
default_breadcrumb_root(main, '.')
