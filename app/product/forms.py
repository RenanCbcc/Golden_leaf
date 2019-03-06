from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, DecimalField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp


class NewProductForm(FlaskForm):
    category = SelectField('Escolha a categoria', coerce=int, choices=[])
    brand = StringField('Marca do produto?', validators=[Length(min=3, max=32),
                                                         Regexp(
                                                             '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$')])
    description = StringField('Descrição do produto?', validators=[Length(min=3, max=64), Regexp(
        '^([A-Za-z0-9\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s\.\-]*)$')])
    price = DecimalField('Preço do produto?', validators=[DataRequired(), NumberRange(min=0.5, max=100.0)])
    code = StringField('Código do produto?', validators=[DataRequired(), Length(min=13, max=13)])
    submit = SubmitField('Salvar')


class SearchProductForm(FlaskForm):
    brand = StringField('Marca do produto?')
    code = StringField('Código do produto?')
    submit = SubmitField('Buscar')


class UpdateProductForm(FlaskForm):
    brand = StringField('Marca do produto?', validators=[Length(min=3, max=32),
                                                         Regexp(
                                                             '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s]*)$')])
    description = StringField('Descrição do produto?', validators=[Length(min=3, max=64), Regexp(
        '^([A-Za-z0-9\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s\.\-]*)$')])

    price = DecimalField('Preço do produto?', validators=[NumberRange(min=0.5, max=100.0)])
    code = StringField('Código do produto?', validators=[Length(min=13, max=13)])
    is_available = BooleanField("Disponível?")
    picture = FileField('Foto de produto', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Salvar')
