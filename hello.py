from threading import Thread

from flask import Flask, request, make_response, redirect, \
    abort, render_template, url_for, session, flash
from flask_script import Manager, Shell  # 导入flask-script 支持命令行选项
from flask_bootstrap import Bootstrap  # 导入 flask_bootstrap 继承Twitter Bootstrap
from flask_moment import Moment  # 使用Flask-Moment 本地化日期和时间
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, DateField
from wtforms.validators import Required, DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_mail import Mail, Message

from utils.email_secret import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY  # 通过app.config设置密钥

# 配置数据库信息, 使用mysql，书本使用SQLite
# todo mysql://username:password@hostname:port/db_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask_data:flaskdata@localhost:3306/gwt_flask_web'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 配置邮箱相关信息
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD  # 这个是授权码
app.config['FLAKSY_MAIL_SUBJECT_PREFIX'] = FLASKY_MAIL_SUBJECT_PREFIX
app.config['FLASKY_MAIL_SENDER'] = FLASKY_MAIL_SENDER
app.config['FLASK_ADMIN'] = FLASKY_ADMIN

manager = Manager(app)  # 初始化
bootstrap = Bootstrap(app)  # 初始化
moment = Moment(app)  # 初始化
db = SQLAlchemy(app)  # 初始化SQLAlchemy实例
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

mail = Mail(app)


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    """
    发送邮件
    :param to: 接收者的邮箱号
    :param subject: 邮件主题
    :param template: 邮件内容模板
    :param kwargs: 额外参数
    :return:
    """
    msg = Message(subject=app.config['FLAKSY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=to)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    # 开启线程发送邮件， 使用celery可能是个更加的选择
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr


class Role(db.Model):
    """create role model"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref='role', lazy='dynamic')

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    """create user model"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))  # 关联角色表

    def __repr__(self):
        return "<User %r>" % self.username


# @app.shell_context_processors
def make_shell_context():
    """注册了程序，数据库实例以及模型，使这些对象能够直接导入shell"""
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))


class NameForm(FlaskForm):
    """create a web form"""
    name = StringField('What is your name!', validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/", methods=["GET", "POST"])
def index():
    # return "<h1>Bad Request</h1>", 400  # 指定返回一个400的状态码
    # response = make_response('make response')
    # response.set_cookie('answer', '12')
    # return response
    # return redirect('/user/name/1/')  # 重定向到指定路由url
    # return render_template('index.html')
    # utcnow()显示的才是当前时间 UTC 协调世界时，now()显示的时间有时差，8个小时

    # todo 使用name存储form.name.data
    # name = None
    # form = NameForm()
    # if form.validate_on_submit():
    #     name = form.name.data
    #     form.name.data = ""
    # return render_template('index.html', current_time=datetime.utcnow(), form=form)

    # todo 优化，使用session保存用户数据信息
    # form = NameForm()
    # if form.validate_on_submit():
    #     old_name = session.get("name")
    #     if old_name is not None and old_name != form.name.data:
    #         flash("Looks like you have change your name !")  # todo 通过flash显示消息
    #     elif old_name == form.name.data:
    #         flash("Your name is not changed !")
    #     session['name'] = form.name.data
    #     return redirect(url_for('index'))  # 重定向到当前页面，GET方法，而不是POST

    # todo 使用数据库存储用户信息
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data, role_id=Role.query.first().id)
            db.session.add(user)
            session['known'] = False
            flash("Nice to meet you !")
            # todo 如果是新用户就发送邮箱表示欢迎
            if app.config.get('FLASK_ADMIN'):
                send_mail(app.config['FLASK_ADMIN'], "New User",
                          'mail/new_user', user=user)
        else:
            session['known'] = True
            flash("Nice to see you too !")
        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for('index'))
    return render_template('index.html', name=session.get('name'),
                           form=form, known=session.get('known', False))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # app.run(debug=True, port=8000, host='0.0.0.0')
    manager.run()