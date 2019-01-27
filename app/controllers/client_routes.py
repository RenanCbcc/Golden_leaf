from flask import render_template, request, redirect, flash, url_for
from app.models.tables import Client, Address, db
from app.models.forms import NewClienteForm, SearchClientForm
from flask_login import login_required
from app import app


@app.route('/client/list')
@login_required
def listing_clients():
    list_of_clients = Client.query.order_by(Client.name)
    return render_template('client/list.html', clients=list_of_clients)


@app.route('/client/new', methods=['GET', 'POST'])
@login_required
def new_client():
    form = NewClienteForm()
    if form.validate_on_submit():
        db.session.add(Client(form.name.data, form.phone_number.data, form.identification.data,
                              Address(form.street.data, form.number.data, form.zip_code.data)))
        db.session.commit()
        return redirect('/client/list')

    return render_template('client/new.html', form=form)


@app.route('/client/<int:id>/edit', methods=['PUT'])
@login_required
def edit_client(id):
    form = NewClienteForm()
    client = Client.query.filter_by(id=id).one()
    address = Address.queryfilter_by(id=client.address_id).one()
    if form.validate_on_submit():
        client.name = form.name.data
        client.phone_number = form.phone_number.data
        client.notifiable = form.notifiable.data
        client.status = form.status.data

        address.street = form.street.data
        address.number = form.number.data
        address.zip_code = form.zip_code.data

        db.session.add(client)
        db.session.commit()
        return redirect('/client/list')

    return render_template('client/edit.html', form=form, client=client,
                           address=address)


@app.route('/client/search', methods=['GET'])
@login_required
def search_client():
    form = SearchClientForm()
    if form.validate_on_submit():
        # Finding names with “form.name.data” in them:
        clients = Client.query.filter(Client.name.like('%' + form.name.data + '%'))
        if not clients:
            flash('Nenhum cliente {} encontrado'.format(form.name.data))
            return redirect(url_for('search_client'))

        else:
            return render_template('client/list.html', clients=clients)

    return render_template(url_for('search_client'))
