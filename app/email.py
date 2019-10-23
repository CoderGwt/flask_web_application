from threading import Thread
from flask import render_template, current_app
from flask_mail import Message

from app import mail


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
    app = current_app.__get_current_object()
    msg = Message(subject=app.config['FLAKSY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'],
                  recipients=to)
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)

    # 开启线程发送邮件， 使用celery可能是个更加的选择
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr