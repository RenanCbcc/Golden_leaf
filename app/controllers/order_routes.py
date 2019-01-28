from app import app
from flask_login import login_required
from app.models.tables import Order
from flask import render_template


@app.route('/client/order', defaults={'id': None})
@app.route('/client/<int:id>/order')
@login_required
def listing_orders_of(id):
    if id is not None:
        list_of_orders = Order.query.filter_by(client_id=id).first()
        return render_template('order/list.html', orders=list_of_orders)
    else:
        list_of_orders = Order.query.all()
        return render_template('order/list.html', orders=list_of_orders)


@app.route('/client/order/new', defaults={'id': None})
@app.route('/client/<int:id>/order/new')
@login_required
def new_order(id):
    return '<html><h1>TODO</h1><html>'
