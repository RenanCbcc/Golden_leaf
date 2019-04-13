import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = 'e1ce303f7bad6f99d2e1320e287cc684'
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <noraplay@goldenleaf.com>'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:showmethemoney@localhost:3306/commerce'


class ProductionConfig(BaseConfig):
    # SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@hostname/database'
    SQLALCHEMY_DATABASE_URI = 'postgres://yfepsfknwjycne:4c75c5d2fe875b87706b264b20de4f977fa7d3561e977cd8f9f7ab54fd341ba1@ec2-54-83-50-174.compute-1.amazonaws.com:5432/ddca94vvt6qsno'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'commerce.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
