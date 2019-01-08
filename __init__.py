from flask import Flask
from main.controller import main
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment


application = Flask(__name__)
Bootstrap(application)
Mail(application)
Moment(application)

application.register_blueprint(main, url_prefix='/')

if __name__ == '__main__':
    application.run()