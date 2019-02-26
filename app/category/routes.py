from app import db
from app.category import blueprint_category
from flask import render_template, redirect, url_for, request

from app.category.forms import NewCategoryForm
from app.models.tables import Category


@blueprint_category.route("/category/list")
def listing_categories():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.order_by(Category.title).paginate(page=page, per_page=10)
    return render_template('categorie/list.html', categories=categories)


@blueprint_category.route("/category/new")
def new_category():
    form = NewCategoryForm()
    if form.validate_on_submit():
        db.session.add(Category(form.title.data))
        db.session.commit()
        return redirect(url_for('blueprint_category.listing_categories'))
    return render_template('category/new.html', form=form)


@blueprint_category.route("/category/search")
def search_category():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.order_by(Category.title).paginate(page=page, per_page=10)
    return render_template('categorie/list.html', categories=categories)


@blueprint_category.route("/category/update")
def update_category():
    page = request.args.get('page', 1, type=int)
    categories = Category.query.order_by(Category.title).paginate(page=page, per_page=10)
    return render_template('categorie/list.html', categories=categories)
