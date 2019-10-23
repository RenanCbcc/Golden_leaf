from flask import render_template, request, redirect, url_for, flash
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required
from sqlalchemy import func

from app import db
from app.models.tables import Order, Client, Item, Status
from app.order import blueprint_order
from app.order.forms import SearchOrderForm


def view_client_dlc(*args, **kwargs):
    id = request.view_args['id']
    c = Client.query.get(id)
    return [{'text': c.name}]


@blueprint_order.route('/order/client/<int:id>', methods=['GET'])
@blueprint_order.route('/order', defaults={'id': None}, methods=['GET'])
@register_breadcrumb(blueprint_order, '.', 'Pedidos')
@login_required
def get_orders(id):
    page = request.args.get('page', 1, type=int)
    if id is not None:
        orders = Order.query \
            .filter_by(client_id=id) \
            .order_by(Order.ordered.desc()) \
            .paginate(page=page, per_page=10)
        return render_template('order/client_orders.html', orders=orders, client_id=id)
    orders = Order.query.order_by(Order.ordered.desc()).paginate(page=page, per_page=10)
    return render_template('order/list.html', orders=orders)


@blueprint_order.route('/client/<int:id>/order/new', methods=["GET", 'POST'])
@register_breadcrumb(blueprint_order, '.id', '', dynamic_list_constructor=view_client_dlc)
@login_required
def new_order(id):
    client = Client.query.get_or_404(id)
    return render_template('order/new.html', client=client)


# @blueprint_order.route('/order/new', methods=["GET", 'POST'])
# @register_breadcrumb(blueprint_order, '.new_loose_order', 'Novo Pedido')
# @login_required
# def new_loose_order():
#     return render_template('order/new.html', client=None)


@blueprint_order.route('/order/<int:id>/update', methods=['GET', 'POST'])
# @register_breadcrumb(blueprint_order, '.id', '', dynamic_list_constructor=view_client_dlc)
@login_required
def update_order(id):
    order = Order.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    all_items = Item.query.filter_by(order=order).paginate(page, per_page=10)
    return render_template('order/edit.html', order_items=all_items)


@blueprint_order.route('/order/search', methods=["GET", 'POST'])
@register_breadcrumb(blueprint_order, '.search_order', 'Busca de Pedido')
def search_order():
    page = request.args.get('page', 1, type=int)
    form = SearchOrderForm()
    if form.validate_on_submit():
        client = form.clients.data
        clerk = form.clerks.data
        status = Status[form.status.data]
        orders = None
        if clerk is not None:
            if client is not None:
                orders = Order.query.filter_by(client=client, clerk=clerk, status=status).paginate(page=page,
                                                                                                   per_page=10)
            else:
                orders = Order.query.filter_by(clerk=clerk, status=status).paginate(page=page,
                                                                                    per_page=10)

        elif client is not None:
            orders = Order.query.filter_by(client=client, status=status).paginate(page=page,
                                                                                  per_page=10)

        if orders:
            flash('Pedido algum encontrado', 'warning')
            return redirect(url_for('blueprint_order.search_order'))
        else:
            flash('Mostrando todos os pedidos encontrados', 'success')
            return render_template('order/list.html', orders=orders)

    return render_template("order/search.html", form=form)


@blueprint_order.route('/order/client/<int:id>/pending', methods=['GET'])
@register_breadcrumb(blueprint_order, '.id', '', dynamic_list_constructor=view_client_dlc)
@login_required
def pending_order(id):
    page = request.args.get('page', 1, type=int)
    if page == 1:
        total = db.session.query(func.sum(Order.total)) \
            .filter_by(client_id=id, status=Status.PENDENTE) \
            .scalar()
    orders = Order.query.filter_by(client_id=id, status=Status.PENDENTE) \
        .order_by(Order.ordered.desc()) \
        .paginate(page=page, per_page=10)
    return render_template('order/pending_order.html', orders=orders, client_id=id, total=total)


@blueprint_order.route('/order/payment', methods=['POST'])
def process_payment():
    import decimal
    value = decimal.Decimal(request.form['paymentValue'])
    client_id = request.form['clientId']
    if value <= 0:
        from flask import abort
        abort(400)
    orders = Order.query.filter_by(client_id=client_id, status=Status.PENDENTE).order_by(
        Order.ordered).all()
    while value > 0:
        for order in orders:
            if value - order.cost > 0:
                value = value - order.cost
                order.cost = 0
                order.status = Status.PAGO
            else:
                order.cost = order.cost - value
                value = 0

    from app import db
    db.session.add_all(orders)
    db.session.commit()
    # send_message(client_id, request.form['value'])
    return redirect(url_for('blueprint_order.pending_order', id=client_id))
