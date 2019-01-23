from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DecimalField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Regexp


class LoginForm(FlaskForm):
    email = StringField('Login', validators=[DataRequired(), Email()])
    password = PasswordField(label='Senha', validators=[Length(min=8, max=32)])
    submit = SubmitField('Entrar')


class NewClerkForm(FlaskForm):
    # TODO Verify the Regex
    name = StringField('Qual é o seu nome?', validators=[DataRequired(), Length(min=10, max=64),
                                                         Regexp('^[A-Za-z]', 0,
                                                                'Usernames must have only letters')])

    phone_number = StringField('Qual é o número do ceu celular?', validators=[DataRequired()])
    email = StringField('Seu endereço de email?', validators=[DataRequired(), Email()])
    password = PasswordField(label='Escolha uma senha',
                             validators=[Length(min=8, max=32), EqualTo('cofirmed_password')])
    cofirmed_password = PasswordField(label='Confirme uma senha', validators=[DataRequired()])

    submit = SubmitField('Register')


class NewClienteForm(FlaskForm):
    name = StringField('Qual é o seu seu?', validators=[DataRequired()])
    cpf = StringField('C.P.F?', validators=[DataRequired()])
    zip_code = StringField('C.E.P?', validators=[DataRequired()])
    street = StringField('Nome da rua?', validators=[DataRequired()])
    number = StringField('Número da residência?', validators=[DataRequired()])
    address_detail = StringField('Complemento', validators=[DataRequired()])
    phone_number = StringField('Número do celular?', validators=[DataRequired()])
    notifiable = BooleanField('Deseja receber notificações?', validators=[DataRequired()])
    status = BooleanField('Cliente ativo?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewProductForm(FlaskForm):
    title = StringField('Título do produto?', validators=[DataRequired()])
    name = StringField('Nome do produto?', validators=[DataRequired()])
    price = DecimalField('Preço do produto?', validators=[DataRequired(), NumberRange(min=0.5, max=100.0)])
    code = DecimalField('Código do produto?', validators=[DataRequired()])
    submit = SubmitField('Salvar')
