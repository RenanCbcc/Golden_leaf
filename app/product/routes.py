from flask import render_template, redirect, flash, url_for, request
from app.models.tables import Product, db
from app.product.forms import NewProductForm, SearchProductForm, UpdateProductForm
from flask_login import login_required
from app.product import blueprint_products


@blueprint_products.route('/products/list')
def listing_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.title, Product.name).paginate(page=page, per_page=10)
    return render_template('product/list.html', products=products)


@blueprint_products.route('/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    form = NewProductForm()
    if form.validate_on_submit():
        db.session.add(Product(form.title.data,
                               form.name.data,
                               form.price.data,
                               form.code.data))

        db.session.commit()
        return redirect(url_for('blueprint_products.listing_products'))
    return render_template('product/new.html', form=form)


@blueprint_products.route('/products/search', methods=["GET", 'POST'])
def search_product():
    form = SearchProductForm()
    if form.validate_on_submit():
        products = Product.query.filter(Product.title.like('%' + form.title.data + '%')).all()
        if not products:
            flash('Produto algum encontrado', 'warning')
            return redirect(url_for('blueprint_products.search_product'))
        else:
            flash('Mostrando todos os produtos com "{}" encontrados'.format(form.title.data), 'success')
            return render_template('product/list.html', products=products)

    return render_template('product/search.html', form=form)


@blueprint_products.route('/products/<string:code>/update', methods=["GET", 'POST'])
@login_required
def update_product(code):
    form = UpdateProductForm()
    product = Product.query.filter_by(code=code).one()
    if form.validate_on_submit():
        product.title = form.title.data
        product.name = form.name.data
        product.price = form.price.data
        product.code = form.code.data
        product.is_available = form.is_available.data
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('blueprint_products.listing_products'))

    form.title.data = product.title
    form.name.data = product.name
    form.price.data = product.price
    form.code.data = product.code
    form.is_available.data = product.is_available
    return render_template('product/edit.html', form=form)
