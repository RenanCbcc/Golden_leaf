from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, DecimalField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange, Length

from app.models.tables import Product, Category


class UpdateOrderForm(FlaskForm):
    date = DateField("Data")
    client = StringField("Cliente")
    clerk = StringField("Atendente")
    status = SelectField("Status", choices=['Pago', 'Pendente'])
    submit = SubmitField('Buscar')


class SearchOrderForm(FlaskForm):
    date = DateField("Data")
    client = StringField("Cliente")
    clerk = StringField("Atendente")
    status = SelectField("Status", choices=['Pago', 'Pendente'])
    submit = SubmitField('Buscar')


class ManualNewOrderForm(FlaskForm):
    # client = StringField("Cliente", render_kw={'disabled': ''})
    category = SelectField('Categoria', coerce=int, choices=[])
    product = SelectField('Produto', coerce=int, choices=[])
    unit_cost = DecimalField('Preço do produto', render_kw={'disabled': ''})
    quantity = DecimalField("Quantidade",
                            validators=[DataRequired(),
                                        NumberRange(min=0.01, max=100.0, message="Quantidade inválida.")])
    # status = SelectField("Status", choices=[('pg', 'PAGO'), ('pd', 'PENDENTE')])
    submitManualNewOrderForm = SubmitField('Adicionar')


class AutomaticNewOrderForm(FlaskForm):
    code = StringField('Código do produto',
                       validators=[DataRequired(), Length(min=13, max=13, message="Código inválido.")])
    description = StringField('Descrição do produto', render_kw={'disabled': ''})
    unit_cost = DecimalField('Preço do produto', render_kw={'disabled': ''})
    quantity = DecimalField("Quantidade",
                            validators=[DataRequired(),
                                        NumberRange(min=0.01, max=100.0, message="Quantidade inválida.")])

    submitAutomaticNewOrderForm = SubmitField('Adicionar')
