from flask import Flask, render_template
from flask_bootstrap import Bootstrap  # 导入 flask_bootstrap 继承Twitter Bootstrap
from flask_moment import Moment  # 使用Flask-Moment 本地化日期和时间
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


# todo 程序工厂函数？？？
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # TODO form_object
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


