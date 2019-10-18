from flask import render_template, redirect, flash, url_for, request
from flask_breadcrumbs import register_breadcrumb
from flask_login import login_required

from app.client import blueprint_client
from app.client.forms import NewClientForm, SearchClientForm, UpdateClientForm
from app.models.tables import Client, Address, db


def view_client_dlc(*args, **kwargs):
    id = request.view_args['id']
    c = Client.query.get(id)
    return [{'text': c.name}]


@blueprint_client.route('/client')
@register_breadcrumb(blueprint_client, '.', 'Clientes')
@login_required
def get_clients():
    page = request.args.get('page', 1, type=int)
    clients = Client.query.order_by(Client.name).paginate(page=page, per_page=10)
    return render_template('client/list.html', clients=clients)


@blueprint_client.route('/client/new', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_client, '.new_client', 'Novo Cliente')
@login_required
def new_client():
    form = NewClientForm()
    if form.validate_on_submit():
        db.session.add(Client(form.name.data, form.phone_number.data, form.identification.data,
                              Address(form.street.data, form.zip_code.data),
                              form.notifiable.data))
        db.session.commit()
        return redirect(url_for('blueprint_client.get_clients'))

    return render_template('client/new.html', form=form)


@blueprint_client.route('/client/<int:id>/update', methods=['GET', 'POST'])
@register_breadcrumb(blueprint_client, '.id', '.update_client', dynamic_list_constructor=view_client_dlc)
@login_required
def update_client(id):
    form = UpdateClientForm()
    client = Client.query.filter_by(id=id).one()
    if form.validate_on_submit():
        client.phone_number = form.phone_number.data
        client.notifiable = form.notifiable.data
        client.status = form.status.data

        client.address.street = form.street.data
        client.address.zip_code = form.zip_code.data

        db.session.add(client)
        db.session.commit()
        return redirect(url_for('blueprint_client.get_clients'))
    elif request.method == 'GET':
        form.name.data = client.name
        form.identification.data = client.identification
        form.phone_number.data = client.phone_number
        form.notifiable.data = client.notifiable
        form.status.data = client.status

        form.street.data = client.address.street
        form.zip_code.data = client.address.zip_code
    return render_template('client/edit.html', form=form)


@blueprint_client.route('/client/search', methods=["GET", 'POST'])
@register_breadcrumb(blueprint_client, '', 'Busca de Cliente')
@login_required
def search_client():
    page = request.args.get('page', 1, type=int)
    form = SearchClientForm()
    if form.validate_on_submit():
        # Finding names with “form.name.data” in them:
        clients = Client.query.filter(Client.name.like('%' + form.name.data + '%')).paginate(page=page, per_page=10)
        if not clients:
            flash('Nenhum cliente {} encontrado'.format(form.name.data), 'warning')
            return redirect(url_for('blueprint_client.search_client'))
        else:
            flash('Mostrando cliente(s) encontrado(s) com nome: {}'.format(form.name.data), 'success')
            return render_template('client/list.html', clients=clients)

    return render_template("client/search.html", form=form)
