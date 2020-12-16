from flask import request, redirect, url_for, render_template, flash
from flask_breadcrumbs import register_breadcrumb
from flask_login import current_user, login_required
from sqlalchemy import func
from Golden_Leaf.models import Order, Payment, Client, db
from Golden_Leaf.views.payment import blueprint_payment
from Golden_Leaf.views.payment.forms import NewPaymentForm, SearchPaymentForm


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
        payments = Payment.query.filter_by(client_id=id).order_by(Payment.date.desc()).paginate(page=page, per_page=10)
        return render_template('payment/list.html', payments=payments)

    payments = Payment.query.order_by(Payment.date.desc()).paginate(page=page, per_page=10)
    return render_template('payment/list.html', payments=payments)



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
                payments = Payment.query.filter_by(clerk=clerk,).paginate(page=page, per_page=10)

        elif client is not None:
            payments = Payment.query.filter_by(client=client,).paginate(page=page, per_page=10)

        if not payments:
            flash('Pagamento algum encontrado', 'warning')
            return redirect(url_for('blueprint_payment.search_payment'))
        else:
            flash('Mostrando todos os pagamentos encontrados', 'info')
            return render_template('payment/list.html', payments=payments)

    return render_template("payment/search.html", form=form)


@blueprint_payment.route('/payment/new/client/<int:id>', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_payment, '.id', '', dynamic_list_constructor=view_client_dlc)
@login_required
def new_payment(id):
    form = NewPaymentForm()
    if form.validate_on_submit():
        payment_value = form.value.data
        if payment_value > get_order_total(id):
            flash('Valor para pagamento ' + str(payment_value) + ' inválido.', 'warning')
            return redirect(url_for('blueprint_payment.new_payment', id=id))
        else:
            client = Client.query.get(id)            
            payment = Payment(client.id, current_user.id, payment_value)
            db.session.add(payment)
            pay_off(client,payment)            
            db.session.commit()
            # send_message(client, request.form['value'])
            flash('Pagamento recebido com sucesso!', 'success')
            return redirect(url_for('blueprint_payment.get_payment', id=id))
    
    form.total.data = get_order_total(id)
    return render_template('payment/new.html', form=form)


def get_order_total(client_id) -> float:
    return db.session.query(func.sum(Client.amount)) \
        .filter_by(id=client_id) \
        .scalar()


def get_orders_of_client(id):
    return Order.query.filter_by(client_id=id).order_by(Order.date).all()


def get_client(client_id) -> Client:
    return Client.query.filter_by(id=client_id).first()

def pay_off(client:Client, payment: Payment) -> None:
    value = payment.amount
    client.amount -= value 


def send_message(payment: Payment) -> None:
    if payment.client.notifiable:
        account_sid = current_app.config['ACOUNT_SID']
        auth_token = current_app.config['AUTH_TOKEN']
        from twilio.rest import Client as Twilio_Client
        twilio_client = Twilio_Client(account_sid, auth_token)

        twilio_client.messages.create(body='Olá, ' + client.name + ' . Você debitou R$ ' + value + ' em sua conta. Volte sempre!',
            from_='+12054311596',
            to='+55' + client.phone_number)
