from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from sqlalchemy import func

from app import db
from app.models.tables import Order, Client, Item, Status
from app.order import blueprint_order
from app.order.forms import SearchOrderForm


@blueprint_order.route('/order/client/<int:id>', methods=['GET'])
@blueprint_order.route('/order', defaults={'id': None}, methods=['GET'])
@login_required
def get_orders(id):
    page = request.args.get('page', 1, type=int)
    if id is not None:
        if page == 1:
            total = db.session.query(func.sum(Order.cost)).filter_by(client_id=id).scalar()
        orders = Order.query.filter_by(client_id=id).order_by(Order.date.desc()).paginate(page=page, per_page=10)
        return render_template('order/client_orders.html', orders=orders, client_id=id, total=total)

    orders = Order.query.order_by(Order.date.desc()).paginate(page=page, per_page=10)
    return render_template('order/list.html', orders=orders)


@blueprint_order.route('/order/new', defaults={'id': None}, methods=["GET", 'POST'])
@blueprint_order.route('/client/<int:id>/order/new', methods=["GET", 'POST'])
@login_required
def new_order(id):
    if id is not None:
        client = Client.query.filter_by(id=id).one()
        return render_template('order/new.html', client=client)
    return render_template('order/new.html')


@blueprint_order.route('/order/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_order(id):
    order = Order.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    all_items = Item.query.filter_by(order=order).paginate(page, per_page=10)
    return render_template('order/edit.html', order_items=all_items)


@blueprint_order.route('/order/search', methods=["GET", 'POST'])
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

        if not orders:
            flash('Pedido algum encontrado', 'warning')
            return redirect(url_for('blueprint_order.search_order'))
        else:
            flash('Mostrando todos os pedidos encontrados', 'success')
            return render_template('order/list.html', orders=orders)

    return render_template("order/search.html", form=form)


@blueprint_order.route('/order/client/<int:id>/pending', methods=['GET'])
@login_required
def pending_order(id):
    page = request.args.get('page', 1, type=int)
    if page == 1:
        total = db.session.query(func.sum(Order.cost)).filter_by(client_id=id).scalar()
    order = Order.query.filter_by(client_id=id, status=Status.PENDENTE).order_by(Order.date.desc()).paginate(page=page,
                                                                                                             per_page=10)
    return render_template('order/pending_order.html', orders=order, client_id=id, total=total)


@blueprint_order.route('/order/payment', methods=['POST'])
def process_payment():
    # import decimal
    # value = decimal.Decimal(request.form['paymentValue'])
    # client_id = request.form['clientId']
    # if value <= 0:
    #     from flask import abort
    #     abort(400)
    # orders = Order.query.filter_by(client_id=client_id, status=Status.PENDENTE).order_by(
    #     Order.date).all()
    # while value > 0:
    #     for order in orders:
    #         if value - order.cost > 0:
    #             value = value - order.cost
    #             order.cost = 0
    #             order.status = Status.PAGO
    #         else:
    #             order.cost = order.cost - value
    #             value = 0
    #
    # from app import db
    # db.session.add_all(orders)
    # db.session.commit()
    # send_message(client_id, request.form['value'])
    # return redirect(url_for('blueprint_order.pending_order', id=client_id))
    return "OK"


def send_message(id, value):
    client = Client.query.get(id)
    if client.notifiable:
        account_sid = 'AC06b6d740e2dbe8c1c94dd41ffed6c3a3'
        auth_token = 'a9a6f4600d1d55989d325443eda3c55e'
        from twilio.rest import Client as Twilio_Client
        twilio_client = Twilio_Client(account_sid, auth_token)

        twilio_client.messages.create(
            body='Olá, ' + client.name +
                 ' .Você debitou R$ ' + value + ' de sua conta. Volte sempre!',
            from_='+12054311596',
            to='+55' + client.phone_number
        )
