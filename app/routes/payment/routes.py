from flask import request, redirect, url_for, render_template, flash
from flask_breadcrumbs import register_breadcrumb
from flask_login import current_user
from sqlalchemy import func

from app import db
from app.models import Order, Status, Payment, Client
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
        payments = Payment.query.filter_by(client_id=id).order_by(Payment.paid.desc()).paginate(page=page, per_page=10)
        return render_template('payment/list.html', payments=payments)

    payments = Payment.query.order_by(Payment.paid.desc()).paginate(page=page, per_page=10)
    return render_template('payment/list.html', payments=payments)


@blueprint_payment.route('/payment/<int:id>/order', methods=['GET'])
def get_orders(id):
    page = request.args.get('page', 1, type=int)
    orders = Order.query \
        .filter_by(payment_id=id) \
        .order_by(Order.ordered.desc()) \
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
                payments = Payment.query.filter_by(client=client, clerk=clerk).paginate(page=page, per_page=10)
            else:
                payments = Payment.query.filter_by(clerk=clerk, ).paginate(page=page, per_page=10)

        elif client is not None:
            payments = Payment.query.filter_by(client=client, ).paginate(page=page, per_page=10)

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
        total = db.session.query(func.sum(Order.total)) \
            .filter_by(client_id=id) \
            .scalar()
        payment_value = form.value.data
        if payment_value > total or payment_value <= 0.0:
            flash('Valor para pagamento ' + str(payment_value) + ' inválido.', 'warning')
            return redirect(url_for('blueprint_payment.new_payment', id=id))
        else:
            orders = Order.query.filter_by(client_id=id, status=Status.PENDENTE).order_by(Order.ordered).all()
            client = Client.query.get(id)
            payment = Payment(client, current_user, payment_value)
            db.session.add(payment)
            value = payment_value
            while value > 0:
                for order in orders:
                    if value >= order.total:
                        value = value - order.total
                        order.status = Status.PAGO

                    else:
                        order.total = order.total - value
                        value = 0
                    order.payment = payment
                    payment.orders.append(order)

            db.session.commit()
            # send_message(client, request.form['value'])
            flash('Pagamento recebido com sucesso!', 'success')
            return redirect(url_for('blueprint_payment.get_payment', id=id))
    elif request.method == 'GET':
        total = db.session.query(func.sum(Order.total)) \
            .filter_by(client_id=id, status=Status.PENDENTE) \
            .scalar()
        form.total.data = total
        return render_template('payment/new.html', form=form)


def send_message(client, value):
    if client.notifiable:
        account_sid = 'AC06b6d740e2dbe8c1c94dd41ffed6c3a3'
        auth_token = '2e22811c3a09a717ecd754b7fb527794'
        from twilio.rest import Client as Twilio_Client
        twilio_client = Twilio_Client(account_sid, auth_token)

        twilio_client.messages.create(
            body='Olá, ' + client.name +
                 ' . Você debitou R$ ' + value + ' de sua conta. Volte sempre!',
            from_='+12054311596',
            to='+55' + client.phone_number
        )
