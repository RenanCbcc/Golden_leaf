from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange

from app.models.tables import Client, Clerk


def enabled_clients():
    return Client.query


def enabled_clerks():
    return Clerk.query


class NewPaymentForm(FlaskForm):
    total = DecimalField('Total R$ ', render_kw={'disabled': ''})
    value = DecimalField('Valor R$ ', validators=[DataRequired(), NumberRange(min=0.1, max=100.0)])
    submit = SubmitField('Pagar')


class SearchPaymentForm(FlaskForm):
    clerks = QuerySelectField('Atendentes',
                              query_factory=enabled_clerks, allow_blank=True,
                              get_label='name', get_pk=lambda a: a.id,
                              blank_text=u'Selecione um atendente...')

    clients = QuerySelectField('Clientes',
                               query_factory=enabled_clients, allow_blank=True,
                               get_label='name', get_pk=lambda c: c.id,
                               blank_text=u'Selecione um cliente...')

    # date = DateField("Data")
    submit = SubmitField('Buscar')
