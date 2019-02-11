#!/usr/bin/python3
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'clerks.login'  # Function's name of route login from the blueprint.
login_manager.login_message_category = 'info'


def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.error.handler import errors
    app.register_blueprint(errors)

    from app.clerk.routes import blueprint_clerks
    app.register_blueprint(blueprint_clerks)

    from app.client.routes import blueprint_clients
    app.register_blueprint(blueprint_clients)

    from app.product.routes import blueprint_products
    app.register_blueprint(blueprint_products)

    from app.order.routes import blueprint_orders
    app.register_blueprint(blueprint_orders)

    from app.main.routes import main
    app.register_blueprint(main)

    from app.api import api
    app.register_blueprint(api, url_prefix='/api')

    return app
