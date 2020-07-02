from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from time import time
import jwt

from app import app, db, login

class Student(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.relationship('StudentAnswer', backref='student', lazy='dynamic')
    fav_color = db.Column(db.String(30))

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
        return User.query.get(id)


class StudentAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_answer = db.Column(db.String(200))
    intended_answer = db.Column(db.String(200))
    correct = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    grade_category = db.Column(db.String(20)) #intended options are 'quiz', 'check', 'test', etc.
    skillname = db.Column(db.String)
    seed = db.Column(db.Float)

    def __repr__(self):
        return '<StudentAnswer {}: {} at {}>'.format(self.grade_category,
                    self.skillname, self.timestamp)

@login.user_loader
def load_user(id):
    return Student.query.get(int(id))
