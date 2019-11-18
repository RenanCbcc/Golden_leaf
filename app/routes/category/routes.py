from flask import render_template, redirect, url_for, request, flash
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required

from app import db
from app.routes.category import blueprint_category
from app.routes.category.forms import CategoryForm, SearchCategoryForm
from app.models import Category, Product
from app.routes.product.forms import NewProductForm


def view_category_dlc(*args, **kwargs):
    id = request.view_args['id']
    c = Category.query.get(id)
    return [{'text': c.title}]


@blueprint_category.route("/category", methods=['GET'])
@register_breadcrumb(blueprint_category, '.', 'Categorias')
def get_categories():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.order_by(Category.title).paginate(page=page, per_page=10)
    return render_template('category/list.html', categories=categories)


@blueprint_category.route("/category/new", methods=['GET', 'POST'])
@register_breadcrumb(blueprint_category, '.new_category', 'Nova Categoria')
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        db.session.add(Category(form.title.data))
        db.session.commit()
        flash(form.title.data + ' inserido com sucesso!', 'success')
        return redirect(url_for('blueprint_category.get_categories'))
    return render_template('category/new.html', form=form)


@blueprint_category.route("/category/search", methods=['GET', 'POST'])
@register_breadcrumb(blueprint_category, '.search_category', 'Busca de Categoria')
def search_category():
    page = request.args.get('page', 1, type=int)
    form = SearchCategoryForm()
    if form.validate_on_submit():
        # Finding names with “form.name.data” in them:
        categories = Category.query.filter(Category.title.like('%' + form.title.data + '%')) \
            .paginate(page=page, per_page=10)
        if not categories:
            flash('Nenhum categoria {} encontrada'.format(form.title.data), 'warning')
            return redirect(url_for('blueprint_category.search_category'))
        else:
            flash('Mostrando categeria(s) encontrada(s) com nome: {}'.format(form.title.data), 'info')
            return render_template('category/list.html', categories=categories)

    return render_template('category/search.html', form=form)


@blueprint_category.route('/category/<int:id>/update', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_category, '.id', '.update_category', dynamic_list_constructor=view_category_dlc)
@login_required
def update_category(id):
    form = CategoryForm()
    category = Category.query.get_or_404(id)
    if form.validate_on_submit():
        category.title = form.title.data
        db.session.add(category)
        db.session.commit()
        flash('Categoria alterada com sucesso!', 'success')
        return redirect(url_for('blueprint_category.get_categories'))
    elif request.method == 'GET':
        form.title.data = category.title
    return render_template('category/edit.html', form=form)


@blueprint_category.route('/category/<int:id>/product')
@register_breadcrumb(blueprint_category, '.id', '', dynamic_list_constructor=view_category_dlc)
def products_of(id):
    category = Category.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(category=category).order_by(Product.description).paginate(page, per_page=10)
    return render_template('category/productsof.html', category=category, all_products=products)


@blueprint_category.route('/category/<int:id>/product/new', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_category, '.id', '', dynamic_list_constructor=view_category_dlc)
@login_required
def new_product(id):
    form = NewProductForm()
    category = Category.query.filter_by(id=id).one()
    form.category.choices = [(category.id, category.title)]

    if form.validate_on_submit():
        db.session.add(Product(category, form.brand.data,
                               form.description.data,
                               form.unit_cost.data,
                               form.code.data))

        db.session.commit()
        flash(form.description.data + ' inserido com sucesso!', 'success')
        return redirect(url_for('blueprint_category.products_of', id=category.id))
    return render_template('product/new.html', form=form)
