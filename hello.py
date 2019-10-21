from datetime import datetime

from flask import Flask, request, make_response, redirect, \
    abort, render_template, url_for, session, flash
from flask_script import Manager  # 导入flask-script 支持命令行选项
from flask_bootstrap import Bootstrap  # 导入 flask_bootstrap 继承Twitter Bootstrap
from flask_moment import Moment  # 使用Flask-Moment 本地化日期和时间

from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, DateField
from wtforms.validators import Required, DataRequired


app = Flask(__name__)
app.config['SECRET_KEY'] = "thisisthesecretkeyandhardtoguessstring"  # 通过app.config设置密钥
manager = Manager(app)  # 初始化
bootstrap = Bootstrap(app)  # 初始化
moment = Moment(app)


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
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have change your name !")  # todo 通过flash显示消息
            session['name'] = form.name.data
        elif old_name == form.name.data:
            flash("Your name is not changed !")
        return redirect(url_for('index'))  # 重定向到当前页面，GET方法，而不是POST
    return render_template('index.html', name=session.get('name'), form=form)


@app.route('/user/<name>/')  # 最后有/，url中没有，默认会加上；若最后没有/，请求url中有，或404；所以默认都加上/
def user(name):
    print(request.args)  # 获取url路径参数
    print(request.path, request.url, request.base_url)  # 获取url相关信息
    comments = range(1, 10)
    return render_template('user.html', name=name, comments=comments)


@app.route('/user/<int:id>/')
def get_user(id):
    user_id = range(1, 11)
    if id not in user_id:
        abort(404)
    return '<h1>Welcome</h1>'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # app.run(debug=True, port=8000, host='0.0.0.0')
    manager.run()