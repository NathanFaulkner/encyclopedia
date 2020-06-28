from flask import render_template, flash, redirect, url_for, request
#from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db, books, sections
import inspect



@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'August'}
    path_for_iframe = 'hello'
    toc = books.Algebra2.subdivisions
    return render_template('base.html', user=user, title='Home',
        site_name=app.config['SITE_NAME'], src=path_for_iframe, toc=toc)

@app.route('/hello')
def hello():
    user = {'username': 'August'}
    return render_template('hello.html', user=user, title='Home',
        site_name=app.config['SITE_NAME'])

@app.route('/factoring1')
def factoring1():
    template_path = sections.factoring1.d['template_path']
    return render_template(template_path + '.html')

@app.route('/polynomials')
def polynomials():
    template_path = sections.polynomials.d['template_path']
    return render_template(template_path + '.html')

# @app.route('/<book_name>/<chapter_number>/<section_number>')
# def book_section(book_name, chapter_number, section_number):
#     user = {'username': 'August'}
#     book = getattr(books, book_name)
#     #section = book.structure[0][0]
#     path_for_iframe = '/sections/factoring-coeff-of-one'
#     toc = [ \
#     ['Chapter', '#', [['Section', '#'], ['Section2', '#'], ['Section3', '#']]], \
#     ['Chapter', '#', [['Section', '#'], ['Section2', '#']]], \
#     ['Chapter', '#', [['Section', '#'], ['Section2', '#']]], \
#     ]
#     return render_template('base.html', user=user, title='book.name',
#         site_name=app.config['SITE_NAME'], src=url_for(path_for_iframe))

@app.route('/<book_name>/<chapter_number>')
def book_chapter(book_name, chapter_number):
    user = {'username': 'August'}
    book = getattr(books, book_name)
    main = book.subdivisions[1]
    chapter = main.subdivisions[int(chapter_number) - 1]
    path_for_iframe = chapter.view_name
    toc = main.subdivisions
    return render_template('base.html', user=user, title='chapter.name',
        site_name=app.config['SITE_NAME'], src=url_for(path_for_iframe), toc=toc,
        book_name=book_name)

@app.route('/<book_name>/<chapter_number>/<section_number>')
def book_section(book_name, chapter_number, section_number):
    user = {'username': 'August'}
    book = getattr(books, book_name)
    main = book.subdivisions[1]
    chapter = main.subdivisions[int(chapter_number) - 1]
    section = chapter.subdivisions[int(section_number) - 1]
    path_for_iframe = section.view_name
    toc = book.subdivisions
    return render_template('base.html', user=user, title='section.name',
        site_name=app.config['SITE_NAME'], src=url_for(path_for_iframe), toc=toc,
        book_name=book_name)
