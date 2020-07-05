import decimal
import jwt
from flask import jsonify, request, url_for, current_app
from app.api import api
from sqlalchemy import func
from app.models import Order, Status, Payment, Client, Clerk, db
from flask_inputs import Inputs
from wtforms.validators import DataRequired, Regexp, ValidationError
from app.api.clerk import auth


def validate_payment(form, field):
    secret = current_app.config['SECRET_KEY']
    try:
        data = jwt.decode(field.data, secret)
    except jwt.ExpiredSignatureError:
        # valid token, but expired
        raise ValidationError('O pedido de pagamento expirou.')
    except jwt.InvalidTokenError:
        # invalid token
        raise ValidationError('O pedido de pagamento é inválido')

    valide_client_id(data)
    valide_clerk_id(data)
    validate_payment_amount(data)
    return True


def valide_client_id(data: dict):
    if 'client_id' not in data:
        raise ValidationError("O pagamento precisa ter um campo 'client_id'.")
    if not Client.query.filter_by(id=data['client_id']).first():
        raise ValidationError(
            f"Id '{data['client_id']}' do cliente é inválido.")


def valide_clerk_id(data: dict):
    if 'clerk_id' not in data:
        raise ValidationError("O pagamento precisa ter um campo 'clerk_id'.")
    if not Clerk.query.filter_by(id=data['clerk_id']).first():
        raise ValidationError(
            f"Id '{data['clerk_id']}' do atendente é inválido.")


def validate_payment_amount(data: dict):
    if 'amount' not in data:
        raise ValidationError('O pagamento precisa um valor.')
    if is_decimal(field.data):
        payment_value = float(field.data)
        if payment_value < 0.1 or payment_value > 1000.0:
            raise ValidationError(
                "O valor do pagamento estar entre R$ 0.1 e R$ 1000.0")
        else:
            return
    raise ValidationError(f"Valor '{field.data}' para pagamento é inválido.")


def is_decimal(value: str) -> bool:
    try:
        decimal.Decimal(value)
        return True
    except:
        return False


class PaymentInputs(Inputs):
    # Dont change this name!  Keep it as json!
    json = {
        'payment': [DataRequired(message="É preciso o pagamento em forma de token."), validate_payment],
    }


@api.route('/payment', defaults={'id': None}, methods=['GET'])
@api.route('/payment/client/<int:id>', methods=['GET'])
def get_payment(id):
    if id is not None:
        payments = Payment.query.filter_by(client_id=id).order_by(
            Payment.paid.desc()).all()
        response = jsonify([payment.to_json() for payment in payments])
        response.status_code = 200
        return response

    payments = Payment.query.order_by(
        Payment.paid.desc()).all()
    response = jsonify([payment.to_json() for payment in payments])
    response.status_code = 200
    return response


@api.route('/payment/<int:id>/order', methods=['GET'])
def get_orders(id):
    orders = Order.query.filter_by(payment_id=id).order_by(Order.date.desc())
    response = jsonify([order.to_json() for order in orders])
    response.status_code = 200
    return response


@api.route('/payment', methods=['POST'])
@auth.login_required
def new_payment():
    paymentInputs = PaymentInputs(request)
    if paymentInputs.validate():
        client_id = request.json.get('client_id')
        payment_value = request.json.get('value')
        if payment_value > get_order_total(client_id):
            return payment_value_error(payment_value)
        else:
            clerk_id = request.json.get('clerk_id')
            payment = create_payment(client_id, clerk_id, payment_value)
            db.session.add(payment)
            pay_off(payment)
            db.session.commit()
            return payment_successfuly(payment)
    else:
        reponse = jsonify(paymentInputs.errors)
        reponse.status_code = 400
        return reponse


def create_payment(client_id: str, clerk_id: str, value: decimal) -> Payment:
    client = Client.query.get(client_id)
    clerk = Clerk.query.get(clerk_id)
    return Payment(client, clerk, decimal.Decimal(value))


def get_order_total(id) -> float:
    return db.session.query(func.sum(Order.total)) \
        .filter_by(client_id=id, status=Status.PENDENTE) \
        .scalar()


def get_orders_of_client(id):
    return Order.query.filter_by(
        client_id=id, status=Status.PENDENTE).order_by(Order.date).all()


def payment_value_error(value) -> str:
    response = jsonify({"Erro": "Pagamento inválido",
                                "Mensagem": 'Valor para pagamento ' + str(value) + ' é maior que o valor devido.'})
    response.status_code = 400
    return response


def payment_successfuly(payment: Payment) -> str:
    response = jsonify(
        {'Sucesso': 'Pagamento recebido com sucesso!', 'payment_id': payment.id})
    response.status_code = 201
    send_message(payment)
    return response


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
