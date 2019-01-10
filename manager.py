from flask import Flask
from main.controller import main
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from data.models import db

application = Flask(__name__)
Bootstrap(application)
Mail(application)
Moment(application)
db.init_app(application)
SQLALCHEMY_DATABASE_URI = 'mysql://flask:showmethemoney@localhost/commerce'
application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

application.register_blueprint(main, url_prefix='/')

if __name__ == '__main__':
    application.run()
