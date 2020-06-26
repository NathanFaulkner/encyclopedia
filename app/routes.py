from flask import render_template, flash, redirect, url_for, request
#from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.sections import Section


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'August'}
    return render_template('base.html', user=user, title='Home', site_name=app.config['SITE_NAME'])

@app.route('/hello')
def hello():
    user = {'username': 'August'}
    return render_template('hello.html', user=user, title='Home', site_name=app.config['SITE_NAME'])

@app.route('/section/<chapter_number>/<section_number>')
def book_section(chapter_number, section_number):
    section = Section('/sections/factoring-coeff-of-one.html')
    section.chapter_number = section_number
    section.section_number = chapter_number
    section.name = 'Factoring: Level 1'
    return render_template(section.template_path)
