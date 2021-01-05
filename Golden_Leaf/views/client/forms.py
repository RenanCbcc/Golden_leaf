from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Regexp


class NewClientForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(message="Cliente precisa ter um nome."), Length(min=6, max=64,message="O nome precisa ter entre 6 e 64 caracteres."),Regexp('^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$',0,
        'Nome deve conter somente letras')])
    phone_number = StringField('Telefone',validators=[DataRequired(message="Cliente precisa ter um número de telefone celular."),
                                                      Regexp('[1-9]{2}[1-9]{4,5}[0-9]{4}',0,'O número deve deve estar no formato: (xx)xxxxx-xxxx.'),
                                                      Length(min=11, max=11,message="O número precisa ter exatamente 11 caracteres.")])
    
    street = StringField('Endereço', validators=[DataRequired(message="O cliente precisa ter um endereço"),Length(min=6, max=64,message="O endereço precisa ter entre 6 e 64 caracteres.")])
    notifiable = BooleanField('Deseja receber notificações?')
    submit = SubmitField('Salvar')


class SearchClientForm(FlaskForm):
    name = StringField('Nome', validators=[DataRequired(message="Cliente precisa ter um nome."), Regexp('^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$',
        0,
        'Nome deve conter somente letras')])
    submit = SubmitField('Buscar')


class UpdateClientForm(FlaskForm):
    name = StringField('Nome', render_kw={'disabled': ''})
    identification = StringField('Identidade', render_kw={'disabled': ''})
    phone_number = StringField('Telefone',validators=[DataRequired(message="Cliente precisa ter um número de telefone celular."),
                                                      Regexp('[1-9]{2}[1-9]{4,5}[0-9]{4}',0,'O número deve deve estar no formato: (xx)xxxxx-xxxx.'),
                                                      Length(min=11, max=11,message="O número precisa ter exatamente 11 caracteres.")])
    street = StringField('Endereço', validators=[DataRequired(message="O cliente precisa ter um endereço")])
    notifiable = BooleanField('Deseja receber notificações?')
    status = BooleanField('Cliente ativo?')
    submit = SubmitField('Salvar')
