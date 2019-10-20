from datetime import datetime

from flask import Flask, request, make_response, redirect, abort, render_template
from flask_script import Manager  # 导入flask-script 支持命令行选项
from flask_bootstrap import Bootstrap  # 导入 flask_bootstrap 继承Twitter Bootstrap
from flask_moment import Moment  # 使用Flask-Moment 本地化日期和时间


app = Flask(__name__)
manager = Manager(app)  # 初始化
bootstrap = Bootstrap(app)  # 初始化
moment = Moment(app)


@app.route("/")
def index():
    # return "<h1>Bad Request</h1>", 400  # 指定返回一个400的状态码
    # response = make_response('make response')
    # response.set_cookie('answer', '12')
    # return response
    # return redirect('/user/name/1/')  # 重定向到指定路由url
    # return render_template('index.html')
    # utcnow()显示的才是当前时间 UTC 协调世界时，now()显示的时间有时差，8个小时
    return render_template('index.html', current_time=datetime.utcnow())


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