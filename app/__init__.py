#!/usr/bin/python3
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object('app.configuration.config.TestingConfig')
db = SQLAlchemy(app)
Bootstrap(app)
Mail(app)
Moment(app)
login_manager = LoginManager(app)
login_manager.login_view = 'clerks.login'  # Function's name of route login from the blueprint.
login_manager.login_message_category = 'info'
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# This variable needs to be already declared even before these pages exist, otherwise
# you'll get a ImportError: cannot import name 'app'.
# Importing the blueprints
from app.models.tables import Product, Client, Clerk
from app.clerk.routes import clerks
from app.client.routes import clients
from app.product.routes import products
from app.order.routes import orders
from app.main.routes import main

app.register_blueprint(main)
app.register_blueprint(clients)
app.register_blueprint(clerks)
app.register_blueprint(products)
app.register_blueprint(orders)
