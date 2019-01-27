from flask import render_template, redirect, flash, url_for
from app.models.tables import Product, db
from app.models.forms import NewProductForm, SearchProductForm, UpdateProductForm
from flask_login import login_required
from app import app


@app.route('/product/list')
def listing_products():
    products = Product.query.all()
    return render_template('product/list.html', products=products)


@app.route('/product/create', methods=['GET', 'POST'])
@login_required
def new_product():
    form = NewProductForm()
    if form.validate_on_submit():
        db.session.add(Product(form.title.data,
                               form.name.data,
                               form.price.data,
                               form.code.data))

        db.session.commit()
        return redirect(url_for('listing_products'))
    return render_template('product/new.html', form=form)


@app.route('/product/search', methods=['GET,POST'])
def search_product():
    form = SearchProductForm()
    if form.validate_on_submit():
        products = Product.query.filter(Product.name.like(form.name.data + '%')).all()
        if not products:
            flash('Nenhum cliente {} encontrado'.format(form.name.data))
            return redirect(url_for('search_product'))
        else:
            return render_template('product/list.html', products=products)

    return render_template('client/search.html', form=form)


@app.route('/product/<string:code>/update', methods=["GET", 'POST'])
@login_required
def update_product(code):
    form = UpdateProductForm()
    product = Product.query.filter_by(code=code).one()
    if form.validate_on_submit():
        product.title = form.title.data
        product.name = form.name.data
        product.price = form.price.data
        product.code = form.code.data
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('listing_products'))

    form.title.data = product.title
    form.name.data = product.name
    form.price.data = product.price
    form.code.data = product.code
    return render_template('product/edit.html', form=form)
