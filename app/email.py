from flask import render_template
from flask_mail import Message
from app import app, mail
from threading import Thread

from app.models import BugReport

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    # print('Change detected')
    # Thread(target=send_async_email, args=(app, msg), daemon=True).start()
    # Thread(target=send_async_email, args=(app, msg)).start()
    mail.send(msg)

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Encyclopedia Omega] Reset Your P***word',
                sender=app.config['MAIL_USERNAME'],
                recipients=[user.email],
                text_body=render_template('email/reset_password.txt',
                                    user=user, token=token),
                html_body=render_template('email/reset_password.html',
                                    user=user, token=token))

def send_report_bug_email(report_id):
    bug_report = BugReport.query.filter_by(id=report_id).first()
    question_name = bug_report.question_name
    send_email('[Encyclopedia Omega] Bug Reported by User',
                sender=app.config['MAIL_USERNAME'],
                recipients=app.config['ADMINS'],
                text_body=render_template('email/report_bug.txt',
                                        question_name=question_name,
                                        bug_id=report_id),
                html_body=render_template('email/report_bug.html',
                                        question_name=question_name,
                                        bug_id=report_id))

# sender=app.config['ADMINS'][0],
