from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt, math

from app import app, db, login, books

observers = db.Table('observers',
    db.Column('observer_id', db.Integer, db.ForeignKey('student.id')),
    db.Column('observed_id', db.Integer, db.ForeignKey('student.id'))
)

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.relationship('StudentAnswer', backref='student', lazy='dynamic')
    fav_color = db.Column(db.String(30))
    observed_students = db.relationship(
        'Student', secondary=observers,
        primaryjoin=(observers.c.observer_id == id),
        secondaryjoin=(observers.c.observed_id == id),
        backref=db.backref('observers', lazy='dynamic'), lazy='dynamic'
    )
    # Could add "super_user"
    # Could add "classcode" ... make view/function to generate unique class codes
    # on request, then view to add observer priviliges for each student
    # who adds the class code

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def name_as_observer(self, user):
        if not self.is_observed_by(user):
            self.observers.append(user)

    def remove_as_observer(self, user):
        if self.is_observed_by(user):
            self.observers.remove(user)

    def unobserve(self, user):
        if self.is_observing(user):
            self.observed_students.remove(user)

    def is_observing(self, user):
        return self.observed_students.filter(
            observers.c.observed_id == user.id).count() > 0

    def is_observed_by(self, user):
        return self.observers.filter(
            observers.c.observer_id == user.id).count() > 0

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                    algorithms=['HS256'])['reset_password']
        except:
            return
        return Student.query.get(id)

    def user_grade_info(self):
        return UserGradeInfo(self)

class BugReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_answer = db.Column(db.String(200))
    seed = db.Column(db.Float)
    question_name = db.Column(db.String)

class StudentAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_answer = db.Column(db.String(200))
    intended_answer = db.Column(db.String(200))
    correct = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    grade_category = db.Column(db.String(20)) #intended options are 'quiz', 'check', 'test', etc.
    skillname = db.Column(db.String) #aka: question_name
    seed = db.Column(db.Float)
    book = db.Column(db.String)
    chapter = db.Column(db.Integer)
    section = db.Column(db.Integer)

    def __repr__(self):
        return '<StudentAnswer {}: {} at {}>'.format(self.grade_category,
                    self.skillname, self.timestamp)

@login.user_loader
def load_user(id):
    return Student.query.get(int(id))

def get_user_books(user):
    answers = StudentAnswer.query.filter_by(user_id=user.id).all()
    books = []
    for answer in answers:
        # answer = answer.__dict__
        # book = answer.get('book')
        book = answer.book
        if book not in books and book is not None:
            books.append(book)
    return books


class UserSectionGradeInfo():
    def __init__(self, user, book, chapter, section):
        """book is really the name of the book;
        section and chapter are numbers from 1 to...
        """
        self.user = user
        self.book = book
        self.chapter = chapter
        self.section = section
        self.set_initial_due_date()
        self.grade = 0
        self.set_grade()


    def set_initial_due_date(self):
        book = getattr(books, self.book)
        main = book.subdivisions['main']
        chapter = main.subdivisions[self.chapter - 1]
        section = chapter.subdivisions[self.section - 1]
        self.initial_due_date = section.due_date
        if self.initial_due_date is not None:
            time_until_due_date = self.initial_due_date - datetime.utcnow()
            days_until_due_date = time_until_due_date.days + time_until_due_date.seconds/60/60/24
            self.memory_gradient = 1 - days_until_due_date
            if self.initial_due_date < datetime.utcnow():
                self.grade = 0


    max_grade = 4
    base = 2#math.sqrt(7) # This is supposed to model duration of memory factoring in past repetitions
    session_duration = 24

    def set_grade(self):
        self.next_due_date = self.initial_due_date
        answers_by_section = StudentAnswer.query.filter_by(user_id=self.user.id,
                                                            book=self.book,
                                                            chapter=self.chapter,
                                                            section=self.section)
        answers = answers_by_section.order_by(StudentAnswer.timestamp.asc()).all()
        if answers == []:
            return None
        grade = 0
        session_count = 0
        i = 0
        # mastery_session = True
        while i < len(answers):
            answer = answers[i]
            if i == 0:
                if answer.correct:
                    grade += 1
                i += 1
            else:
                prev_answer = answers[i - 1]
                time_since_previous = answer.timestamp - prev_answer.timestamp
                days_since_previous = time_since_previous.days + time_since_previous.seconds/60/60/24
                # print('chapter:', self.chapter,
                #         'section:', self.section,
                #         'try number:', i+1,
                #         'days since prev:', days_since_previous)
                new_session = days_since_previous > 0.5
                if new_session:
                    if grade == self.max_grade:
                        session_count += 1
                    expected_recall_duration = int(self.base**(session_count))
                    memory_decay_penalty = int(days_since_previous/expected_recall_duration)
                    grade = max(0, grade - memory_decay_penalty)
                #     if answer.correct:
                #         grade = min(self.max_grade, grade + 1)
                #     else:
                #         grade = max(0, grade - 1)
                # else:
                if answer.correct:
                    grade = min(self.max_grade, grade + 1)
                else:
                    grade = max(0, grade - 1)
                # print('chapter:', self.chapter, 'section:', self.section, 'try number:', i+1, 'grade:', grade)
                i += 1
        time_since_last = datetime.utcnow() - answers[-1].timestamp
        # print(datetime.utcnow())
        # print(answers[-1].timestamp)
        days_since_last = time_since_last.days + time_since_last.seconds/60/60/24
        # print('chapter:', self.chapter, 'section:', self.section, 'days since last:', days_since_last)
        expected_recall_duration = int(self.base**(session_count))
        # print('chapter:', self.chapter, 'section:', self.section, 'session count:', session_count)
        self.session_count = session_count
        self.memory_gradient = days_since_last/expected_recall_duration
        self.next_due_date = answers[-1].timestamp + timedelta(days=expected_recall_duration)
        memory_decay_penalty = int(days_since_last/expected_recall_duration)
        grade = max(0, grade - memory_decay_penalty)

        self.grade = grade


class UserGradeInfo():
    def __init__(self, user):
        self.user = user
        self.answers = StudentAnswer.query.filter_by(user_id=user.id).all()

    def get_book_names(self):
        answers = self.answers
        books = []
        for answer in answers:
            answer = answer.__dict__
            book = answer.get('book')
            if book not in books and book is not None:
                books.append(book)
        return books

    def get_books(self):
        user_books = []
        for book_name in self.get_book_names():
            book = getattr(books, book_name)
            user_books.append(book)
        return user_books

    def get_chapters(self, book):
        answers_by_book = StudentAnswer.query.filter_by(user_id=self.user.id,
                                                        book=book).all()
        chapters = []
        for answer in answers_by_book:
            answer = answer.__dict__
            chapter = answer.get('chapter')
            if chapter not in chapters and chapter is not None:
                chapters.append(chapter)
        return chapters

    def get_sections(self, book, chapter):
        answers_by_chapter = StudentAnswer.query.filter_by(user_id=self.user.id,
                                                        book=book,
                                                        chapter=chapter).all()
        sections = []
        for answer in answers_by_chapter:
            answer = answer.__dict__
            section = answer.get('section')
            if section not in sections and section is not None:
                sections.append(section)
        return sections

    def get_answers_by_section_desc(self, book, chapter, section):
        answers_by_section = StudentAnswer.query.filter_by(user_id=self.user.id,
                                                            book=book,
                                                            chapter=chapter,
                                                            section=section)
        answers = answers_by_section.order_by(StudentAnswer.timestamp.desc()).all()
        return answers

    def get_answers_by_section_asc(self, book, chapter, section):
        answers_by_section = StudentAnswer.query.filter_by(user_id=self.user.id,
                                                            book=book,
                                                            chapter=chapter,
                                                            section=section)
        answers = answers_by_section.order_by(StudentAnswer.timestamp.asc()).all()
        return answers

    max_grade = 4
    base = 2#math.sqrt(7) # This is supposed to model duration of memory factoring in past repetitions
    session_duration = 24

    def grade_section(self, book, chapter, section):
        grade_info = UserSectionGradeInfo(self.user, book, chapter, section)
        return grade_info

    def whole_book_info(self, book):
        info = []
        main = book.subdivisions['main']
        chapters = main.subdivisions
        for i, chapter in enumerate(chapters):
            chapter_info = []
            sections = chapter.subdivisions
            for j in range(len(sections)):
                chapter_info.append(self.grade_section(book.name_for_path, i+1, j+1))
            info.append(chapter_info)
        return info

    def get_whole_book_grade(self, book):
        whole_book_info = self.whole_book_info(book)
        grades = []
        for chapter in whole_book_info:
            for section_info in chapter:
                try:
                    grades.append(section_info.grade)
                except AttributeError:
                    pass
        return sum(grades)/len(grades)
