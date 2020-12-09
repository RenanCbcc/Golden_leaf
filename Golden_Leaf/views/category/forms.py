from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Regexp


class CategoryForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Regexp(
        '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s\/\-\.]*)$',
        0,
        'O nome da categoria deve conter somente letras')])
    submit = SubmitField('Salvar')


class SearchCategoryForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Regexp(
        '^([A-Za-z\u00C0-\u00D6\u00D8-\u00f6\u00f8-\u00ff\s\/\-\.]*)$',
        0,
        'O nome da categoria deve conter somente letras')])
    submit = SubmitField('Buscar')
