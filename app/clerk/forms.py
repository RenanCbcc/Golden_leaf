from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DecimalField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Regexp

class LoginForm(FlaskForm):
    email = StringField('Login', validators=[DataRequired(), Email()])
    password = PasswordField(label='Senha', validators=[Length(min=8, max=32)])
    submit = SubmitField('Entrar')


class NewClerkForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired(), Length(min=10, max=64),
                                                         Regexp(
                                                             '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$',
                                                             0,
                                                             'Usernames must have only letters')])

    phone_number = StringField('Número do celular?',
                               validators=[DataRequired(), Length(min=11, max=11), Regexp('^[0-9]*$')])
    email = StringField('Seu endereço de email?', validators=[DataRequired(), Email()])
    password = PasswordField(label='Escolha uma senha',
                             validators=[Length(min=8, max=32)])
    cofirm_password = PasswordField(label='Confirme sua senha', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Registrar')
