from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__)

from Golden_Leaf.api import product, category, client, clerk, order, erros, payment, report

@api.after_request
def add_header(response):
    response.headers.add('Access-Control-Allow-Origin',
                         'http://golden-leaf.herokuapp.com')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    return response

@api.before_request
def verify_header():
    if request.method == 'POST' and not request.is_json:
        response = jsonify({"Erro": "Tipo de conteúdo inválido.",
                                "Mensagem": 'Para metodos do tipo POST o sevidor processa somente requisições do tipo application/json'})
        response.status_code = 415
        return response

