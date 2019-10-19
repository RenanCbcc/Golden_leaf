from flask_wtf import FlaskForm
from wtforms import DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class NewPaymentForm(FlaskForm):
    value = unit_cost = DecimalField('Valor R$ ', validators=[DataRequired(), NumberRange(min=0.1, max=100.0)])
    submit = SubmitField('Pagar')
