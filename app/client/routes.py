from flask import render_template, redirect, flash, url_for, Blueprint, request
from app.models.tables import Client, Address, db
from app.client.forms import NewClientForm, SearchClientForm, UpdateClientForm
from flask_login import login_required
from app.client import blueprint_clients

@blueprint_clients.route('/clients/list')
@login_required
def listing_clients():
    page = request.args.get('page', 1, type=int)
    clients = Client.query.order_by(Client.name).paginate(page=page, per_page=10)
    return render_template('client/list.html', clients=clients)


@blueprint_clients.route('/clients/new', methods=['GET', 'POST'])
@login_required
def new_client():
    form = NewClientForm()
    if form.validate_on_submit():
        db.session.add(Client(form.name.data, form.phone_number.data, form.identification.data,
                              Address(form.street.data, form.address_detail.data, form.zip_code.data),
                              form.notifiable.data))
        db.session.commit()
        return redirect(url_for('blueprint_clients.listing_clients'))

    return render_template('client/new.html', form=form)


@blueprint_clients.route('/clients/<int:id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('blueprint_clients.listing_clients'))
    elif request.method == 'GET':
        form.name.data = client.name
        form.phone_number.data = client.phone_number
        form.notifiable.data = client.notifiable
        form.status.data = client.status

        form.street.data = client.address.street
        form.address_detail.data = client.address.detail
        form.zip_code.data = client.address.zip_code
    return render_template('client/edit.html', form=form)


@blueprint_clients.route('/clients/search', methods=["GET", 'POST'])
@login_required
def search_client():
    form = SearchClientForm()
    if form.validate_on_submit():
        # Finding names with “form.name.data” in them:
        clients = Client.query.filter(Client.name.like('%' + form.name.data + '%')).all()
        if not clients:
            flash('Nenhum cliente {} encontrado'.format(form.name.data), 'warning')
            return redirect(url_for('blueprint_clients.search_client'))
        else:
            flash('Mostrando cliente(s) encontrado(s) com nome: {}'.format(form.name.data), 'success')
            return render_template('client/list.html', clients=clients)

    return render_template("client/search.html", form=form)
