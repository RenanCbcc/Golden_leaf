from flask import Flask
from main.controller import main
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
Bootstrap(application)
Mail(application)
Moment(application)

application.register_blueprint(main, url_prefix='/')



SQLALCHEMY_DATABASE_URI = 'mysql://flask:showmethemoney@localhost/commerce'
application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(application)


if __name__ == '__main__':
    application.run()