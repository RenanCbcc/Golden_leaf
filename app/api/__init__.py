from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import product, category, client, clerk, order, erros
