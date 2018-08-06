from flask import Flask, render_template, request, redirect, session, flash

from persistence.addressDAO import AddressDAO, PhoneDAO
from persistence.connection import Connection
from persistence.productDAO import ProductDAO
from persistence.usersDAO import ClientDAO, ClerkDAO
from transference.address import Address, Phone
from transference.products import Product
import re

app = Flask(__name__)
app.run()
app.secret_key = 'JRRT'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/listing')
def listing_product():
    if 'user_authenticated' not in session or session['user_authenticated'] is not None:
        productdao = ProductDAO(Connection())
        list = productdao.show_all()
        return render_template('products/list.html', products=list)
    else:
        flash('É preciso fazer login')
        return redirect('/login?next_page=listing')


@app.route('/new_product')
def new_product():
    if 'user_authenticated' not in session or session['user_authenticated'] is not None:
        return render_template('products/new.html')
    else:
        flash('É preciso fazer login')
        return redirect('/login?next_page=new_product')


@app.route('/create_product', methods=['POST'])
def create_product():
    productdao = ProductDAO(Connection())
    productdao.save(Product(request.form['title'],
                            request.form['name'],
                            request.form['price'],
                            request.form['code']))

    return redirect('/')


@app.route('/search_product', methods=['POST'])
def search_product():
    productdao = ProductDAO(Connection())
    product = productdao.search(request.form['code'])
    if product is not None:
        list = [product]
        return redirect('products/list.html', products=list)
    else:
        flash('Nenhum produto encontrado')
        return redirect('/products/list.html')


@app.route('/listing_clientes')
def listing_clientes():
    if 'user_authenticated' not in session or session['user_authenticated'] is not None:
        clientdao = ClientDAO(Connection())
        list = clientdao.show_all()
        return render_template('users/list.html', products=list)
    else:
        flash('É preciso fazer login')
        return redirect('/login?next_page=listing')


@app.route('/new_client')
def new_client():
    if 'user_authenticated' not in session or session['user_authenticated'] is not None:
        return render_template('users/new.html')
    else:
        flash('É preciso fazer login')
        return redirect('/login?next_page=new_product')


@app.route('/create_client', methods=['POST'])
def create_client():
    connection = Connection()
    clientdao = ClientDAO(connection)
    addressdao = AddressDAO(connection)
    phonedao = PhoneDAO(connection)
    client = clientdao.save(Product(request.form['name'],
                                    request.form['surname'],
                                    request.form['identification']))

    addressdao.save(Address(client.id, client.identification, request.form['zip_code']))
    phonedao.save(Phone(client.identification, request.form['phone_number']))
    return redirect('/users/list.html')


@app.route('/search_client', methods=['POST'])
def search_client():
    cliendao = ClientDAO(Connection())
    list = cliendao.search_for_name(request.form['name'])
    if not list:
        flash('Nenhum cliente {} encontrado'.format(request.form['name']))
        return redirect('/clients/list.html')

    else:
        return redirect('/clients/list.html', products=list)


@app.route('/login')
def login():
    following = request.args.get('next_page')
    return render_template('users/login.html', next_page=following)


@app.route('/authentication', methods=['POST'])
def authenticate():
    clerkdao = ClerkDAO(Connection())
    clerk = clerkdao.login(request.form['email'])
    if clerk is None:
        flash('Erro, atendente não encontrado.')
        return redirect('/login')
    elif request.form['password'] == clerk.password:
        session[clerk.name] = request.form['email']
        result = re.match(r'.*@', session[clerk.name])
        flash(result.group() + ' logado com sucesso')
        return redirect('/{}'.format(request.form['next']))
    else:
        flash('Erro, senha incorreta.')
        return redirect('/login')


@app.route('/logout')
def logout():
    session['user_authenticated'] = None
    flash('Deslogado com sucesso')
    return redirect('/login')
