from flask import render_template, current_app, request, redirect, url_for, flash, jsonify
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required, current_user
from sqlalchemy import func
from Golden_Leaf import db
from Golden_Leaf.models import Order, Client, Item
from Golden_Leaf.views.order import blueprint_order
from Golden_Leaf.views.order.forms import SearchOrderForm
import jwt
from datetime import datetime,timedelta

def view_client_dlc(*args, **kwargs):
    id = request.view_args['id']
    c = Client.query.get(id)
    return [{'text': c.name}]


def view_order_dlc(*args, **kwargs):
    id = request.view_args['id']
    c = Order.query.get(id)
    return [{'text': "renan"}]


@blueprint_order.route('/order/client/<int:id>', methods=['GET'])
@blueprint_order.route('/order', defaults={'id': None}, methods=['GET'])
@register_breadcrumb(blueprint_order, '.', 'Pedidos')
def get_orders(id):
    page = request.args.get('page', 1, type=int)
    if id is not None:
        orders = Order.query \
            .filter_by(client_id=id) \
            .order_by(Order.date.desc()) \
            .paginate(page=page, per_page=10)
        return render_template('order/client_orders.html', orders=orders, client_id=id)
    orders = Order.query.order_by(Order.date.desc()).paginate(page=page, per_page=10)
    return render_template('order/list.html', orders=orders)


@blueprint_order.route('/client/<int:id>/order/new', methods=["GET", 'POST'])
@register_breadcrumb(blueprint_order, '.id', '', dynamic_list_constructor=view_client_dlc)
@login_required
def new_order(id):
    client = Client.query.get_or_404(id)
    token = get_token(client.id, current_user.id)
    return render_template('order/new.html', token=token)


@blueprint_order.route('/order/<int:id>/items', methods=['GET'])
# @register_breadcrumb(blueprint_order, '.id', '',
# dynamic_list_constructor=view_order_dlc)
@login_required
def items_order(id):
    order = Order.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    all_items = Item.query.filter_by(order=order).paginate(page, per_page=10)
    return render_template('order/items.html', order_items=all_items)


@blueprint_order.route('/order/search', methods=["GET", 'POST'])
@register_breadcrumb(blueprint_order, '.search_order', 'Busca de Pedido')
def search_order():
    page = request.args.get('page', 1, type=int)
    form = SearchOrderForm()
    if form.validate_on_submit():
        client = form.clients.data
        clerk = form.clerks.data        
        orders = None
        if clerk is not None:
            if client is not None:
                orders = Order.query.filter_by(client=client, clerk=clerk).paginate(page=page,
                                                                                                   per_page=10)
            else:
                orders = Order.query.filter_by(clerk=clerk).paginate(page=page,
                                                                                    per_page=10)

        elif client is not None:
            orders = Order.query.filter_by(client=client).paginate(page=page,
                                                                                  per_page=10)

        if orders:
            flash('Pedido algum encontrado', 'warning')
            return redirect(url_for('blueprint_order.search_order'))
        else:
            flash('Mostrando todos os pedidos encontrados', 'success')
            return render_template('order/list.html', orders=orders)

    return render_template("order/search.html", form=form)



def get_token(client_id, clerk_id, expires_in=25):
    secret = current_app.config['SECRET_KEY']
    payload = {'client_id': client_id,
               'clerk_id': clerk_id,
               'exp': datetime.utcnow() + timedelta(minutes=expires_in)}
    token = jwt.encode(payload, secret)
    return token.decode('UTF-8')
