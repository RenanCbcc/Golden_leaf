from flask_admin import Admin
from flask_bootstrap import Bootstrap
from flask_breadcrumbs import Breadcrumbs
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
breadcrumbs = Breadcrumbs()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
admin = Admin(name='Golden Leaf', template_mode='bootstrap3')
