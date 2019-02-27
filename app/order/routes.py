from flask_login import login_required
from app.models.tables import Order, Client
from flask import render_template, redirect, url_for, request
from app.order import blueprint_order
from app.order.forms import SearchOrderForm, NewOrderForm


@blueprint_order.route('/client/orders', defaults={'id': None})
@blueprint_order.route('/client/<int:id>/orders')
@login_required
def listing_orders_of(id):
    page = request.args.get('page', 1, type=int)
    if id is not None:
        orders = Order.query.filter_by(client_id=id).order_by(Order.date.desc()).paginate(page=page, per_page=10)
        return render_template('order/list.html', orders=orders)
    else:
        orders = Order.query.order_by(Order.date.desc()).paginate(page=page, per_page=10)
        return render_template('order/list.html', orders=orders)


@blueprint_order.route('/order/new', defaults={'id': None})
@blueprint_order.route('/client/<int:id>/order/new')
@login_required
def new_order(id):
    if id is None:
        # Creating a list of tuples for conviniense
        clients = [(client.name) for client in Client.query.order_by(Client.name).all()]
    else:
        clients = [(client.name) for client in Client.query.filter_by(id=id).one()]
    form = NewOrderForm(clients)
    if form.validate_on_submit():
        return redirect(url_for('blueprint_orders.listing_orders_of'))
    return render_template('order/new.html', form=form)


@blueprint_order.route('/order/<int:id>/update', methods=["GET", 'POST'])
def update_order(id):
    return '<html><h1>TODO</h1><html>'


@blueprint_order.route('/order/search', methods=["GET", 'POST'])
def search_order():
    form = SearchOrderForm(Client.query.order_by(Client.name).all())
    if form.validate_on_submit():
        pass
    else:
        pass

    return render_template("order/search.html", form=form)
