from flask import render_template, request, redirect, flash, url_for
from app.models.tables import Clerk
from app.models.forms import LoginForm
from flask_login import login_user, logout_user, current_user
from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        clerk = Clerk.query.filter_by(email=form.email.data).first()
        if clerk is not None and clerk.verify_password(form.password.data):
            login_user(clerk)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Erro, login ou senha inválidos!','error')
            return redirect(url_for('login'))
    return render_template('clerk/login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
