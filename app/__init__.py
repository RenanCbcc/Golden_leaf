from flask import Flask
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from app.extensions import bootstrap, breadcrumbs, db, mail, login_manager, admin


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bootstrap.init_app(app)
    breadcrumbs.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    login_manager.login_view = 'blueprint_clerk.login'  # Function's name of route login from the blueprint.
    login_manager.login_message_category = 'info'

    from app.models import User, Client, Clerk, Address, Product, Item, Order, Payment
    admin.add_view(AdminView(Client, db.session))
    admin.add_view(AdminView(Clerk, db.session))
    admin.add_view(AdminView(Address, db.session))
    admin.add_view(AdminView(Product, db.session))
    admin.add_view(AdminView(Item, db.session))
    admin.add_view(AdminView(Order, db.session))
    admin.add_view(AdminView(Payment, db.session))

    from app.routes.error.handler import blueprint_error
    app.register_blueprint(blueprint_error)

    from app.routes.clerk.routes import blueprint_clerk
    app.register_blueprint(blueprint_clerk)

    from app.routes.client.routes import blueprint_client
    app.register_blueprint(blueprint_client)

    from app.routes.category.routes import blueprint_category
    app.register_blueprint(blueprint_category)

    from app.routes.product.routes import blueprint_product
    app.register_blueprint(blueprint_product)

    from app.routes.order.routes import blueprint_order
    app.register_blueprint(blueprint_order)

    from app.routes.payment.routes import blueprint_payment
    app.register_blueprint(blueprint_payment)

    from app.routes.main.routes import blueprint_main
    app.register_blueprint(blueprint_main)

    from app.api import api
    app.register_blueprint(api, url_prefix='/api')

    # create all db tables
    @app.before_first_request
    def create_tables():
        db.create_all()

    return app
