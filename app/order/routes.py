from flask_login import login_required
from app.models.tables import Order, Client, Category, Product
from flask import render_template, redirect, url_for, request, flash
from app.order import blueprint_order
from app.order.forms import SearchOrderForm, NewOrderForm


@blueprint_order.route('/client/orders', defaults={'id': None}, methods=["GET", 'POST'])
@blueprint_order.route('/client/<int:id>/orders', methods=["GET", 'POST'])
@login_required
def listing_orders_of(id):
    page = request.args.get('page', 1, type=int)
    if id is not None:
        orders = Order.query.filter_by(client_id=id).order_by(Order.date.desc()).paginate(page=page, per_page=10)
        return render_template('order/list.html', orders=orders)
    else:
        orders = Order.query.order_by(Order.date.desc()).paginate(page=page, per_page=10)
        return render_template('order/list.html', orders=orders)


@blueprint_order.route('/order/new', defaults={'id': None}, methods=["GET", 'POST'])
@blueprint_order.route('/client/<int:id>/order/new', methods=["GET", 'POST'])
@login_required
def new_order(id):
    form = NewOrderForm()
    categories = Category.query.order_by(Category.title)
    form.category.choices = [(category.id, category.title) for category in categories.all()]
    form.product.choices = [(product.id, product.description) for product in
                            Product.query.filter_by(is_available=True, category_id=form.category.choices[0][0]).all()]


    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Produto invalido', 'warning')
            # return redirect(url_for('blueprint_order.new_order'))

    return render_template('order/new.html', form=form)


@blueprint_order.route('/order/<int:id>/update', methods=["GET", 'POST'])
def update_order(id):
    return '<html><h1>TODO</h1><html>'


@blueprint_order.route('/order/search', methods=["GET", 'POST'])
def search_order():
    form = SearchOrderForm(Client.query.order_by(Client.name).all())
    if form.validate_on_submit():
        pass
    else:
        pass

    return render_template("order/search.html", form=form)
