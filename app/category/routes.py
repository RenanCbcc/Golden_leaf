from app import db
from app.category import blueprint_category
from flask import render_template, redirect, url_for, request, flash, jsonify
from app.category.forms import CategoryForm
from app.models.tables import Category, Product


@blueprint_category.route("/category/list", methods=['GET'])
def listing_categories():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.order_by(Category.title).paginate(page=page, per_page=10)
    return render_template('category/list.html', categories=categories)


@blueprint_category.route("/category/new", methods=['GET', 'POST'])
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        db.session.add(Category(form.title.data))
        db.session.commit()
        return redirect(url_for('blueprint_category.listing_categories'))
    return render_template('category/new.html', form=form)


@blueprint_category.route("/category/search", methods=['GET', 'POST'])
def search_category():
    form = CategoryForm()
    if form.validate_on_submit():
        # Finding names with “form.name.data” in them:
        categories = Category.query.filter(Category.title.like('%' + form.title.data + '%')).all()
        if not categories:
            flash('Nenhum categoria {} encontrada'.format(form.title.data), 'warning')
            return redirect(url_for('blueprint_category.search_category'))
        else:
            flash('Mostrando categeria(s) encontrada(s) com nome: {}'.format(form.title.data), 'success')
            return render_template('client/list.html', categories=categories)

    return render_template('category/search.html', form=form)


@blueprint_category.route('/category/<int:id>/update', methods=['GET', 'POST'])
def update_category(id):
    form = CategoryForm()
    category = Category.query.get_or_404(id)
    if form.validate_on_submit():
        category.title = form.title.data
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('blueprint_category.listing_categories'))
    elif request.method == 'GET':
        form.title.data = category.title
    return render_template('category/edit.html', form=form)


@blueprint_category.route('/category/<int:id>/product')
def products_of(id):
    category = Category.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(category=category).order_by(Product.description).paginate(page, per_page=10)
    return render_template('category/productsof.html', category=category, all_products=products)
