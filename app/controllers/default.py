from flask import render_template, request, redirect, session, flash, url_for
from app.models.tables import Client, Clerk, Address, Product, Order, db
from app import app
import re


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products_list')
def listing_products():
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=products_list')
    else:
        list_of_products = Product.query.all()
        return render_template('product/list.html', products=list_of_products)


@app.route('/product_new')
def new_product():
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=new_product')
    else:
        return render_template('product/new.html')


@app.route('/product_create', methods=['POST'])
def create_product():
    db.session.add(Product(request.form['title'],
                           request.form['name'],
                           request.form['price'],
                           request.form['code']))

    db.session.commit()
    return redirect('/')


@app.route('/product_search/<string:code>', methods=['POST'])
def search_product(code):
    product = Product.query.filter_by(code=code).first()
    if product is not None:
        list_of_products = [product]
        # TODO What this should do?
        # product=list_of_products
        return redirect('/products_list')
    else:
        flash('Nenhum produto encontrado')
        return redirect('/products_list')


@app.route('/product_edit/<string:code>', methods=['PUT'])
def edit_product(code):
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect(url_for('/login', next_page=url_for('product_edit')))
    else:
        product = Product.query.filter_by(code=code).first()
        if product is not None:
            return render_template('product/edit.html', product=product)


@app.route('/product_update', methods=['PUT'])
def update_product():
    product = Product.queryfilter_by(code=request.form['code']).one()
    product.title = request.form['title']
    product.name = request.form['name']
    product.price = request.form['price']
    product.code = request.form['code']
    db.session.add(product)
    db.session.commit()
    return redirect('/product/list.html')


@app.route('/clients_list')
def listing_clients():
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=clients_list')
    else:
        list_of_clients = Client.query.all()
        return render_template('client/list.html', clients=list_of_clients)


@app.route('/client_new')
def new_client():
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        return render_template('client/new.html')
    else:
        flash('É preciso fazer login')
        return redirect('/login?next_page=new_product')


@app.route('/clerk_new')
def new_clerk():
    return render_template('clerk/new.html')


@app.route('/clerk_create', methods=['POST'])
def create_clerk():
    db.session.add(Clerk(request.form['name'] + " " + request.form['surname'], request.form['phone_number'],
                         request.form['email'], request.form['password']))
    db.session.commit()
    return redirect('/clerk/list.html')


@app.route('/client_create', methods=['POST'])
def create_client():
    db.session.add(Client(request.form['name'] + " " + request.form['surname'], request.form['phone_number'],
                          request.form['identification'],
                          Address(request.form['street'], request.form['number'], request.form['zip_code'])))
    db.session.commit()
    return redirect('/client/list.html')


@app.route('/client_edit/<int:id>')
def edit_client(id):
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect(url_for('/login', next_page=url_for('client_edit')))
    else:
        client = Client.query.filter_by(id=id).one()
        address = Address.queryfilter_by(id=client.address_id).first()
        return render_template('client/edit.html', client=client,
                               address=address)


@app.route('/client_update/<int:id>', methods=['PUT'])
def update_client(id):
    client = Client.query.filter_by(id=id).one()
    client.name = request.form['name']
    client.phone_number = request.form['phone']
    client.notifiable = request.form['notifiable']
    client.status = request.form['status']
    db.session.add(client)

    address = Address.queryfilter_by(id=client.address_id)
    address.street = request.form['street']
    address.number = request.form['number']
    address.zip_code = request.form['zip_code']
    db.session.commit()
    return redirect('/clients/list.html')


@app.route('/search_client', methods=['POST'])
def search_client():
    list_of_clients = Client.query.filter_by(name=request.form['name'])
    if not list_of_clients:
        flash('Nenhum cliente {} encontrado'.format(request.form['name']))
        return redirect('/clients/list.html')

    else:
        return render_template('client/list.html', clients=list_of_clients)
        # TODO I don't know if this will work.
        # return redirect('/client/list.html', clients=list_of_clients)


@app.route('/orders_of/<int:id>')
def listing_orders_of(id):
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=orders_of')
    else:
        list_of_orders = Order.query.filter_by(client_id=id).all()
        return render_template('order/list.html', orders=list_of_orders)


@app.route('/order_new')
def new_order():
    if 'user_authenticated' not in session or session['user_authenticated'] is None:
        flash('É preciso fazer login')
        return redirect('/login?next_page=new_product')
    else:
        # TODO create the below template.
        return render_template('sales/new.html')


@app.route('/login')
def login():
    following = request.args.get('next_page')
    return render_template('client/login.html', next_page=following)


@app.route('/authentication', methods=['POST'])
def authenticate():
    clerk = Clerk.query.filter_by(email=request.form['email']).one()
    if clerk is None:
        flash('Erro, atendente não encontrado.')
        return redirect('/login')
    elif request.form['password'] == clerk.password:
        session['user_authenticated'] = request.form['email']
        result = re.match(r'.*@', session['user_authenticated'])
        flash(result.group() + ' logado com sucesso')
        return redirect('/{}'.format(request.form['next']))
    else:
        flash('Erro, senha incorreta.')
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user_authenticated', None)
    return redirect('/login')


