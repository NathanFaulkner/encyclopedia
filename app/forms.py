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
        try:
            # user_answer = answer.data.replace('^', '**')
            # user_answer = parse_expr(user_answer, transformations=transformations)
            self.validator(answer.data)
        except:
            raise ValidationError('You have not used mathematically correct syntax.')
        # if answer.data == ',':
        #     raise ValidationError('Use proper syntax.')
