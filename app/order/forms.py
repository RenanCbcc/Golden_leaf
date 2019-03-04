from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, DecimalField
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
    client = StringField("Cliente", render_kw={'disabled': ''})
    category = SelectField('Categorias', coerce=int, choices=[])
    product = SelectField('Produtos', coerce=int, choices=[])
    quantity = DecimalField("Quantidade", validators=[DataRequired(), NumberRange(min=0.01, max=100.0)])
    status = SelectField("Status", choices=[('pg', 'PAGO'), ('pd', 'PENDENTE')])
    submit = SubmitField('Salvar')
