from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DecimalField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange


class LoginForm(FlaskForm):
    email = StringField('Login', validators=[DataRequired(), Email()])
    password = PasswordField(label='Senha', validators=[Length(min=5, max=70)])
    submit = SubmitField('Entrar')


class NewClerkForm(FlaskForm):
    name = StringField('Qual é o seu nome?', validators=[DataRequired()])
    phone_number = StringField('Qual é o número do ceu celular?', validators=[DataRequired()])
    email = StringField('Seu endereço de email?', validators=[DataRequired(), Email()])
    password = PasswordField(label='Escolha uma senha', validators=[Length(min=8, max=32)])
    cofirmed_password = PasswordField(label='Confirme uma senha', validators=[EqualTo(password)])

    submit = SubmitField('Submit')


class NewClienteForm(FlaskForm):
    client_name = StringField('Qual é o seu seu?', validators=[DataRequired()])
    client_cpf = StringField('C.P.F?', validators=[DataRequired()])
    client_zip_code = StringField('C.E.P?', validators=[DataRequired()])
    address_street = StringField('Nome da rua?', validators=[DataRequired()])
    address_detail = StringField('Complemento', validators=[DataRequired()])
    client_phone_number = StringField('Número do celular?', validators=[DataRequired()])
    notifications = BooleanField('Deseja receber notificações?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewProductForm(FlaskForm):
    title = StringField('Título do produto?', validators=[DataRequired()])
    name = StringField('Nome do produto?', validators=[DataRequired()])
    price = DecimalField('Preço do produto?', validators=[DataRequired(), NumberRange(min=0.5, max=100.0)])
    code = DecimalField('Código do produto?', validators=[DataRequired()])
    submit = SubmitField('Submit')
