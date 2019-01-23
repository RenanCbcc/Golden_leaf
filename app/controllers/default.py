from flask import render_template, request, redirect, session, flash, url_for
from app.models.tables import Client, Clerk, Address, Product, Order, db
from app.models.forms import NewClerkForm, NewProductForm, NewClienteForm, LoginForm
from flask_login import login_user, logout_user, login_required
from app import app, login_manager


@login_manager.user_loader
def load_user(id):
    return Clerk.query.get(id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/product/list')
def listing_products():
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=products/list')
    else:
        list_of_products = Product.query.all()
        return render_template('product/list.html', products=list_of_products)


@app.route('/product/new')
def new_product():
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=new_product')
    form = NewProductForm()
    if form.validate_on_submit():
        db.session.add(Product(form.title.data,
                               form.name.data,
                               form.price.data,
                               form.code.data))

        db.session.commit()
        return redirect('product/list')
    return render_template('product/new.html', form=form)


@app.route('/product/search/<string:code>', methods=['POST'])
def search_product(code):
    product = Product.query.filter_by(code=code).first()
    if product is not None:
        list_of_products = [product]
        # TODO What this should do?
        # product=list_of_products
        return redirect('/products_list')
    else:
        flash('Nenhum produto encontrado')
        return redirect('/product/list')


@app.route('/product/<string:code>/edit', methods=['PUT'])
def edit_product(code):
    form = NewProductForm()
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect(url_for('/login', next_page=url_for('edit_product')))

    if form.validate_on_submit():
        product = Product.queryfilter_by(code=form.code.data).one()
        product.title = form.title.data
        product.name = form.name.data
        product.price = form.price.data
        product.code = form.code.data
        db.session.add(product)
        db.session.commit()
        return redirect('/product/list.html')

    product = Product.query.filter_by(code=code).first()
    return render_template('product/edit.html', form=form, product=product)


@app.route('/client/list')
def listing_clients():
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=clients_list')
    else:
        list_of_clients = Client.query.all()
        return render_template('client/list.html', clients=list_of_clients)


@app.route('/client/new', methods=['GET', 'POST'])
def new_client():
    form = NewClienteForm()
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        if form.validate_on_submit():
            db.session.add(Client(request.form['name'] + " " + request.form['surname'], request.form['phone_number'],
                                  request.form['identification'],
                                  Address(request.form['street'], request.form['number'], request.form['zip_code'])))
            db.session.commit()
            return redirect('/client/list')

        return render_template('client/new.html', form=form)
    else:
        flash('É preciso fazer login')
        return redirect('/login?next_page=new_client')


@app.route('/client/<int:id>/edit', methods=['PUT'])
def edit_client(id):
    form = NewClienteForm()
    client = Client.query.filter_by(id=id).one()
    address = Address.queryfilter_by(id=client.address_id).first()
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect(url_for('/login', next_page=url_for('/client/' + id + '/edit')))
    elif form.validate_on_submit():
        client.name = form.name.data
        client.phone_number = form.phone_number.data
        client.notifiable = form.notifiable.data
        client.status = form.status.data
        db.session.add(client)

        address.street = form.street.data
        address.number = form.number.data
        address.zip_code = form.zip_code.data
        db.session.commit()
        return redirect('/client/list')

    return render_template('client/edit.html', form=form, client=client,
                           address=address)


@app.route('/client/search', methods=['POST'])
def search_client():
    list_of_clients = Client.query.filter_by(name=request.form['name'])
    if not list_of_clients:
        flash('Nenhum cliente {} encontrado'.format(request.form['name']))
        return redirect('/clients/list.html')

    else:
        return render_template('client/list.html', clients=list_of_clients)
        # TODO I don't know if this will work.
        # return redirect('/client/list.html', clients=list_of_clients)


@app.route('/client/<int:id>/order')
def listing_orders_of(id):
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=orders_of')
    else:
        list_of_orders = Order.query.filter_by(client_id=id).all()
        return render_template('order/list.html', orders=list_of_orders)


@app.route('/client/<int:id>/order/new')
def new_order(id):
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=new_product')
    else:
        # TODO create the below template.
        return render_template('sales/new.html')


@app.route('/clerk/new', methods=['GET', 'POST'])
def new_clerk():
    form = NewClerkForm()
    if form.validate_on_submit():
        clerk = Clerk(form.name.data, form.phone_number.data, form.email.data,
                      form.cofirmed_password.data)
        db.session.add(clerk)
        db.session.commit()
        flash('Você pode fazer login agora.')
        return redirect(url_for('login'))
    return render_template('clerk/new.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    following = request.args.get('next_page')
    form = LoginForm()
    if form.validate_on_submit():
        clerk = Clerk.query.filter_by(email=form.email.data).first()
        if clerk is not None and clerk.verify_password(form.password.data):
            login_user(clerk)
            session['user_authenticated'] = request.form['email']
            flash(clerk.name + ', você foi logado com sucesso!')
            return redirect('/{}'.format(request.form['next']))
        else:
            flash('Erro, login ou senha inválidos!')
            return redirect(url_for('login'))
    return render_template('client/login.html', next_page=following, form=form)


@app.route('/logout')
def logout():
    logout_user()
    session.pop('user_authenticated', None)
    return redirect(url_for('login'))
