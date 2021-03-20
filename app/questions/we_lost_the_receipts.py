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
import json

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation,
                            has_letters,
                            find_numbers)
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

class WeLostTheReceipts(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        self.total_tix = random.randint(5000,11000)
        self.adult_tix = random.randint(int(0.25*self.total_tix), int(0.5*self.total_tix))
        self.kid_tix = self.total_tix - self.adult_tix

        self.cost_kid = random.randint(4,8)
        self.cost_adult = random.randint(9,15)

        self.total_rev = self.cost_kid*self.kid_tix + self.cost_adult*self.adult_tix
        self.format_answer = f"""
{self.kid_tix} kid tickets, {self.adult_tix} adult tickets"""

        self.prompt_single = f"""
"We lost the receipts": For the opening day of the fair,
(let's say that) {'{:,}'.format(self.total_tix)}
admission tickets were sold.
The receipts totaled ${'{:,}'.format(self.total_rev)}.
Tickets for children cost ${self.cost_kid} each and adults cost
${self.cost_adult} each.   How many of each type of ticket were sold?
"""

        self.format_given_for_tex = f"""
``We lost the receipts'': For the opening day of the fair,
(let's say that) {'{:,}'.format(self.total_tix)}
admission tickets were sold.
The receipts totaled \${'{:,}'.format(self.total_rev)}.
Tickets for children cost \${self.cost_kid} each and adults cost
\${self.cost_adult} each.   How many of each type of ticket were sold?
"""

    prob_type = 'math_blank'

    name = 'We Lost the Receipts from the Fair'
    module_name = 'we_lost_the_receipts'


    prompt_multiple = """TBA
    """
    further_instruction = """Enter your answer as
"number of kids tickets sold, number of adults tickets sold".
For instance, you answer might be "1234, 5678"
The point is, you must separate the values by a comma and list
the number of kid's tickets sold first!  Also, do NOT use commas
to format your numbers.  For instance, if 1,000 kid tickets
were sold, type "1000" not "1,000".  Otherwise you'll either
get a syntax error or, possibly, the checker will misunderstand your intent.
    """

    # loom_link = ""






    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = user_answer.replace('(', '')
        user_answer = user_answer.replace(')', '')
        user_answer = user_answer.replace("'", '')
        user_answer = user_answer.replace('childrens', 'kids')
        if ',' not in user_answer and ' and' not in user_answer:
            return False
        if len(user_answer.split(',')) > 1:
            user_x, user_y = user_answer.split(',')
        elif len(user_answer.split(' and')) > 1:
            user_x, user_y = user_answer.split(' and')
        if 'y' in user_x:
            user_x, user_y = [user_y, user_x]
        elif 'adult' in user_x:
            user_x, user_y = [user_y, user_x]
        if ' x ' in user_x or 'x=' in user_x:
            i = user_x.find('x')
            user_x = user_x[i+1:]
            i = user_x.find('=')
            user_x = user_x[i+1:]
            user_x = user_x.replace(' ', '')
            user_x = parse_expr(user_x, transformations=transformations)
        elif 'kid' in user_x:
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
        elif 'adult' in user_y:
            user_y = find_numbers(user_y)
        else:
            user_y = user_y.replace(' ', '')
            user_y = parse_expr(user_y, transformations=transformations)
        return user_y == self.adult_tix and user_x == self.kid_tix

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
            elif 'adult' in user_x:
                user_x, user_y = [user_y, user_x]
            if ' x ' in user_x or 'x=' in user_x:
                i = user_x.find('x')
                user_x = user_x[i+1:]
                i = user_x.find('=')
                user_x = user_x[i+1:]
                user_x = user_x.replace(' ', '')
                user_x = parse_expr(user_x, transformations=transformations)
            elif 'kid' in user_x:
                user_x = find_numbers(user_x)
            else:
                user_x = user_x.replace(' ', '')
                user_x = parse_expr(user_x, transformations=transformations)
            if 'y' in user_y:
                i = user_y.find('y')
                user_y = user_y[i+1:]
                i = user_y.find('=')
                user_y = user_y[i+1:]
                user_y = user_y.replace(' ', '')
                user_y = parse_expr(user_y, transformations=transformations)
            elif 'adult' in user_y:
                user_y = find_numbers(user_y)
            else:
                user_y = user_y.replace(' ', '')
                user_y = parse_expr(user_y, transformations=transformations)
        except:
            raise SyntaxError






Question_Class = WeLostTheReceipts
