from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, \
                EqualTo, Length, InputRequired
from app.models import Student, StudentAnswer

from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))

class AnswerForm(FlaskForm):
    def __init__(self, validator, *args, **kwargs):
        #super(AnswerForm, self)
        super().__init__(*args, **kwargs)
        self.validator = validator

    seed = HiddenField()
    answer = StringField('Answer', validators=[InputRequired()], id="useranswer")
    submit = SubmitField('Submit')


    def validate_answer(self, answer):
        if 'simplify' in answer.data or 'factor' in answer.data or 'solve' in answer.data:
            raise ValidationError('A++ thinking!  But, sorry, not allowed.')
        try:
            # user_answer = answer.data.replace('^', '**')
            # user_answer = parse_expr(user_answer, transformations=transformations)
            # if 'simplify' in answer:
            #     raise ValidationError('A++ thinking!  But not allowed.')
            self.validator(answer.data)
        except:
            raise ValidationError('You have not used intelligible syntax.')
        # if answer.data == ',':
        #     raise ValidationError('Use proper syntax.')

class BlankForm(FlaskForm):
    seed = HiddenField()
    submit = SubmitField('Submit', id='submitter')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = Student.query.filter_by(username=username.data.strip()).first()
        if user is not None:
            raise ValidationError('This user name is already in use. \
            Please use another name.')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already in use. \
            Please use another email.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password',
            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class ResetEmailForm(FlaskForm):
    email = StringField('Enter New Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Email')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already in use. \
            Please use another email.')

class ReportBugForm(FlaskForm):
    seed = HiddenField()
    user_answer = HiddenField(id="bug_answer")
    question_name = HiddenField()
    submit = SubmitField('Report Bug')

class RealLineForm(FlaskForm):
    points = HiddenField(id="points_field")
    intervals = HiddenField(id="intervals_field")
    submit = SubmitField('Submit')
