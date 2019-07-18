import os
import secrets

from PIL import Image
from flask import render_template, redirect, flash, url_for, request, jsonify, current_app
from app.models.tables import Product, db, Category
from app.product import blueprint_product
from app.product.forms import NewProductForm, SearchProductForm, UpdateProductForm
from flask_login import login_required


@blueprint_product.route('/product/list', methods=['GET'])
def listing_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.description).paginate(page=page, per_page=10)
    return render_template('product/list.html', all_products=products)


@blueprint_product.route('/product/available/list', methods=['GET'])
def available_products():
    page = request.args.get('page', 1, type=int)
    products = Product.query.filter_by(is_available=False).order_by(Product.description).paginate(
        page=page, per_page=10)
    return render_template('product/list.html', all_products=products)


@blueprint_product.route('/product/create', methods=['GET', 'POST'])
@login_required
def new_product():
    form = NewProductForm()
    form.category.choices = [(category.id, category.title) for category in
                             Category.query.order_by(Category.title).all()]

    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).one()
        db.session.add(Product(category, form.brand.data,
                               form.description.data,
                               form.unit_cost.data,
                               form.code.data))

        db.session.commit()
        return redirect(url_for('blueprint_product.listing_products'))
    return render_template('product/new.html', form=form)


@blueprint_product.route('/product/search', methods=["GET", 'POST'])
def search_product():
    form = SearchProductForm()
    if form.validate_on_submit():
        products = Product.query.filter(Product.brand.like('%' + form.brand.data + '%')).all()
        if not products:
            flash('Produto algum encontrado', 'warning')
            return redirect(url_for('blueprint_product.search_product'))
        else:
            flash('Mostrando todos os produtos com "{}" encontrados'.format(form.brand.data), 'success')
            return render_template('product/list.html', products=products)

    return render_template('product/search.html', form=form)


@blueprint_product.route('/product/<string:code>/update', methods=["GET", 'POST'])
@login_required
def update_product(code):
    form = UpdateProductForm()
    product = Product.query.filter_by(code=code).one()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            product.image_file = picture_file
            print(picture_file)
        product.brand = form.brand.data
        product.description = form.description.data
        product.unit_cost = form.unit_cost.data
        product.code = form.code.data
        product.is_available = form.is_available.data
        db.session.add(product)
        db.session.commit()
        flash('Categoria atualizada com sucesso.', 'success')
        return redirect(url_for('blueprint_product.update_product', code=product.code))
    elif request.method == 'GET':
        form.brand.data = product.brand
        form.description.data = product.description
        form.unit_cost.data = product.unit_cost
        form.code.data = product.code
        form.is_available.data = product.is_available
    image_file = url_for('static', filename='product_pic/' + product.image_file)
    return render_template('product/edit.html', form=form, image_file=image_file)


@blueprint_product.route('/product/category/<id>')
def product(id):
    products = Product.query.filter_by(category_id=id).all()
    response = jsonify({'products': [
        {'id': product.id, 'description': product.description, 'unit_cost': str(product.unit_cost)} for product in
        products]})
    return response


@blueprint_product.route('/product/unit_cost/<id>')
def product_cost(id):
    product = Product.query.filter_by(id=id).one()
    response = jsonify({'id': product.id, 'unit_cost': str(product.unit_cost)})
    return response


def save_picture(form_picture):
    random_hex = secrets.token_hex(16)
    # I do not want the file file name, so I use _ instead
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/product_pic', picture_filename)

    output_size = (320, 320)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    # Saves the picture in file system
    image.save(picture_path)
    return picture_filename
