from flask_login import login_required
from app.models.tables import Order
from flask import render_template

from flask import Blueprint

from app.order.forms import SearchOrderForm, NewOrderForm

orders = Blueprint('orders', __name__)


@orders.route('/client/order', defaults={'id': None})
@orders.route('/client/<int:id>/order')
@login_required
def listing_orders_of(id):
    if id is not None:
        list_of_orders = Order.query.filter_by(client_id=id).first()
        return render_template('order/list.html', orders=list_of_orders)
    else:
        list_of_orders = Order.query.all()
        return render_template('order/list.html', orders=list_of_orders)


@orders.route('/client/order/new', defaults={'id': None})
@orders.route('/client/<int:id>/order/new')
@login_required
def new_order(id):
    form = NewOrderForm()
    if form.validate_on_submit():
        pass
    else:
        pass
    return render_template('order/new.html', form=form)


@orders.route('/order/<int:id>/update', methods=["GET", 'POST'])
def update_order(id):
    return '<html><h1>TODO</h1><html>'


@orders.route('/order/search', methods=["GET", 'POST'])
def search_order():
    form = SearchOrderForm()
    if form.validate_on_submit():
        pass
    else:
        pass

    return render_template("order/search.html", form=form)
