from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from app.models import Client, Clerk


def enabled_clients():
    return Client.query


def enabled_clerks():
    return Clerk.query


class SearchOrderForm(FlaskForm):
    clerks = QuerySelectField('Atendentes',
                              query_factory=enabled_clerks, allow_blank=True,
                              get_label='name', get_pk=lambda a: a.id,
                              blank_text=u'Selecione uma atendente...')

    clients = QuerySelectField('Clientes',
                               query_factory=enabled_clients, allow_blank=True,
                               get_label='name', get_pk=lambda c: c.id,
                               blank_text=u'Selecione um cliente...')

    # date = DateField("Data")
    status = SelectField("Status", choices=[('PAGO', 'Pago'), ('PENDENTE', 'Pendente')])
    submit = SubmitField('Buscar')
