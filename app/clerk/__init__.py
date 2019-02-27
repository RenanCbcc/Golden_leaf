# A blueprint needs to be a package. That's why all folders needs to have a __init__.py
from flask import Blueprint

blueprint_clerk = Blueprint('blueprint_clerk', __name__)
