from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "hello flask"


@app.route('/user/<name>/<int:path>/')  # 最后有/，url中没有，默认会加上；若最后没有/，请求url中有，或404；所以默认都加上/
def user(name, path):
    print(request.args)  # 获取url路径参数
    print(request.path, request.url, request.base_url)  # 获取url相关信息
    return "<h1>Hello, {}, {} !".format(name, path)


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')