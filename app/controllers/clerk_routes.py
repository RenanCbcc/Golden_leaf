from flask import render_template, redirect, flash, url_for
from app.models.tables import Clerk, db
from app.models.forms import NewClerkForm
from flask_login import current_user
from app import app


@app.route('/clerk/new', methods=['GET', 'POST'])
def new_clerk():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = NewClerkForm()
    if form.validate_on_submit():
        clerk = Clerk(form.name.data, form.phone_number.data, form.email.data,
                      form.cofirm_password.data)
        db.session.add(clerk)
        db.session.commit()
        flash('Você pode fazer login agora.')
        return redirect(url_for('login'))
    return render_template('clerk/new.html', form=form)
