from flask import render_template, url_for
from app import app

site_name = 'Encyclopedia Omega'

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'August'}
    return render_template('index.html', user=user, title='Home', site_name=site_name)

@app.route('/hello')
def hello():
    user = {'username': 'August'}
    return render_template('hello.html', user=user, title='Home', site_name=site_name)
