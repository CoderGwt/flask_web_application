from utils.email_secret import *


class Config:
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASKY_MAIL_SUBJECT_PREFIX = FLASKY_MAIL_SUBJECT_PREFIX
    FLASKY_MAIL_SENDER = FLASKY_MAIL_SENDER
    FLASKY_ADMIN = FLASKY_ADMIN

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = MAIL_SERVER
    MAIL_PORT = MAIL_PORT
    MAIL_USE_TLS = True
    MAIL_USERNAME = MAIL_USERNAME
    MAIL_PASSWORD = MAIL_PASSWORD
    SQLALCHEMY_DATABASE_URI = 'mysql://flask_data:flaskdata@localhost:3306/gwt_flask_web'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://flask_data:flaskdata@localhost:3306/gwt_flask_web'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://flask_data:flaskdata@localhost:3306/gwt_flask_web'


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}