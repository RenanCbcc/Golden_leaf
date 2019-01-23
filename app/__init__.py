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
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# This variable needs to be already declared even before these pages exist, otherwise
# you'll get a ImportError: cannot import name 'app'.
from app.controllers import default, errors
from app.models import tables, forms
