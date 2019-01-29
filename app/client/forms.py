from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp


class NewClientForm(FlaskForm):
    name = StringField('Qual é o seu seu?', validators=[DataRequired()])
    phone_number = StringField('Número do celular?', validators=[DataRequired(), Length(min=11, max=11)])
    identification = StringField('C.P.F?', validators=[DataRequired(), Length(min=11, max=11)])
    zip_code = StringField('C.E.P?', validators=[DataRequired(), Length(min=8, max=8), Regexp('^[0-9]*$')])
    street = StringField('Nome da rua?', validators=[DataRequired()])
    address_detail = StringField('Complemento', validators=[DataRequired()])
    notifiable = BooleanField('Deseja receber notificações?')
    submit = SubmitField('Salvar')


class SearchClientForm(FlaskForm):
    name = StringField('Nome do cliente?', validators=[DataRequired(), Regexp(
        '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$',
        0,
        'Nome deve conter somente letras')])
    submit = SubmitField('Buscar')


class UpdateClientForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired()])
    phone_number = StringField('Número do celular?',
                               validators=[DataRequired(), Length(min=11, max=11), Regexp('^[0-9]*$')])
    zip_code = StringField('C.E.P?', validators=[DataRequired(), Length(min=8, max=8), Regexp('^[0-9]*$')])
    street = StringField('Nome da rua', validators=[DataRequired()])
    address_detail = StringField('Complemento', validators=[DataRequired()])
    notifiable = BooleanField('Deseja receber notificações?')
    status = BooleanField('Cliente ativo?')
    submit = SubmitField('Submit')
