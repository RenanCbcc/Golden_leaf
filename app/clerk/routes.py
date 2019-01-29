from flask import Blueprint
from flask import render_template, request, redirect, flash, url_for
from app.clerk.forms import NewClerkForm, LoginForm
from app.models.tables import Clerk, db
from flask_login import login_user, logout_user, current_user

clerks = Blueprint('clerks', __name__)


@clerks.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        clerk = Clerk.query.filter_by(email=form.email.data).first()
        if clerk is not None and clerk.verify_password(form.password.data):
            login_user(clerk)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Erro, login ou senha inválidos!', 'error')
            return redirect(url_for('clerks.login'))
    return render_template('clerk/login.html', form=form)


@clerks.route('/logout')
def logout():
    logout_user()


@clerks.route('/clerk/new', methods=['GET', 'POST'])
def new_clerk():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = NewClerkForm()
    if form.validate_on_submit():
        clerk = Clerk(form.name.data, form.phone_number.data, form.email.data,
                      form.cofirm_password.data)
        db.session.add(clerk)
        db.session.commit()
        flash('Você pode fazer login agora.')
        return redirect(url_for('clerks.login'))
    return render_template('clerk/new.html', form=form)
