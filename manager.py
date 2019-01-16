from flask import Flask
from controller.default import main
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from data.models import Base

application = Flask(__name__)


Bootstrap(application)
Mail(application)
Moment(application)
#SQLALCHEMY_DATABASE_URI = 'mysql://flask:showmethemoney@localhost:3306/commerce'
application.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

application.register_blueprint(main, url_prefix='/')


if __name__ == '__main__':
    application.run()
