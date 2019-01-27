from flask_wtf import FlaskForm
from reportlab.pdfbase.pdfform import ButtonField
from wtforms import StringField, SubmitField, PasswordField, BooleanField, DecimalField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Regexp


class LoginForm(FlaskForm):
    email = StringField('Login', validators=[DataRequired(), Email()])
    password = PasswordField(label='Senha', validators=[Length(min=8, max=32)])
    submit = SubmitField('Entrar')


class NewClerkForm(FlaskForm):
    # TODO Verify the Regex
    name = StringField('Qual é o seu nome?', validators=[DataRequired(), Length(min=10, max=64),
                                                         Regexp(
                                                             '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$',
                                                             0,
                                                             'Usernames must have only letters')])

    phone_number = StringField('Qual é o número do ceu celular?', validators=[DataRequired()])
    email = StringField('Seu endereço de email?', validators=[DataRequired(), Email()])
    password = PasswordField(label='Escolha uma senha',
                             validators=[Length(min=8, max=32)])
    cofirm_password = PasswordField(label='Confirme sua senha', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Registrar')


class NewClienteForm(FlaskForm):
    name = StringField('Qual é o seu seu?', validators=[DataRequired()])
    identification = StringField('C.P.F?', validators=[DataRequired(), Length(min=11, max=11)])
    zip_code = StringField('C.E.P?', validators=[DataRequired()])
    street = StringField('Nome da rua?', validators=[DataRequired()])
    number = StringField('Número da residência?', validators=[DataRequired()])
    address_detail = StringField('Complemento', validators=[DataRequired()])
    phone_number = StringField('Número do celular?', validators=[DataRequired()])
    notifiable = BooleanField('Deseja receber notificações?', validators=[DataRequired()])
    status = BooleanField('Cliente ativo?', validators=[DataRequired()])
    submit = SubmitField('Submit')


class NewProductForm(FlaskForm):
    title = StringField('Título do produto?', validators=[DataRequired(), Length(min=1, max=32)])
    name = StringField('Nome do produto?', validators=[DataRequired(), Length(min=1, max=32)])
    price = DecimalField('Preço do produto?', validators=[DataRequired(), NumberRange(min=0.5, max=100.0)])
    code = StringField('Código do produto?', validators=[DataRequired(), Length(min=13, max=13)])
    submit = SubmitField('Salvar')


class SearchProductForm(FlaskForm):
    title = StringField('Título do produto?')
    name = StringField('Nome do produto?')
    code = DecimalField('Código do produto?')
    submit = SubmitField('Buscar')


class SearchClientForm(FlaskForm):
    name = StringField('Nome do produto?', validators=[DataRequired()])
    submit = SubmitField('Buscar')


class SearchOrderForm(FlaskForm):
    client = StringField('Nome do cliente?')
    clerk = StringField('Preço do nome do atendente?')
    submit = SubmitField('Buscar')


class UpdateProductForm(FlaskForm):
    title = StringField('Título do produto?',
                        validators=[DataRequired(), Length(min=1, max=32),
                                    Regexp('^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$')])
    name = StringField('Nome do produto?', validators=[DataRequired(), Length(min=1, max=32), Regexp(
        '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$')])
    price = DecimalField('Preço do produto?', validators=[DataRequired(), NumberRange(min=0.5, max=100.0)])
    code = StringField('Código do produto?', validators=[DataRequired(), Length(min=13, max=13)])
    submit = SubmitField('Salvar')
