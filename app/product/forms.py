from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp


class NewProductForm(FlaskForm):
    title = StringField('Título do produto?', validators=[DataRequired(), Length(min=1, max=32)])
    name = StringField('Nome do produto?', validators=[DataRequired(), Length(min=3, max=32)])
    price = DecimalField('Preço do produto?', validators=[DataRequired(), NumberRange(min=0.5, max=100.0)])
    code = StringField('Código do produto?', validators=[DataRequired(), Length(min=13, max=13)])
    submit = SubmitField('Salvar')


class SearchProductForm(FlaskForm):
    title = StringField('Título do produto?')
    code = StringField('Código do produto?')
    submit = SubmitField('Buscar')


class UpdateProductForm(FlaskForm):
    title = StringField('Título do produto?',
                        validators=[Length(min=1, max=32),
                                    Regexp('^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$')])
    name = StringField('Nome do produto?', validators=[Length(min=1, max=32), Regexp(
        '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$')])
    price = DecimalField('Preço do produto?', validators=[NumberRange(min=0.5, max=100.0)])
    code = StringField('Código do produto?', validators=[Length(min=13, max=13)])
    is_available = BooleanField("Disponível?")
    submit = SubmitField('Salvar')
