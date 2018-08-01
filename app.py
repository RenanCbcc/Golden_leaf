from flask import Flask, render_template, request, redirect, session,flash
from transference.products import Product
import re


app = Flask(__name__)
app.secret_key = 'JRRT'
list = [Product("Arroz", "Fazenda", 3.00, 1),
        Product("Óleo", "Primor", 3.50, 2),
        Product("Manteiga", "Tourinho", 7.00, 3),
        Product("Açúcar", "União", 2.80, 4),
        Product("Feijão", "Tio João", 6.00, 5)]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/listing')
def listing_product():
    if 'user_authenticated' not in session or session['user_authenticated'] is not None:
        return render_template('list.html', products=list)
    else:
        flash('É preciso fazer login')
        return redirect('/login?next_page=listing')


@app.route('/new_product')
def new():
    if 'user_authenticated' not in session or session['user_authenticated'] is not None:
        return render_template('new.html')
    else:
        flash('É preciso fazer login')
        return redirect('/login?next_page=new_product')


@app.route('/create_product', methods=['POST'])
def create():
    list.append(
        Product(request.form['title'],
                request.form['name'],
                request.form['price'],
                request.form['code']
                )
    )
    return redirect('/')


@app.route('/login')
def login():
    following = request.args.get('next_page')
    return render_template('login.html',next_page=following)


@app.route('/authentication',methods=['POST'])
def authenticate():
    if 'mestra' == request.form['password']:
        session['user_authenticated'] = request.form['email']
        result = re.match(r'.*@', session['user_authenticated'])
        flash(result.group() + ' logado com sucesso')
        return redirect('/{}'.format(request.form['next']))
    else:
        flash('Erro no email ou senha')
        return redirect('/login')

@app.route('/logout')
def logout():
    session['user_authenticated'] = None
    flash('Deslogado com sucesso')
    return redirect('/login')


app.run(debug=True)
