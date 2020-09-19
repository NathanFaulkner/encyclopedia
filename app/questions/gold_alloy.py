#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from flask_wtf import FlaskForm
# from wtforms import SubmitField, StringField, HiddenField
# from wtforms.validators import DataRequired, ValidationError, Email, \
#                 EqualTo, Length, InputRequired

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *
import numpy as np
# import json
from pint import UnitRegistry
import inflect

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation,
                            has_letters,
                            find_numbers)

ureg = UnitRegistry()
#
inflector = inflect.engine()
# from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general

# class RealLineForm(FlaskForm):
#     points = HiddenField(id="points_field")
#     intervals = HiddenField(id="intervals_field")
#     submit = SubmitField('Submit')

# form = RealLineForm

prob_type = 'math_blank'

class GoldAlloyProblem(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        self.high_pct = random.randint(60,99)
        self.low_pct = random.randint(40, self.high_pct-10)
        self.new_pct = random.randint(self.low_pct+3, self.high_pct-3)

        how_much = random.randint(1,10) * ureg.ounces
        self.mass_units = random.choice([ureg.ounces, ureg.grams])
        self.how_much = round(how_much.to(self.mass_units).magnitude, 1)

        A = [[1, 1],[self.low_pct, self.high_pct]]
        B = [self.how_much, self.how_much*self.new_pct]

        x, y = np.linalg.solve(A,B)
        self.amt_of_low = round(x, 2)#'hi'
        self.amt_of_high = round(y, 2) #'lo'

        self.format_answer = f"""
You would need {self.amt_of_high}
{inflector.plural(str(self.mass_units))} of the
higher percentage gold alloy and
{self.amt_of_low}
{inflector.plural(str(self.mass_units))} of the
lower percentage gold alloy.
"""
        self.prompt_single = f"""
Say that we have a quantity of <span style="color:red">{self.high_pct}%</span>
gold alloy (the rest is silver), and we want to mix it with a
<span style="color:red">{self.low_pct}%</span> gold alloy to create a portion of
<span style="color:red">{self.new_pct}%</span> gold alloy.
If we want <span style="color:red">{self.how_much}
{inflector.plural(str(self.mass_units))}</span> of
the <span style="color:red">{self.new_pct}%</span> gold alloy,
how much of each of the original alloys should we combine?
You may round your answer to two decimal places,
as long as you don't round until the very last step.
(Use exact fractions until the last step.)
"""

        self.format_given_for_tex = f"""
Say that we have a quantity of {self.high_pct}\%
gold alloy (the rest is silver), and we want to mix it with a
{self.new_pct}\% gold alloy.
If we want {self.how_much}
{inflector.plural(str(self.mass_units))} of
the {self.new_pct}\% gold alloy,
how much of each of the original alloys should we combine?
You may round your answer to two decimal places,
as long as you don't round until the very last step.
(Use exact fractions until the last step.)
"""
        self.further_instruction = f"""
Enter your answer as
"<span style="color:red">{inflector.plural(str(self.mass_units))}</span> needed of higher percentage alloy,
<span style="color:red">{inflector.plural(str(self.mass_units))}</span> needed of lower percentage alloy".
For instance, you answer might be "2, 3".
The point is, you must separate the values by a comma and list
the amount needed of the higher percentage alloy first!  Also, do NOT use commas
to format your numbers.  For instance, if you need
1,000 <span style="color:red">{inflector.plural(str(self.mass_units))}</span> of one alloy, enter "1000" not "1,000".
Otherwise you'll either
get a syntax error or, possibly, the checker will misunderstand your intent.
"""

    prob_type = 'math_blank'

    name = 'Gold Alloy Problem'
    module_name = 'gold_alloy'

    prompt_multiple = """TBA
    """
    # loom_link = ""

    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        if self.mass_units == ureg.ounces:
            bad_units = [' g ', ' grams ', ' gram ']
            for unit in bad_units:
                if unit in user_answer:
                    return False
        else:
            bad_units = [' oz ', ' ounces ', ' ounce ']
            for unit in bad_units:
                if unit in user_answer:
                    return False
        user_answer = user_answer.replace('%', '')
        user_answer = user_answer.replace('^', '**')
        user_answer = user_answer.replace('(', '')
        user_answer = user_answer.replace(')', '')
        if ',' not in user_answer and ' and' not in user_answer:
            return False
        if len(user_answer.split(',')) > 1:
            user_x, user_y = user_answer.split(',')
        elif len(user_answer.split(' and')) > 1:
            user_x, user_y = user_answer.split(' and')
        if ' y ' in user_x:
            user_x, user_y = [user_y, user_x]
        elif ' low' in user_x or 'low ' in user_x or 'lower ' in user_x or ' lower' in user_x:
            user_x, user_y = [user_y, user_x]
        if ' x ' in user_x or 'x=' in user_x:
            i = user_x.find('x')
            user_x = user_x[i+1:]
            i = user_x.find('=')
            user_x = user_x[i+1:]
            user_x = user_x.replace(' ', '')
            user_x = parse_expr(user_x, transformations=transformations)
        elif ' high' in user_x or 'high ' in user_x or 'higher ' in user_x or ' higher' in user_x:
            user_x = find_numbers(user_x)
        else:
            user_x = user_x.replace(' ', '')
            user_x = parse_expr(user_x, transformations=transformations)
        if ' y ' in user_y or 'y=' in user_y:
            i = user_y.find('y')
            user_y = user_y[i+1:]
            i = user_y.find('=')
            user_y = user_y[i+1:]
            user_y = user_y.replace(' ', '')
            user_y = parse_expr(user_y, transformations=transformations)
        elif ' low' in user_y or 'low ' in user_y or 'lower ' in user_y or ' lower' in user_y:
            user_y = find_numbers(user_y)
        else:
            user_y = user_y.replace(' ', '')
            user_y = parse_expr(user_y, transformations=transformations)
        return abs(user_y - self.amt_of_low) < 0.005 and abs(user_x - self.amt_of_high) < 0.005

    def format_useranswer(self, user_answer, display=False):
        # user_answer = user_answer.lower()
        if has_letters(user_answer):
            return user_answer
        else:
            return f'\({user_answer}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('%', '')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('(', '')
            user_answer = user_answer.replace(')', '')
            if ',' not in user_answer and ' and' not in user_answer:
                raise SyntaxError
            if len(user_answer.split(',')) > 1:
                user_x, user_y = user_answer.split(',')
            elif len(user_answer.split(' and')) > 1:
                user_x, user_y = user_answer.split(' and')
            if ' y ' in user_x or 'y=' in user_x:
                user_x, user_y = [user_y, user_x]
            elif ' low' in user_x or 'low ' in user_x or 'lower ' in user_x or ' lower' in user_x:
                user_x, user_y = [user_y, user_x]
            if ' x ' in user_x or 'x=' in user_x:
                i = user_x.find('x')
                user_x = user_x[i+1:]
                i = user_x.find('=')
                user_x = user_x[i+1:]
                user_x = user_x.replace(' ', '')
                user_x = parse_expr(user_x, transformations=transformations)
            elif ' high' in user_x or 'high ' in user_x or 'higher ' in user_x or ' higher' in user_x:
                user_x = find_numbers(user_x)
            else:
                user_x = user_x.replace(' ', '')
                user_x = parse_expr(user_x, transformations=transformations)
            if ' y ' in user_y:
                i = user_y.find('y')
                user_y = user_y[i+1:]
                i = user_y.find('=')
                user_y = user_y[i+1:]
                user_y = user_y.replace(' ', '')
                user_y = parse_expr(user_y, transformations=transformations)
            elif ' low' in user_y or 'low ' in user_y or 'lower ' in user_y or ' lower' in user_y:
                user_y = find_numbers(user_y)
            else:
                user_y = user_y.replace(' ', '')
                user_y = parse_expr(user_y, transformations=transformations)
        except:
            raise SyntaxError






Question_Class = GoldAlloyProblem
