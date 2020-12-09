import sqlalchemy
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, DecimalField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp, ValidationError

from Golden_Leaf.models import Category, Product, db


def enabled_categories():
    return Category.query


class NewProductForm(FlaskForm):
    category = SelectField('Categoria', coerce=int, choices=[])
    description = StringField('Descrição', validators=[Length(min=3, max=128), Regexp(
        '^([A-Za-z0-9\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s\.\-]*)$')])
    unit_cost = DecimalField('Preço', validators=[DataRequired(message="Produto precisa ter um preço."), 
                                                             NumberRange(min=0.5, max=100.0,message="Preço do produto precisa estar entre R$ 0.5 e R$ 100.00")])
    code = StringField('Código',
                       validators=[DataRequired(), Length(min=9, max=13, 
                                                          message="Código do produto precisa ter entre 9 e 13 dígitos.")])
    submit = SubmitField('Salvar')

    def validate_code(self, code):
        if Product.query.filter_by(code=code.data).first():
            raise ValidationError('Código de produto já registrado.')


class SearchProductForm(FlaskForm):
    description = StringField('Palavra chave')
    code = StringField('Código do produto')
    submit = SubmitField('Buscar')


class UpdateProductForm(FlaskForm):
    categories = QuerySelectField('Categorias',
                                  query_factory=enabled_categories, allow_blank=False,
                                  get_label='title', get_pk=lambda c: c.id,
                                  blank_text=u'Selecione uma categoria...')

    description = StringField('Descrição', validators=[Length(min=3, max=64), Regexp(
        '^([A-Za-z0-9\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s\.\-]*)$')])

    unit_cost = DecimalField('Preço', validators=[NumberRange(min=0.5, max=100.0)])
    code = StringField('Código', render_kw={'disabled': ''})
    is_available = BooleanField("Está disponível")   
    submit = SubmitField('Salvar')
