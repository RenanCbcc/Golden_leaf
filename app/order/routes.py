from flask_login import login_required
from app.models.tables import Order
from flask import render_template, redirect, url_for, request

from flask import Blueprint

from app.order.forms import SearchOrderForm, NewOrderForm

orders = Blueprint('orders', __name__)


@orders.route('/client/order', defaults={'id': None})
@orders.route('/client/<int:id>/order')
@login_required
def listing_orders_of(id):
    page = request.args.get('page', 1, type=int)
    if id is not None:
        orders = Order.query.filter_by(client_id=id).order_by(Order.date.desc()).paginate(page=page, per_page=10)
        return render_template('order/list.html', orders=orders)
    else:
        orders = Order.query.order_by(Order.date.desc()).paginate(page=page, per_page=10)
        return render_template('order/list.html', orders=orders)


@orders.route('/client/order/new', defaults={'id': None})
@orders.route('/client/<int:id>/order/new')
@login_required
def new_order(id):
    form = NewOrderForm()
    if form.validate_on_submit():
        return redirect(url_for('orders.listing_orders_of'))
    else:
        return redirect(url_for('orders.new_order'))
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
