from flask import render_template, redirect, flash, url_for, request, jsonify
from app.models.tables import Product, db, Category
from app.product import blueprint_products
from app.product.forms import NewProductForm, SearchProductForm, UpdateProductForm
from flask_login import login_required


@blueprint_products.route('/product/list', methods=['GET'])
def listing_products():
    page = request.args.get('page', 1, type=int)
    # products = Product.query.order_by(Product.brand, Product.description).paginate(page=page, per_page=10)
    # Avoiding the N+1 problem by querying first the category
    # TODO function is showing categories without products
    all_products_by_category = Category.query.order_by(Category.title).paginate(page=page, per_page=10)
    return render_template('product/list.html', all_products=all_products_by_category)


@blueprint_products.route('/product/create', methods=['GET', 'POST'])
@login_required
def create_product():
    form = NewProductForm()
    form.category.choices = [(category.id, category.title) for category in
                             Category.query.order_by(Category.title).all()]

    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).one()
        db.session.add(Product(category, form.brand.data,
                               form.descriptio.data,
                               form.price.data,
                               form.code.data))

        db.session.commit()
        return redirect(url_for('blueprint_products.listing_products'))
    return render_template('product/new.html', form=form)


@blueprint_products.route('/product/search', methods=["GET", 'POST'])
def search_product():
    form = SearchProductForm()
    if form.validate_on_submit():
        products = Product.query.filter(Product.brand.like('%' + form.brand.data + '%')).all()
        if not products:
            flash('Produto algum encontrado', 'warning')
            return redirect(url_for('blueprint_products.search_product'))
        else:
            flash('Mostrando todos os produtos com "{}" encontrados'.format(form.brand.data), 'success')
            return render_template('product/list.html', products=products)

    return render_template('product/search.html', form=form)


@blueprint_products.route('/product/<string:code>/update', methods=["GET", 'POST'])
@login_required
def update_product(code):
    form = UpdateProductForm()
    product = Product.query.filter_by(code=code).one()
    if form.validate_on_submit():
        product.brand = form.brand.data
        product.descriptio = form.descriptio.data
        product.price = form.price.data
        product.code = form.code.data
        product.is_available = form.is_available.data
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('blueprint_products.listing_products'))

    form.brand.data = product.brand
    form.descriptio.data = product.description
    form.price.data = product.price
    form.code.data = product.code
    form.is_available.data = product.is_available
    return render_template('product/edit.html', form=form)


@blueprint_products.route('/product/category/<id>')
def product(id):
    products = Product.query.filter_by(category_id=id).all()
    print(products)
    response = jsonify({'products': [{'id': product.id, 'description': product.description} for product in products]})
    return response
