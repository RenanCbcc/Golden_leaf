from flask import request, redirect, url_for, render_template, flash
from flask_breadcrumbs import register_breadcrumb
from flask_login import current_user
from sqlalchemy import func
from app.models import Order, Status, Payment, Client, db
from app.routes.payment import blueprint_payment
from app.routes.payment.forms import NewPaymentForm, SearchPaymentForm


def view_client_dlc(*args, **kwargs):
    id = request.view_args['id']
    c = Client.query.get(id)
    return [{'text': c.name}]


@blueprint_payment.route('/payment', defaults={'id': None}, methods=['GET'])
@blueprint_payment.route('/payment/client/<int:id>', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_payment, '.', 'Pagamentos')
def get_payment(id):
    page = request.args.get('page', 1, type=int)
    if id is not None:
        payments = Payment.query.filter_by(client_id=id).order_by(
            Payment.date.desc()).paginate(page=page, per_page=10)
        return render_template('payment/list.html', payments=payments)

    payments = Payment.query.order_by(
        Payment.date.desc()).paginate(page=page, per_page=10)
    return render_template('payment/list.html', payments=payments)


@blueprint_payment.route('/payment/<int:id>/order', methods=['GET'])
def get_orders(id):
    page = request.args.get('page', 1, type=int)
    orders = Order.query \
        .filter_by(payment_id=id) \
        .order_by(Order.date.desc()) \
        .paginate(page=page, per_page=10)
    return render_template('order/client_orders.html', orders=orders)


@blueprint_payment.route('/payment/search', methods=["GET", 'POST'])
@register_breadcrumb(blueprint_payment, '.search_payment', 'Busca de Pagamento')
def search_payment():
    page = request.args.get('page', 1, type=int)
    form = SearchPaymentForm()
    if form.validate_on_submit():
        client = form.clients.data
        clerk = form.clerks.data
        payments = None
        if clerk is not None:
            if client is not None:
                payments = Payment.query.filter_by(
                    client=client, clerk=clerk).paginate(page=page, per_page=10)
            else:
                payments = Payment.query.filter_by(
                    clerk=clerk, ).paginate(page=page, per_page=10)

        elif client is not None:
            payments = Payment.query.filter_by(
                client=client, ).paginate(page=page, per_page=10)

        if not payments:
            flash('Pagamento algum encontrado', 'warning')
            return redirect(url_for('blueprint_payment.search_payment'))
        else:
            flash('Mostrando todos os pagamentos encontrados', 'info')
            return render_template('payment/list.html', payments=payments)

    return render_template("payment/search.html", form=form)


@blueprint_payment.route('/payment/new/client/<int:id>', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_payment, '.id', '', dynamic_list_constructor=view_client_dlc)
def new_payment(id):
    form = NewPaymentForm()
    if form.validate_on_submit():
        payment_value = form.value.data
        if payment_value > get_order_total(id):
            flash('Valor para pagamento ' +
                  str(payment_value) + ' inválido.', 'warning')
            return redirect(url_for('blueprint_payment.new_payment', id=id))
        else:
            client = Client.query.get(id)
            payment = Payment(client, current_user, payment_value)
            db.session.add(payment)
            pay_off(payment)
            db.session.commit()
            # send_message(client, request.form['value'])
            flash('Pagamento recebido com sucesso!', 'success')
            return redirect(url_for('blueprint_payment.get_payment', id=id))
    elif request.method == 'GET':
        form.total.data = get_order_total(id)
        return render_template('payment/new.html', form=form)


def get_order_total(id) -> float:
    return db.session.query(func.sum(Order.total)) \
        .filter_by(client_id=id, status=Status.PENDENTE) \
        .scalar()


def get_orders_of_client(id):
    return Order.query.filter_by(
        client_id=id, status=Status.PENDENTE).order_by(Order.date).all()


def pay_off(payment: Payment) -> None:
    value = payment.total
    while value > 0:
        for order in get_orders_of_client(payment.client_id):
            if value >= order.total:
                value = value - order.total
                order.status = Status.PAGO

            else:
                order.total = order.total - value
                value = 0
                order.payment = payment
                payment.orders.append(order)


def send_message(payment: Payment) -> None:
    if payment.client.notifiable:
        account_sid = current_app.config['ACOUNT_SID']
        auth_token = current_app.config['AUTH_TOKEN']
        from twilio.rest import Client as Twilio_Client
        twilio_client = Twilio_Client(account_sid, auth_token)

        twilio_client.messages.create(
            body='Olá, ' + client.name +
                 ' . Você debitou R$ ' + value + ' em sua conta. Volte sempre!',
            from_='+12054311596',
            to='+55' + client.phone_number
        )