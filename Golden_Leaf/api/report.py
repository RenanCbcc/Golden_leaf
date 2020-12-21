from flask import jsonify
from sqlalchemy import func
from Golden_Leaf.api import api
from Golden_Leaf.models import Payment,Order,db
from datetime import datetime
from datetime import timedelta

def get_income(date:datetime) -> float:
    income = db.session.query(func.sum(Payment.amount)).filter(Payment.date > date).scalar()
    if income is None:
        return 0
    else:
        return income

def get_salles(date:datetime) -> float:
    salles = db.session.query(func.sum(Order.total)).filter(Order.date > date).scalar()
    if salles is None:
        return 0
    else:
        return salles


@api.route('/report/balance', methods=['GET'])
def balance():
    today = datetime.now()
    yesterday = today - timedelta(days = 1) 
    income = get_income(yesterday)
    salles = get_salles(yesterday)
    response = jsonify({"salles":str(salles),"income":str(income)})
    response.status_code = 200
    return response

@api.route('/report/most-seling', methods=['GET'])
def topSalles():
    balance = db.session.query(func.sum(Payment.amount)).scalar()
    response = jsonify(str(balance))
    response.status_code = 200
    return response
