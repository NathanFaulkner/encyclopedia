import inspect, random, datetime, io, json

from flask import (render_template,
                    flash,
                    redirect,
                    url_for,
                    request,
                    session,
                    make_response,)
from flask_login import (current_user,
                        login_user,
                        logout_user,
                        login_required)
from werkzeug.urls import url_parse

from app import app, db, books, sections, questions, interpolator

from app.questions import *
from app.forms import (AnswerForm,
                        LoginForm,
                        RegistrationForm,
                        ResetPasswordRequestForm,
                        ResetPasswordForm,
                        BlankForm,
                        ReportBugForm,
                        ResetEmailForm)
from app.models import (Student,
                        StudentAnswer,
                        BugReport,
                        get_user_books,
                        UserGradeInfo,
                        UserSectionGradeInfo,
                        UserSectionStatus)
from app.email import (send_password_reset_email,
                        send_report_bug_email)

# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
# from matplotlib.dates import DateFormatter








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
    if request.method == 'GET':
        session['prev_page'] = request.referrer
    # print('referrer', request.referrer)
    # print('request.args at GET login', request.args)
    if form.validate_on_submit():
        user = Student.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # print('referrer', request.referrer)
        # next_page = request.args.get('next')
        next_page = session['prev_page']
        # print('next_page', next_page)
        if not next_page: # or url_parse(next_page).netloc != '':
            next_page = url_for('library')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    print('logout referrer', request.referrer)
    next_page = request.referrer
    if not next_page: # or url_parse(next_page).netloc != '':
        next_page = url_for('entrance')
    return redirect(next_page)
    # return redirect(url_for('entrance'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('library'))
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        user = Student(username=form.username.data,
                        email=form.email.data,
                        firstname=form.firstname.data,
                        lastname=form.lastname.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        super_user = Student.query.filter_by(username='Nathan').first()
        user = Student.query.filter_by(username=username, email=form.email.data).first()
        user.name_as_observer(super_user)
        db.session.commit()
        flash('You are now a registered user.')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_p***word/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('library'))
    user = Student.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('library'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

@app.route('/reset_email', methods=['GET', 'POST'])
def reset_email():
    if not current_user.is_authenticated:
        return redirect(url_for('library'))
    form = ResetEmailForm()
    if form.validate_on_submit():
        current_user.set_email(form.email.data)
        db.session.commit()
        flash('Your email has been reset')
        return redirect(url_for('user', username=current_user.username))
    return render_template('reset_email.html', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('library'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash("Check your email for the instructions to reset your password.  If the email doesn't come through in a minute or so, please send a second request.")
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                            title='Reset Password', form=form)

@app.route('/report_bug', methods=['POST'])
def report_bug():
    form = BlankForm()
    seed = session.get('seed')
    user_answer = session.get('user_answer')
    question_name = session.get('question_name')
    if form.validate_on_submit():
        return send_report_bug_email(question_name, seed, user_answer)
    return redirect(url_for('library'))

@app.route('/user/<username>')
@login_required
def user(username):
    profile_user = Student.query.filter_by(username=username).first_or_404()
    # answers = StudentAnswer.query.filter_by(user_id=profile_user.id).all()
    # books = []
    # for answer in answers:
    #     answer = answer.__dict__
    #     book = answer.get('book')
    #     if book not in books and book is not None:
    #         books.append(book)
    # books = get_user_books(profile_user)
    grades = UserGradeInfo(profile_user)
    # book_names = grades.get_book_names()
    # print('book_names: ', book_names)
    # user_books = []
    # for book_name in book_names:
    #     book = getattr(books, book_name)
    #     user_books.append(book)
    user_books = grades.get_books()
    form = BlankForm()
    try:
        observed = current_user.observed_students.order_by(Student.lastname.asc(),
                                                            Student.firstname.asc()).all()
    except AttributeError:
        observed = None
    return render_template('user.html', user=profile_user, form=form,
                            grades=grades, user_books=user_books,
                            observed=observed)

@app.route('/name_as_observer/<username>', methods=['POST'])
@login_required
def name_as_observer(username):
    form = BlankForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('library'))
        if user == current_user:
            flash('You automatically observe yourself.')
            return redirect(url_for('user', username=username))
        current_user.name_as_observer(user)
        db.session.commit()
        flash('You are now observed by {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('library'))

@app.route('/remove_as_observer/<username>', methods=['POST'])
@login_required
def remove_as_observer(username):
    form = BlankForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('library'))
        if user == current_user:
            flash('You cannot un-observe yourself!')
            return redirect(url_for('user', username=username))
        current_user.remove_as_observer(user)
        db.session.commit()
        flash('You are no longer observed by {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('library'))

@app.route('/unobserve/<username>', methods=['POST'])
@login_required
def unobserve(username):
    form = BlankForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('library'))
        if user == current_user:
            flash('You cannot un-observe yourself!')
            return redirect(url_for('user', username=username))
        current_user.unobserve(user)
        db.session.commit()
        flash('You are no longer an observer of {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('library'))
############################################################################
# routes for iframe
@app.route('/hello')
def hello():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = {'username': 'Anonymous'}
    return render_template('hello.html', user=user, title='Home',
        site_name=app.config['SITE_NAME'])

# @app.route('/algebra2')
# def algebra2():
#     template_path = sections.algebra2.d['template_path']
#     return render_template(template_path + '.html')
#
# @app.route('/factoring1')
# def factoring1():
#     template_path = sections.factoring1.d['template_path']
#     return render_template(template_path + '.html')
#
# @app.route('/polynomials')
# def polynomials():
#     template_path = sections.polynomials.d['template_path']
#     return render_template(template_path + '.html')
#
# @app.route('/quadraticpattern')
# def quadraticpattern():
#     template_path = sections.quadraticpattern.d['template_path']
#     return render_template(template_path + '.html')

@app.route('/section/<section_name>')
def section(section_name):
    session['section_name'] = section_name ## Added 12/16/2020
    section = getattr(books, section_name)
    template_path = section.template_path
    section_display_name = section.display_name
    questions = section.questions
    # print(questions)
    if questions != []:
        if current_user.is_authenticated:
            section_status = UserSectionStatus.query.filter_by(student=current_user, section_name=section_name).first()
            if section_status == None:
                section_status = UserSectionStatus(student=current_user, section_name=section_name, grade=0)
                db.session.commit()
            if section_status.underway:
                question_name = section_status.underway_question_name
                if question_name not in questions:
                    question_name = random.choice(questions)
            else:
                question_name = random.choice(questions)
        else:
            question_name = random.choice(questions)
    else:
        question_name = False
    # print(question_name)
    return render_template(template_path + '.html',
        section_display_name=section_display_name,
        question_name=question_name)


@app.route('/answer_previewer/<question_name>', methods=['GET', 'POST'])
def answer_previewer(question_name):
    user_answer = request.args.get('user_answer')
    question = getattr(questions, question_name).Question_Class
    if user_answer == None:
        return redirect(url_for('library'))
    # print(question.format_useranswer)
    # print(type(user_answer))
    try:
        question.validator(user_answer)
        if 'simplify' in user_answer or 'factor' in user_answer or 'solve' in user_answer:
            return 'The answer checker will not admit this input.'
    except SyntaxError:
        return 'The answer checker will not admit this input.'
    try:
        content = question.format_useranswer(user_answer)
    except TypeError:
        return 'This functionality is not available for this problem.'
    except:
        return 'This will result in an error.'
    return render_template('just_math_jax.html', content=content)
        # return 'hello'


# Avert your eyes from this monster!!  This is what happens
# when you learn as you build and don't have time for a re-write!!
@app.route('/question/<question_name>', methods=['GET', 'POST'])
def question(question_name):
    """
    A rewrite could
    include using only one 'form' of the type AnswerForm, but
    deciding whether to display an answer field or instead
    write to it secretly based on either multiple
    answer fields or based on interaction with a graph, etc.  ...
    An arbitrary page should also be used in place of
    question_page.html---that is, the template to be rendered
    should be a variable that is determined by the attribute
    question.template.  Of course, many of these templates
    could inherit from a common template, too!  Many other
    functions should be tossed to methods of the
    question = QuestionClass() object.  For instance, ajax
    handling could happen there.  Interpolator should be moved
    to the questions module...
    """
    # print('session at first', session)
    # if request.args.get('bug_id'):
    #     answer_id = request.args.get('bug_id')
    #     bug_answer = StudentAnswer.query.filter_by(id=answer_id).first()
        # print('bug_answer.seed', bug_answer.seed)
    # print(request.args)
    bug_form = ReportBugForm()
    book_info = {}
    session['question_name'] = question_name
    if current_user.is_authenticated: ## Added 12/16/2020
        section_name = session.get('section_name') ## Added 12/16/2020
        # print(section_name)
        if not session.get('tried'):
            if section_name is None:
                # print('this is untested')
                return redirect(url_for('logout'))
                # session['tried'] = True
            else:
                _section = getattr(books, section_name)
                # print('The section is', section_name)
                if question_name not in _section.questions:
                    # print('logged you out since question not in section')
                    flash('You need to navigate to or from the corresponding book section in order to get credit.  You have been logged out.')
                    # session['tried'] = True
                    return redirect(url_for('logout'))
        grade_info = UserSectionStatus.query.filter_by(student=current_user, section_name=section_name).first()## Added 12/16/2020;
        # if section_name is not None and grade_info is None:
        #     print('this is untested also')
        #     grade_info = UserSectionStatus(current_user, section_name, grade=0) #This is untested, but seems necessary...
    else:  ## Added 12/16/2020
        # print('no user!!!!!')
        grade_info = None  ## Added 12/16/2020
    if current_user.is_authenticated:
        user_book_names = json.loads(current_user.books)
        # user_books = [getattr(books, book_name) for book_name in user_book_names]
        books_info = []
        for book_name in user_book_names:
            book = getattr(books, book_name)
            info = book.get_skill_info(question_name)
            for occurrence in info:
                books_info.append({'book': book.name_for_path,
                                'chapter': occurrence[0],
                                'section': occurrence[1]})
    if session.get('section'):
        book_name = session.get('book')
        book = getattr(books, book_name)
        main = book.subdivisions['main']
        chapter_number = int(session.get('chapter'))
        chapter = main.subdivisions[chapter_number - 1]
        section_number = int(session.get('section'))
        section = chapter.subdivisions[section_number - 1]
        book_info = {'book': book.name_for_path,
                    'chapter': chapter_number,
                    'section': section_number}
        # print('section: ', section)
        # print('book info: ', book_info)
    user_poly_points = ''
    graph = None
    correct_answer_poly_points = ''
    # if request.method == 'GET':
    parameters = None
    question_module = getattr(questions, question_name)
    if current_user.is_authenticated:
        user = current_user
    else:
        user = {'username': 'Anonymous'}
    # validator = question_module.Question_Class.validator
    if question_module.prob_type == 'graph':
        # print("Working with a graph here")
        form = BlankForm()
        whether_graph = True
        parameters = interpolator.get_parameters()
        # print('parameters: ', parameters, '; type is ', type(parameters))
        # print('This is how I view form.validate_on_submit: ', form.validate_on_submit())
        if 'data' in request.form and not form.validate_on_submit():
            points = request.form["data"]
            shift_y = json.loads(request.form["shift_y"])
            print('shift_y', shift_y)
            # session['user_answer'] = points # for bug reporting
            # print('points straight from page: ', type(points))
            points = json.loads(points)
            # print(points)
            return_data = interpolator.get_dict_for_svg(points, shift_y=shift_y)
            # graph = interpolator.Graph(points)
            # graph.gen_dict_for_svg()
            # return_data = graph.svg_data
            # print(return_data)
            #return json.dumps(data)
            # graph = interpolator.Graph(points)
            session['user_points'] = points
            session['shift_y'] = shift_y
            # print('session says the user answer is:', session['user_answer'])
            return json.dumps(return_data)
    elif question_module.prob_type == 'real_line_graph':
        form = question_module.form()
        real_line = True
        whether_graph = False
    else:
        validator = question_module.Question_Class.validator
        form = AnswerForm(validator)
        # print('form.answer.data just after (re)instantiation', form.answer.data)
        whether_graph = False
        real_line = False
    if request.method == 'GET':
        session['user_answer'] = json.dumps(None)
        if request.args.get('bug_id'):
            bug_id = request.args.get('bug_id')
            bug_answer = BugReport.query.filter_by(id=bug_id).first()
            session['tried'] = True
            session['seed'] = bug_answer.seed
            # print('session seed after bug assignment', session['seed'])
            if whether_graph:
                try:
                    session['user_points'] = json.loads(bug_answer.user_answer)
                except (json.decoder.JSONDecodeError, TypeError) as e:
                    session['user_points'] = []
            elif question_module.prob_type == 'real_line_graph':
                # print('Not my fault!')
                try:
                    user_answer = json.loads(bug_answer.user_answer)
                    user_points = user_answer['user_points']
                    user_intervals = user_answer['user_intervals']
                except:
                    return f'bug_id: {bug_id}, seed: {bug_answer.seed}, question_name: {bug_answer.question_name}'
            else:
                form.answer.data = bug_answer.user_answer
        elif request.args.get('ans_id'):
            # print('This worked!')
            ans_id = request.args.get('ans_id')
            answer = StudentAnswer.query.filter_by(id=ans_id).first()
            session['tried'] = True
            session['seed'] = answer.seed
            flash('This is your original submission, but the problem is just for practice now.')
            if whether_graph:
                try:
                    info = json.loads(answer.user_answer)
                    # session['user_points']
                    if type(info) == dict:
                        session['user_points'] = info.get('points')
                        session['shift_y'] = info.get('shift_y')
                    else:
                        session['user_points'] = info
                except (json.decoder.JSONDecodeError, TypeError) as e:
                    session['user_points'] = []
            elif question_module.prob_type == 'real_line_graph':
                question = question_module.Question_Class(seed=session['seed'])
                answer = json.loads(answer.user_answer)
                user_points = answer['user_points']
                user_intervals = answer['user_intervals']
                question.points = user_points
                question.intervals = user_intervals
            else:
                form.answer.data = answer.user_answer
        elif request.args.get('skip_to_exercises'):
            # print('It worked!')
            session['tried'] = True
            session['seed'] = random.random()
            question = question_module.Question_Class(seed=session['seed'])
            session['user_points'] = []
            flash('This problem is just for practice.  If you want to work one for credit, navigate from a book section.')
        elif current_user.is_authenticated and grade_info.underway:
            question = question_module.Question_Class(seed=grade_info.underway_seed)
            session['tried'] = False
            session['seed'] = grade_info.underway_seed
            session['user_points'] = []
        else: # AttributeError:
            # print('Else anonymous!!!')
            session['tried'] = False
            session['seed'] = random.random()
            if current_user.is_authenticated:
                grade_info.underway = True
                grade_info.underway_question_name = question_name
                grade_info.underway_seed = session['seed']
                db.session.commit()
            session['user_points'] = []
        # form.seed.data = session['seed']

    try:
        question
    except NameError:
        try:
            question = question_module.Question_Class(seed=session['seed'])
        except:
            question = question_module.Question_Class()
    # print('session seed', session['seed'])

    if whether_graph:
        points = session.get('user_points')
        print(points)
        shift_y = session.get('shift_y')
        # print('These are the points in session: ', points)
        # print('This is what I think about the form: ', form)
        # graph = interpolator.Graph(points, shift_y=shift_y) # I don't actually use 'shift_y'... I did temporarily... It's a nice proof of concept for further use of ajax here, but I preferred another solution from a philosphical perspective.
        graph = interpolator.Graph(points)
        print('graph.vert is', graph.vert)
        if points != []:
            print('points is not []')
            if not graph.vert:
                print('thinks graph not vert')
                useranswer = graph.as_lambda
            else:
                print('graph.vert == True')
                useranswer = points[0][0]
            graph.gen_dict_for_svg()
            # if graph.piecewise:
            # #     print('yay!')
            #     user_poly_points = graph.
            # else:
            # #     print('still yay!')
            user_poly_points = graph.poly_points
            # user_answer_for_db = json.dumps({'points': points, 'shift_y': shift_y})
            user_answer_for_db = json.dumps(points)
        else:
            useranswer = None
            user_answer_for_db = json.dumps([])
        x_min = parameters['cart_x_min']
        x_max = parameters['cart_x_max']
        correct_answer_poly_points = question.get_svg_data([x_min, x_max])
        # print("session['useranswer']", session['user_answer'])
    elif question_module.prob_type == 'real_line_graph':
        if form.points.data:
            user_points = json.loads(form.points.data)
            question.points = user_points
        elif request.args.get('bug_id'):
            question.points = user_points
        else:
            user_points = []
        # for item in user_points:
        #     print('point:', item)
        #     print('type:', type(item))
        # print(user_points)
        if form.intervals.data:
            user_intervals = json.loads(form.intervals.data)
            question.intervals = user_intervals
        elif request.args.get('bug_id'):
            question.intervals = user_intervals
        else:
            user_intervals = []
        # for item in user_intervals:
        #     print('interval:', item)
        #     print('type:', type(item))
        useranswer = {'user_points': user_points, 'user_intervals': user_intervals}
        user_answer_for_db = json.dumps(useranswer)
    else:
        useranswer = form.answer.data
        session['user_answer'] = form.answer.data or session.get('user_answer') #for bug report
        user_answer_for_db = useranswer
        correct_answer_poly_points = ''
    # print("request.args.get('form')", request.args.get('form'))
    # Added the request.args.get('form') == 'form' requirement in the process
    # of figuring out if I could have a second submit button---for submitting
    # requests for a preview of the math AnswerForm
    if form.validate_on_submit() and request.args.get('form') == 'form' and not (whether_graph and points == []):
        correct = question.checkanswer(useranswer)
        if current_user.is_authenticated and not session['tried']:
            user = current_user
            now = datetime.datetime.utcnow()
            diff = now - grade_info.timestamp
            if diff > datetime.timedelta(0,5,0):
                grade_info.update_grade_after_user_attempt(correct, now, commit=False) ## Added 12/16/2020
                for book_info in books_info:
                    answer_event = StudentAnswer(student=user,
                                            skillname=question_name,
                                            grade_category='check',
                                            seed=session['seed'],
                                            book=book_info.get('book'),
                                            chapter=book_info.get('chapter'),
                                            section=book_info.get('section'),
                                            user_answer=user_answer_for_db)
                    db.session.add(answer_event)
                    if correct:  # Just in case you get clever and think you can just do answer_event.correct = correct, you might be wrong.... why I don't know!! ... oh, perhaps it is because of sympy returning special Boolean types rather than simple ones and sqlalchemy doesn't like them
                        answer_event.correct = True
                    else:
                        answer_event.correct = False
                    # answer_event.correct = correct
            grade_info.underway = False
            db.session.commit()
        if correct:
            message = 'You got it right!!'
            if session['tried'] == True:
                message += " But you'll have to try a new problem to earn credit."
        else:
            message = "Incorrect. You'll have to try a new problem."
            if whether_graph:
                message = 'The correct answer is in <span style="color:green">green</span>.'
            if question_module.prob_type == 'real_line_graph':
                message = 'The correct answer is in <span style="color:green">green</span>'
        # if current_user.is_authenticated and not session['tried']:
        #     db.session.commit()
        session['tried'] = True
    else:
        if request.method == 'POST':
            if session['tried'] == False:
                message = 'You can try again, since you just had a syntax error.'
                if (whether_graph and points == []):
                    message = "You left it blank!  You may try again."
            else:
                message = """You had a syntax error,
but you should try a different problem if you want credit."""
            if bug_form.validate_on_submit() and request.args.get('form') == 'bug_form':
                # print('bug_form_validated')
                flash('A bug report email was just sent to your friendly Ency-O Admin!')
                # print('form.answer.data', form.answer.data)
                # try:
                #     bug_answer = form.answer.data
                # except:
                #     bug_answer = json.dumps(session.get('user_points'))
                # print('bug_form.user_answer.data:', bug_form.user_answer.data)
                answer = bug_form.user_answer.data or session['user_answer']
                bug_report = BugReport(user_answer=answer,
                                        seed=session['seed'],
                                        question_name=question_name)
                db.session.add(bug_report)
                db.session.commit()
                bug_report = BugReport.query.filter_by(user_answer=answer,
                                        seed=session['seed'],
                                        question_name=question_name).all()[-1]
                report_id = bug_report.id
                # print('report_id', report_id)
                send_report_bug_email(report_id)
            # if preview_form.validate_on_submit() and request.args.get('form') == 'preview_form':
            #     return redirect(url_for('answer_previewer', question_name=question_name))
        else:
            message = "It's a brand new problem!!"
    # print('session user_points just before rendering', session.get('user_points'))
    # print('current book: ', session.get('book'))
    if session.get('section'): # This can result in jumping to an unintended question if the page is accessed directly.
        new_question_name = random.choice(section.questions)
        # print('new_question_name: ', new_question_name)
    else:
        new_question_name = question_name

    ###############################
    #This is for the progress bar.   Commented out on 12/16/2020
    ###############################
    # if current_user.is_authenticated:
    #     book_info = books_info[0]
    #     # grades = UserGradeInfo(current_user)
    #     # print(current_user.username)
    #     # print('book', book_info.get('book'))
    #     # print('chapter', book_info.get('chapter'))
    #     # print('section', book_info.get('section'))
    #     grade_info = UserSectionGradeInfo(current_user,
    #                                     book_info.get('book'),
    #                                     book_info.get('chapter'),
    #                                     book_info.get('section'))
    #     # print('grade is:', grade_info.grade)
    # else:
    #     grade_info = None
    #
    #  ## Concludes comment from 12/16/2020
    ###############################
    return render_template('question_page.html', user=user, title='Question',
        site_name=app.config['SITE_NAME'], form=form, question=question,
        tried=session['tried'], message=message, whether_graph=whether_graph,
        parameters=parameters, question_name=new_question_name,
        points=session.get('user_points'), graph=graph,
        correct_answer_poly_points=correct_answer_poly_points,
        user_poly_points=user_poly_points, grade_info=grade_info,
        bug_form=bug_form)
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
    session['book'] = book_name # I'm moving away from that...
    session['chapter'] = chapter_number # I'm moving away from that...
    if current_user.is_authenticated:
        user = current_user
        current_user.add_to_books(book_name) # This will be the better way!
        db.session.commit()
    else:
        user = {'username': 'Anonymous'}
    try:
        book = getattr(books, book_name)
        main = book.subdivisions['main']
        chapter = main.subdivisions[int(chapter_number) - 1]
    except AttributeError:
        return render_template('404.html'), 404
    path_for_iframe = url_for('section', section_name=chapter.view_name)
    toc = main.subdivisions
    return render_template('chapter.html', user=user, title='chapter.name',
        site_name=app.config['SITE_NAME'], src=path_for_iframe, toc=toc,
        book_name=book_name, book=book)

@app.route('/Books/<book_name>/<chapter_number>/<section_number>')
def book_section(book_name, chapter_number, section_number):
    session['book'] = book_name # I'm moving away from that...
    session['chapter'] = chapter_number # I'm moving away from that...
    session['section'] = section_number
    if current_user.is_authenticated:
        user = current_user
        current_user.add_to_books(book_name) # This will be the better way!
        db.session.commit()
    else:
        user = {'username': 'Anonymous'}
    try:
        book = getattr(books, book_name)
        main = book.subdivisions['main']
        chapter = main.subdivisions[int(chapter_number) - 1]
        section = chapter.subdivisions[int(section_number) - 1]
        section_name = section.view_name
        session['section_name'] = section_name
    except:
        return render_template('404.html'), 404
    skip_to_exercises = request.args.get('skip_to_exercises')
    # print('section query...', skip_to_exercises, type(skip_to_exercises))
    if request.args.get('skip_to_exercises') == 'True':
        if request.args.get('question_name'):
            question_name = request.args.get('question_name')
            ans_id = request.args.get('ans_id')
            path_for_iframe = url_for('question', question_name=question_name, skip_to_exercises=True, ans_id=ans_id)
        else:
            try:
                question_name = random.choice(section.questions)
                path_for_iframe = url_for('question', question_name=question_name, skip_to_exercises=True)
            except IndexError:
                path_for_iframe = ''
    else:
        path_for_iframe = url_for('section', section_name=section.view_name)
    toc = main.subdivisions
    # print(session['book'])
    return render_template('chapter.html', user=user, title=section.display_name,
        site_name=app.config['SITE_NAME'], src=path_for_iframe, toc=toc,
        book_name=book_name, book=book)

@app.route('/Books/<book_name>')
def book(book_name):
    session['book'] = book_name # I'm moving away from that...
    if current_user.is_authenticated:
        user = current_user
        current_user.add_to_books(book_name) # This will be the better way!
        db.session.commit()
    else:
        user = {'username': 'Anonymous'}
    try:
        book = getattr(books, book_name)
    except AttributeError:
        return render_template('404.html'), 404
    path_for_iframe = url_for('section', section_name=book.view_name)
    toc = book.subdivisions
    return render_template('chapter.html', user=user, title=book_name,
        site_name=app.config['SITE_NAME'], src=path_for_iframe, toc=toc,
        book=book, book_name=book_name)

@app.route('/Books')
def library():
    if current_user.is_authenticated:
        user = current_user
    else:
        user = {'username': 'Anonymous'}
    path_for_iframe = url_for('hello')
    library = books.Library.subdivisions
    return render_template('library.html', user=user, title='Library',
        site_name=app.config['SITE_NAME'], src=path_for_iframe,
        library=library)



# @app.route('/Books/<book_name>/<chapter_number>/<section_number>/Exercises', methods=['GET', 'POST'])
# def new_question(book_name, chapter_number, section_number):
#     book = getattr(books, book_name)
#     main = book.subdivisions['main']
#     chapter = main.subdivisions[int(chapter_number) - 1]
#     section = chapter.subdivisions[int(section_number) - 1]
#     book_info = {}
#     if session.get('section'):
#         book_info = {'book': book.name_for_path,
#                     'chapter': chapter_number,
#                     'section': section_number}
#         # print('section: ', section)
#         # print('book info: ', book_info)
#     question_name = random.choice(section.questions)
#     user_poly_points = ''
#     correct_answer_poly_points = ''
#     # if request.method == 'GET':
#     parameters = None
#     question_module = getattr(questions, question_name)
#     if current_user.is_authenticated:
#         user = current_user
#     else:
#         user = {'username': 'Anonymous'}
#     # validator = question_module.Question_Class.validator
#     if question_module.prob_type == 'graph':
#         print("Working with a graph here")
#         form = BlankForm()
#         whether_graph = True
#         parameters = interpolator.get_parameters()
#         # print('parameters: ', parameters, '; type is ', type(parameters))
#         print('This is how I view form.validate_on_submit: ', form.validate_on_submit())
#         if 'data' in request.form and not form.validate_on_submit():
#             return_data = {}
#             points = request.form["data"]
#             # print('points straight from page: ', type(points))
#             points = json.loads(points)
#             # print(points)
#             return_data = interpolator.get_dict_for_svg(points)
#             # graph = interpolator.Graph(points)
#             # graph.gen_dict_for_svg()
#             # return_data = graph.svg_data
#             # print(return_data)
#             #return json.dumps(data)
#             # graph = interpolator.Graph(points)
#             session['user_points'] = points
#             # print('session says the user answer is:', session['user_answer'])
#             return json.dumps(return_data)
#     else:
#         validator = question_module.Question_Class.validator
#         form = AnswerForm(validator)
#         whether_graph = False
#     if request.method == 'GET':
#         session['seed'] = random.random()
#         form.seed.data = session['seed']
#         session['tried'] = False
#         session['user_points'] = []
#     question = question_module.Question_Class(seed=session['seed'])
#     # if request.method == 'GET':
#     #     answer_event = StudentAnswer(student=student, skillname=question_name,
#     #                     grade_category='check', seed=session['seed'])
#     #     db.session.add(answer_event)
#     #     # db.session.commit()
#     # else:
#     #     answer_event = StudentAnswer.query.filter_by(seed=session['seed'], student=student).first()
#     if whether_graph:
#         points = session.get('user_points')
#         print('These are the points in session: ', points)
#         # print('This is what I think about the form: ', form)
#         graph = interpolator.Graph(points)
#         if points != []:
#             if not graph.vert:
#                 useranswer = graph.as_lambda
#             graph.gen_dict_for_svg()
#             user_poly_points = graph.poly_points
#         else:
#             useranswer = None
#         x_min = parameters['cart_x_min']
#         x_max = parameters['cart_x_max']
#         correct_answer_poly_points = question.get_svg_data([x_min, x_max])
#     else:
#         useranswer = form.answer.data
#         correct_answer_svg_data = ''
#     if form.validate_on_submit() and not (whether_graph and points == []):
#         # print('useranswer: ', useranswer)
#         if whether_graph and graph.vert:
#             correct = False
#         else:
#             correct = question.checkanswer(useranswer)
#         if current_user.is_authenticated:
#             user = current_user
#             answer_event = StudentAnswer(student=user,
#                                         skillname=question_name,
#                                         grade_category='check',
#                                         seed=session['seed'],
#                                         book=book_info.get('book'),
#                                         chapter=book_info.get('chapter'),
#                                         section=book_info.get('section'))
#             db.session.add(answer_event)
#         if correct:
#             message = 'You got it right!!'
#             if session['tried'] == True:
#                 message += " But you'll have to try a new problem to earn credit."
#             else:
#                 if current_user.is_authenticated:
#                     answer_event.correct = True
#                     db.session.commit()
#         else:
#             message = "If you want credit, you'll have to try a new problem."
#             if whether_graph:
#                 message = 'The correct answer is in <span style="color:green">green</span>.'
#             if current_user.is_authenticated:
#                 answer_event.correct = False
#                 db.session.commit()
#         session['tried'] = True
#     else:
#         if request.method == 'POST':
#             if session['tried'] == False:
#                 message = 'You can try again, since you just had a syntax error.'
#                 if (whether_graph and points == []):
#                     message = "You left it blank!  You may try again."
#             else:
#                 message = """You had a syntax error,
# but you should try a different problem if you want credit."""
#         else:
#             message = "It's a brand new problem!!"
#     # print('session user_points just before rendering', session.get('user_points'))
#     # print('current book: ', session.get('book'))
#     if session.get('section'):
#         new_question_name = random.choice(section.questions)
#         # print('new_question_name: ', new_question_name)
#     else:
#         new_question_name = question_name
#     if current_user.is_authenticated:
#         grade_info = UserSectionGradeInfo(user,
#                                         book.name_for_path,
#                                         int(chapter_number),
#                                         int(section_number))
#         # print('grade is:', grade_info.grade)
#     else:
#         grade_info = None
#     return render_template('question_page.html', user=user, title='Question',
#         site_name=app.config['SITE_NAME'], form=form, question=question,
#         tried=session['tried'], message=message, whether_graph=whether_graph,
#         parameters=parameters, question_name=new_question_name,
#         points=session.get('user_points'),
#         correct_answer_poly_points=correct_answer_poly_points,
#         user_poly_points=user_poly_points, grade_info=grade_info,
#         book_name=book_name, section_number=section_number,
#         chapter_number=chapter_number)



#########################
# Experiments
# @app.route("/simple.png")
# def simple():
#     fig = Figure()
#     ax = fig.add_subplot(111)
#     x = []
#     y = []
#     now = datetime.datetime.now()
#     delta = datetime.timedelta(days=1)
#     for i in range(10):
#         x.append(now)
#         now += delta
#         y.append(random.randint(0,1000))
#     ax.plot_date(x, y, '-')
#     ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
#     fig.autofmt_xdate()
#     canvas = FigureCanvas(fig)
#     png_output = io.BytesIO()
#     canvas.print_png(png_output)
#     response = make_response(png_output.getvalue())
#     response.headers['Content-Type'] = 'image/png'
#     return response

# @app.route('/tester', methods=['GET', 'POST'])
# def tester():
#     # svg_width = interpolator.svg_x_length
#     # svg_height = interpolator.svg_y_length
#     # cart_width = interpolator.cart_x_length
#     # cart_height = interpolator.cart_y_length
#     parameters = interpolator.get_parameters()
#     print('parameters: ', parameters, '; type is ', type(parameters))
#     if 'data' in request.form:
#         return_data = {}
#         points = request.form["data"]
#         # print(request.form["anchor"])
#         # try:
#         #     anchor = request.form["anchor"]
#         #     exec(f'anchor={anchor}')
#         #     print('anchor is ', anchor)
#         #     if type(anchor) != tuple:
#         #         del anchor
#         #         warning = """You have not entered a properly
#         #         formatted pair of coordinates.  Enter in "(x,y)" format."""
#         #         return_data["warning"] = warning
#         # except:
#         #     warning = """You have not entered a properly
#         #     formatted pair of coordinates.  Enter in "(x,y)" format."""
#         #     return_data["warning"] = warning
#         points = json.loads(points)
#         # print(points)
#         return_data.update(interpolator.get_dict_for_svg(points))
#         # print(return_data)
#         #return json.dumps(data)
#         return json.dumps(return_data)
#     return render_template('tester.html', parameters=parameters)

# @app.route('/handle_graph', methods=['GET', 'POST'])
def handle_graph():
    parameters = interpolator.get_parameters()
    # print('parameters: ', parameters, '; type is ', type(parameters))
    # if 'data' in request.form:
    return_data = {}
    points = session.get('user_points')
    print('handle_graph thinks points are ', type(points))
    #points = json.loads(points)
    # print(points)
    return_data.update(interpolator.get_dict_for_svg(points))
    print('handle_graph is getting ready to return ', return_data)
    return json.dumps(return_data)

@app.route('/real_line_tester')
def real_line_tester():
    return render_template('real_line_tester.html')
