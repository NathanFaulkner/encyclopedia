from flask import render_template, flash, redirect, url_for, request, session
#from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import inspect, random

from app import app, db, books, sections, questions
from app.questions import *
from app.forms import AnswerForm


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'August'}
    path_for_iframe = 'hello'
    toc = books.Library.subdivisions
    return render_template('base.html', user=user, title='Home',
        site_name=app.config['SITE_NAME'], src=path_for_iframe, toc=toc)





############################################################################
# routes for iframe
@app.route('/hello')
def hello():
    user = {'username': 'August'}
    return render_template('hello.html', user=user, title='Home',
        site_name=app.config['SITE_NAME'])

@app.route('/algebra2')
def algebra2():
    template_path = sections.algebra2.d['template_path']
    return render_template(template_path + '.html')

@app.route('/factoring1')
def factoring1():
    template_path = sections.factoring1.d['template_path']
    return render_template(template_path + '.html')

@app.route('/polynomials')
def polynomials():
    template_path = sections.polynomials.d['template_path']
    return render_template(template_path + '.html')

@app.route('/quadraticpattern')
def quadraticpattern():
    template_path = sections.quadraticpattern.d['template_path']
    return render_template(template_path + '.html')

@app.route('/question/<question_name>', methods=['GET', 'POST'])
def question(question_name):
    # if request.method == 'GET':
    question_module = getattr(questions, question_name)
    user = {'username': 'August'}
    validator = question_module.Question_Class.validator
    form = AnswerForm(validator)
    # if request.method == 'POST':
    #     form = AnswerForm(request.form)
    # else:
    #     form = AnswerForm()
    #form = AnswerForm(request.form)
    # if request.method == 'POST':
    #     session['seed'] = form.seed.data
    # else:
    #     session['seed'] = random.random()
    #     form.seed.data = session['seed']
    if request.method == 'GET':
        session['seed'] = random.random()
        form.seed.data = session['seed']
        session['tried'] = False
    question = question_module.Question_Class(seed=session['seed'])
    useranswer = form.answer.data
    if form.validate_on_submit():
        correct = question.checkanswer(useranswer)
        if correct:
            message = 'You got it right!!'
            if session['tried'] == True:
                message += ' But you should try a new problem.'
        else:
            message = "If you want credit, you'll have to try a new problem."
        session['tried'] = True
    else:
        if request.method == 'POST':
            if session['tried'] == False:
                message = 'You can try again, since you just had a syntax error.'
            else:
                message = "You had a syntax error, but you should try a different problem if you want credit."
        else:
            message = "It's a brand new problem!!"
    # if request.method == 'POST':
    #      session['tried'] = True
    # try:
    #     seed = session['seed']
    # except:
    #     seed = random.random()
    #     session['seed'] = seed
    return render_template('question_page.html', user=user, title='Question',
        site_name=app.config['SITE_NAME'], form=form, question=question,
        tried=session['tried'], message=message)
#
############################################################################



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

@app.route('/Books/<book_name>/<chapter_number>')
def book_chapter(book_name, chapter_number):
    user = {'username': 'August'}
    book = getattr(books, book_name)
    main = book.subdivisions['main']
    chapter = main.subdivisions[int(chapter_number) - 1]
    path_for_iframe = chapter.view_name
    toc = main.subdivisions
    return render_template('chapter.html', user=user, title='chapter.name',
        site_name=app.config['SITE_NAME'], src=url_for(path_for_iframe), toc=toc,
        book_name=book_name, book=book)

@app.route('/Books/<book_name>/<chapter_number>/<section_number>')
def book_section(book_name, chapter_number, section_number):
    user = {'username': 'August'}
    book = getattr(books, book_name)
    main = book.subdivisions['main']
    chapter = main.subdivisions[int(chapter_number) - 1]
    section = chapter.subdivisions[int(section_number) - 1]
    path_for_iframe = section.view_name
    toc = main.subdivisions
    return render_template('chapter.html', user=user, title='section.name',
        site_name=app.config['SITE_NAME'], src=url_for(path_for_iframe), toc=toc,
        book_name=book_name, book=book)

@app.route('/Books/<book_name>')
def book(book_name):
    user = {'username': 'August'}
    book = getattr(books, book_name)
    path_for_iframe = 'hello'
    toc = book.subdivisions
    return render_template('book.html', user=user, title=book_name,
        site_name=app.config['SITE_NAME'], src=url_for(path_for_iframe), toc=toc,
        book=book, book_name=book_name)

@app.route('/Books')
def library():
    user = {'username': 'August'}
    path_for_iframe = 'hello'
    library = books.Library.subdivisions
    return render_template('library.html', user=user, title='Library',
        site_name=app.config['SITE_NAME'], src=url_for(path_for_iframe),
        library=library)
