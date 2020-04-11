from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import product, category, client, clerk, order, erros

@api.after_request
def add_header(response):
    response.headers.add('Access-Control-Allow-Origin','https://golden-leaf.herokuapp.com/api')
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization')    
    return response
