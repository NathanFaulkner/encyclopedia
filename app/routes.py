from flask import render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
import inspect, random

from app import app, db, books, sections, questions
from app.questions import *
from app.forms import AnswerForm, LoginForm, RegistrationForm
from app.models import Student, StudentAnswer



@app.route('/index')
def index():
    user = {'username': 'August'}
    path_for_iframe = 'hello'
    toc = books.Library.subdivisions
    return render_template('base.html', user=user, title='Home',
        site_name=app.config['SITE_NAME'], src=path_for_iframe, toc=toc)

@app.route('/')
@app.route('/entrance')
def entrance():
    return render_template('entrance.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('library'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('library'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('entrance'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('library'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Student(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = Student.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password.')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                            title='Reset Password', form=form)


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
    if current_user.is_authenticated:
        user = current_user
    else:
        user = {'username': 'Anonymous'}
    validator = question_module.Question_Class.validator
    form = AnswerForm(validator)
    if request.method == 'GET':
        session['seed'] = random.random()
        form.seed.data = session['seed']
        session['tried'] = False
    question = question_module.Question_Class(seed=session['seed'])
    # if request.method == 'GET':
    #     answer_event = StudentAnswer(student=student, skillname=question_name,
    #                     grade_category='check', seed=session['seed'])
    #     db.session.add(answer_event)
    #     # db.session.commit()
    # else:
    #     answer_event = StudentAnswer.query.filter_by(seed=session['seed'], student=student).first()
    useranswer = form.answer.data
    if form.validate_on_submit():
        correct = question.checkanswer(useranswer)
        if current_user.is_authenticated:
            user = current_user
            answer_event = StudentAnswer(student=user, skillname=question_name,
                        grade_category='check', seed=session['seed'])
            db.session.add(answer_event)
        if correct:
            message = 'You got it right!!'
            if session['tried'] == True:
                message += ' But you should try a new problem.'
            else:
                if current_user.is_authenticated:
                    answer_event.correct = True
                    db.session.commit()
        else:
            message = "If you want credit, you'll have to try a new problem."
            if current_user.is_authenticated:
                answer_event.correct = False
                db.session.commit()
        session['tried'] = True
    else:
        if request.method == 'POST':
            if session['tried'] == False:
                message = 'You can try again, since you just had a syntax error.'
            else:
                message = """You had a syntax error,
but you should try a different problem if you want credit."""
        else:
            message = "It's a brand new problem!!"
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
    return render_template('chapter.html', user=user, title=book_name,
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
