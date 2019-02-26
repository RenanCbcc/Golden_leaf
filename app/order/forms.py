from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, DateField, SelectField, DecimalField
from wtforms.validators import DataRequired, NumberRange


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


class NewOrderForm(FlaskForm):
    client = StringField("Cliente")
    clerk = StringField("Atendente")
    category = SelectField("Categoria")
    title = StringField("Produto")
    name = StringField("Nome")
    quantity = DecimalField("Quantidade", validators=[DataRequired(), NumberRange(min=0.01, max=100.0)])
    status = SelectField("Status", choices=['Pago', 'Pendente'])
    date = DateField("Data")
    submit = SubmitField('Salvar')
