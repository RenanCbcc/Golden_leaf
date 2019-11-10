from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError

from app.models import Clerk


class LoginForm(FlaskForm):
    email = StringField('Login', validators=[DataRequired('Por favos, entre com o seu endereço de email.'),
                                             Email('Este campo requer um endereçode email válido.')])
    password = PasswordField(label='Senha', validators=[Length(min=8, max=32)])
    submit = SubmitField('Entrar')


class UpdateClerkForm(FlaskForm):
    email = StringField('Email', validators=[Email()])
    picture = FileField('Atualizar foto de perfil', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Salvar')

    def validate_email(self, email):
        if email.data != current_user.email:
            clerk = Clerk.query.filter_by(email=email.data).first()
            if clerk:
                raise ValidationError("Este endereço de email já está regitrado!")


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
                             validators=[Length(min=8, max=32),
                                         EqualTo('cofirm_password', message='Senhas não conferem!')])
    cofirm_password = PasswordField(label='Confirme sua senha', validators=[DataRequired()])

    submit = SubmitField('Registrar')


    def validate_email(self, email):
        if Clerk.query.filter_by(email=email.data).first():
            raise ValidationError('Este email já está registrado!')



class RequestResetForm(FlaskForm):
    email = StringField('Seu endereço de email?', validators=[DataRequired(), Email()])
    submit = SubmitField('Requisitar redefinição de senha')

    def validate_email(self, email):
        clerk = Clerk.query.filter_by(email=email.data).first()
        if clerk is None:
            raise ValidationError("Não há atendente com este email. Registre-se")


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Escolha uma senha',
                             validators=[Length(min=8, max=32)])
    cofirm_password = PasswordField(label='Confirme sua senha', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Redefinir senha')
