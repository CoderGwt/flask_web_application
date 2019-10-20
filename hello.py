from flask import Flask, request, make_response, redirect, abort

app = Flask(__name__)


@app.route("/")
def index():
    # return "<h1>Bad Request</h1>", 400  # 指定返回一个400的状态码
    # response = make_response('make response')
    # response.set_cookie('answer', '12')
    # return response
    return redirect('/user/name/1/')  # 重定向到指定路由url


@app.route('/user/<name>/<int:path>/')  # 最后有/，url中没有，默认会加上；若最后没有/，请求url中有，或404；所以默认都加上/
def user(name, path):
    print(request.args)  # 获取url路径参数
    print(request.path, request.url, request.base_url)  # 获取url相关信息
    return "<h1>Hello, {}, {} !".format(name, path)


@app.route('/user/<int:id>/')
def get_user(id):
    user_id = range(1, 11)
    if id not in user_id:
        abort(404)
    return '<h1>Welcome</h1>'


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')