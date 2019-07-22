from flask_login import login_required

from app import db
from app.models.tables import Order, Client, Item
from flask import render_template, request, jsonify, url_for
from app.order import blueprint_order
from app.order.forms import SearchOrderForm


@blueprint_order.route('/client/orders', defaults={'id': None}, methods=["GET", 'POST'])
@blueprint_order.route('/client/<int:id>/orders', methods=["GET", 'POST'])
@login_required
def listing_orders_of(id):
    page = request.args.get('page', 1, type=int)
    if id is not None:
        orders = Order.query.filter_by(client_id=id).order_by(Order.date.desc()).paginate(page=page, per_page=10)
        return render_template('order/list.html', orders=orders)
    else:
        orders = Order.query.order_by(Order.date.desc()).paginate(page=page, per_page=10)
        return render_template('order/list.html', orders=orders)


@blueprint_order.route('/order/new', defaults={'id': None}, methods=["GET", 'POST'])
@blueprint_order.route('/client/<int:id>/order/new', methods=["GET", 'POST'])
@login_required
def new_order(id):
    return render_template('order/new.html')


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


@blueprint_order.route('/order/save', methods=['POST'])
def save_order():
    print(request.json)
    # product = Product.from_json(request.json)
    # db.session.add(order)
    # db.session.commit()
    return request.json, 201, {'Location': "www.goldenleaf.com"}
