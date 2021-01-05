import os
import secrets
from PIL import Image
from flask import current_app
from flask import render_template, request, redirect, flash, url_for
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_user, logout_user, current_user
from flask_mail import Message

from Golden_Leaf import mail
from Golden_Leaf.views.clerk import blueprint_clerk
from Golden_Leaf.views.clerk.forms import NewClerkForm, LoginForm, UpdateClerkForm, RequestResetForm, ResetPasswordForm
from Golden_Leaf.models import Clerk, db


def view_clerk_dlc(*args, **kwargs):
    id = request.view_args['id']
    c = Clerk.query.get(id)
    return [{'text': c.name}]


@blueprint_clerk.route('/login', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_clerk, '.login', 'Login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blueprint_main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        clerk = Clerk.query.filter_by(email=form.email.data).first()
        if clerk is not None and clerk.verify_password(form.password.data):
            login_user(clerk)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('blueprint_main.index'))
        else:
            flash('Erro, login ou senha inválidos!', 'danger')
            return redirect(url_for('blueprint_clerk.login'))
    return render_template('clerk/login.html', form=form)


@blueprint_clerk.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blueprint_main.index'))


@blueprint_clerk.route('/clerk/account', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_clerk, '.', 'Atendente')
def account():
    form = UpdateClerkForm()
    if form.validate_on_submit():        
        if form.image_file.data:
            picture_file = save_picture(form.image_file.data)            
            current_user.image_file = picture_file
        current_user.email = form.email.data
        db.session.commit()
        flash('Sua conta foi atualizada com sucesso.', 'success')
        return redirect(url_for('blueprint_clerk.account'))
    elif request.method == 'GET':
        form.phone_number.data = current_user.phone_number
        form.email.data = current_user.email    
    image_file = url_for('static', filename='profile_pic/' + current_user.image_file)
    return render_template('clerk/account.html', form=form, image_file=image_file)


@blueprint_clerk.route('/clerk/new', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_clerk, '.new_clerk', 'Novo Atendente')
def new_clerk():
    if current_user.is_authenticated:
        return redirect(url_for('blueprint_main.index'))
    form = NewClerkForm()
    if form.validate_on_submit():
        clerk = Clerk(form.name.data, form.phone_number.data, form.email.data,form.confirm.data)
        db.session.add(clerk)
        db.session.commit()
        login_user(clerk)        
        flash('Você foi registrado com sucesso!', 'info')
        return redirect(url_for('blueprint_clerk.account'))    
    return render_template('clerk/new.html', form=form)


def send_email(clerk):
    token = clerk.get_token()
    msg = Message('Requisição de redefinição de senha', sender=current_app.config['FLASKY_MAIL_SENDER'],
                  recipients=[clerk.email])
    msg.body = f''' Para redefinir sua senha, visite o seguinte endereço: {url_for('reset_token', token=token,
                                                                                   _external=True)}
            Se você não fez esta requisição então ignore este email e mudança alguma será feita.
    '''
    mail.send(msg)


@blueprint_clerk.route('/clerk/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('blueprint_main.index'))
    form = RequestResetForm()
    if form.is_submitted():
        clerk = Clerk.query.filter_by(email=form.email.data).one()
        send_email(clerk)
        flash('Um email foi enviado com intruções para redefinir sua senha.', 'info')
        return redirect(url_for('blueprint_clerk.login'))
    return render_template('clerk/reset_request.html', form=form)


@blueprint_clerk.route('/clerk/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('blueprint_main.index'))
    clerk = Clerk.verify_token(token)
    if clerk is None:
        flash('O token recebido é inválido ou está expirado.', 'warning')
        return redirect(url_for('blueprint_clerk.reset_request'))
    form = ResetPasswordForm()
    if form.is_submitted():
        clerk.password = form.password.data
        db.session.commit()
        flash('Sua senha foi atualizada! Você pode agora fazer log in.', 'success')
    return render_template('clerk/reset_token.html', form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pic', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn
