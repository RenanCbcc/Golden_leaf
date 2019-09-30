from flask_login import login_required

from app.models.tables import Order, Client, Item, Product
from flask import render_template, request, jsonify
from app.order import blueprint_order
from app.order.forms import SearchOrderForm


@blueprint_order.route('/orders', methods=['GET'])
@login_required
def get_orders():
    page = request.args.get('page', 1, type=int)
    orders = Order.query.order_by(Order.date.desc()).paginate(page=page, per_page=10)
    return render_template('order/list.html', orders=orders)


@blueprint_order.route('/order/new', defaults={'id': None}, methods=["GET", 'POST'])
@blueprint_order.route('/client/<int:id>/order/new', methods=["GET", 'POST'])
@login_required
def new_order(id):
    return render_template('order/new.html')


@blueprint_order.route('/orders/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_order(id):
    order = Order.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    all_items = Item.query.filter_by(order=order).paginate(page, per_page=10)
    return render_template('order/edit.html', order_items=all_items)


@blueprint_order.route('/order/search', methods=["GET", 'POST'])
def search_order():
    form = SearchOrderForm(Client.query.order_by(Client.name).all())
    if form.validate_on_submit():
        pass
    else:
        pass

    return render_template("order/search.html", form=form)
