from flask import render_template, redirect, flash, url_for, Blueprint
from app.models.tables import Client, Address, db
from app.client.forms import NewClientForm, SearchClientForm, UpdateClientForm
from flask_login import login_required

clients = Blueprint('clients', __name__)


@clients.route('/client/list')
@login_required
def listing_clients():
    clients = Client.query.order_by(Client.name)
    return render_template('client/list.html', clients=clients)


@clients.route('/client/new', methods=['GET', 'POST'])
@login_required
def new_client():
    form = NewClientForm()
    if form.validate_on_submit():
        db.session.add(Client(form.name.data, form.phone_number.data, form.identification.data,
                              Address(form.street.data, form.address_detail.data, form.zip_code.data),
                              form.notifiable.data))
        db.session.commit()
        return redirect(url_for('listing_clients'))

    return render_template('client/new.html', form=form)


@clients.route('/client/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_client(id):
    form = UpdateClientForm()
    client = Client.query.filter_by(id=id).one()
    if form.validate_on_submit():
        client.name = form.name.data
        client.phone_number = form.phone_number.data
        client.notifiable = form.notifiable.data
        client.status = form.status.data

        client.address.street = form.street.data
        client.address.detail = form.address_detail.data
        client.address.zip_code = form.zip_code.data

        db.session.add(client)
        db.session.commit()
        return redirect(url_for('listing_clients'))
    form.name.data = client.name
    form.phone_number.data = client.phone_number
    form.notifiable.data = client.notifiable
    form.status.data = client.status

    form.street.data = client.address.street
    form.address_detail.data = client.address.detail
    form.zip_code.data = client.address.zip_code
    return render_template('client/edit.html', form=form)


@clients.route('/client/search', methods=["GET", 'POST'])
@login_required
def search_client():
    form = SearchClientForm()
    if form.validate_on_submit():
        # Finding names with “form.name.data” in them:
        clients = Client.query.filter(Client.name.like('%' + form.name.data + '%')).all()
        if not clients:
            flash('Nenhum cliente {} encontrado'.format(form.name.data))
            return redirect(url_for('search_client'))
        else:
            flash('Mostrando cliente(s) encontrado(s) com nome: {}'.format(form.name.data))
            return render_template('client/list.html', clients=clients)

    return render_template("client/search.html", form=form)
