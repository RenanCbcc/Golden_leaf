from flask import Flask, render_template, request, redirect, session, flash, url_for

from persistence.addressDAO import AddressDAO, PhoneDAO
from persistence.connection import Connection
from persistence.productDAO import ProductDAO
from persistence.usersDAO import ClientDAO, ClerkDAO
from transference.addresses import Address, Phone
from transference.products import Product
import re
import os

app = Flask(__name__)
app.secret_key = os.urandom(666)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/listing')
def listing_product():
    if 'user_authenticated' not in session or session['user_authenticated'] is not None:
        list_of_products = ProductDAO(Connection()).show_all()
        return render_template('products/list.html', products=list_of_products)
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


@app.route('/search_product/<string:code>', methods=['POST'])
def search_product(code):
    products = ProductDAO(Connection()).search(code)
    if products is not None:
        list_of_products = [products]
        return redirect('products/list.html', products=list_of_products)
    else:
        flash('Nenhum produto encontrado')
        return redirect('products/list.html')


@app.route('/edit_product/<string:code>')
def edit_product(code):
    product = ProductDAO(Connection()).search_code(code)
    return render_template('products/edit.html', product=product)


@app.route('/update_product', methods=['PUT'])
def update_product():
    productdao = ProductDAO(Connection())
    productdao.alter(Product(request.form['title'],
                             request.form['name'],
                             request.form['price'],
                             request.form['code']))

    return redirect('/products/list.html')


@app.route('/listing_clients')
def listing_clientes():
    if 'user_authenticated' not in session or session['user_authenticated'] is not None:
        list_of_clients = ClientDAO(Connection()).show_all()
        return render_template('users/list.html', clients=list_of_clients)
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
    list_of_clients = ClientDAO(Connection()).search_for_name(request.form['name'])
    if not list_of_clients:
        flash('Nenhum cliente {} encontrado'.format(request.form['name']))
        return redirect('/clients/list.html')

    else:
        return redirect('/clients/list.html', clients=list_of_clients)


@app.route('/login')
def login():
    following = request.args.get('next_page')
    return render_template('users/login.html', next_page=following)


@app.route('/authentication', methods=['POST'])
def authenticate():
    clerk = ClerkDAO(Connection()).login(request.form['email'])

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


@app.route('/logout/<int:id>')
def logout(id):
    clerk = ClerkDAO(Connection()).search(id)
    print(clerk)
    session[clerk.email] = None
    flash('{} deslogado com sucesso'.format(clerk.name))
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)



"""
    if 'user_authenticated' not in session or session['user_authenticated'] is not None:
        flash('É preciso fazer login')
        return redirect(url_for('users/login', next_page=url_for('edit_product')))
    else:
"""