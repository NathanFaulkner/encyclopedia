from flask import render_template, flash, redirect, url_for, request
#from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'August'}
    return render_template('index.html', user=user, title='Home', site_name=app.config['SITE_NAME'])

@app.route('/hello')
def hello():
    user = {'username': 'August'}
    return render_template('hello.html', user=user, title='Home', site_name=app.config['SITE_NAME'])
