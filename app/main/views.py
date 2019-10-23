from datetime import datetime

from flask import render_template, session, redirect, url_for, flash, current_app

from . import main
from .forms import NameForm
from .. import db
from ..models import User, Role
from ..email import send_mail


@main.route("/", methods=["GET", "POST"])
def index():
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
            if current_app.config.get('FLASK_ADMIN'):
                send_mail(current_app.config['FLASK_ADMIN'], "New User",
                          'mail/new_user', user=user)
        else:
            session['known'] = True
            flash("Nice to see you too !")
        session['name'] = form.name.data
        form.name.data = ""
        return redirect(url_for('.index'))  # main.index -> .index
    return render_template('index.html', name=session.get('name'),
                           form=form, known=session.get('known', False),
                           current_time=datetime.utcnow())