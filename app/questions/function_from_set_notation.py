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
                            fix_quotes_for_tex)
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

class FunctionFromSetNotation(Question):
    """
    The given is
    \\[
        symbol = \{(x_0, y_0, ...)\}
    \\]
    a set of ordered pairs of length l (4 to 6).

    Symbol is f, g, or h

    The task is to either state "not a function"
    or to compute a value or its domain or its range.
    Key words are 'mode' = 'compute', 'domain', or 'range'

    Another key word: 'force_function'

    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'l' in kwargs:
            self.l = kwargs['l']
        else:
            self.l = random.randint(4, 5)
        if 'mode' in kwargs:
            self.mode = kwargs['mode']
        else:
            self.mode = random.choice(['compute', 'domain', 'range'])
        if 'symbol' in kwargs:
            self.symbol = kwargs['symbol']
        else:
            self.symbol = random.choice(['f', 'g', 'h'])
        if 'force_function' in kwargs:
            self.force_function = kwargs['force_function']
        else:
            self.force_function = random.choice([True, False])
        if 'force_function' in kwargs:
            self.force_not_function = kwargs['force_not_function']
        else:
            self.force_not_function = random.choice([True, False])

        self.genproblem()

        # self.given_latex = latex_print(self.given)
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        # self.format_answer = self.answer
    prob_type = 'math_blank'

    name = 'Function from Set Notation'
    module_name = 'function_from_set_notation'



    # loom_link = "https://www.loom.com/share/5028da702f8143568d2762e7a47d64db"


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        symb = self.symbol
        l = self.l
        mode = self.mode
        force_function = self.force_function
        # force_not_function = self.force_not_function
        f = []
        for i in range(l):
            x = random.randint(-10,10)
            domain = [p[0] for p in f]
            if force_function:
                while x in domain:
                    x = random.randint(-10,10)
            f.append((x, random.randint(-10,10)))
        self.f = set(f)
        self.is_function = len(domain) == len(set(domain))
        prompt_single = """Consider the relation (set of ordered pairs)
        defined here.  If it is not a function, answer "not a function".
        Otherwise, """
        domain = [p[0] for p in f]
        self.domain = set(domain)
        f_range = [p[1] for p in f]
        self.range = set(f_range)
        format_given = f'\\[ {self.symbol} = \\{{ '
        for p in f:
            format_given += f'({p[0]}, {p[1]}),'
        format_given = format_given[:-1]
        format_given += '\\} \\]'
        self.format_given = format_given
        if not self.is_function:
            self.format_answer = 'not a function'
        if mode == 'compute':
            input = random.choice(domain)
            prompt_single += f"compute the value of \({self.symbol}({input})\)."
            self.input = input
            self.further_instruction = f"""Do NOT include "{self.symbol}({input})"
            in your answer.
            """
            if self.is_function:
                self.answer = dict(f)[input]
                self.format_answer = f'\({self.answer}\)'
        elif mode == 'domain':
            prompt_single += """give the domain of the function.
            Use set notation or list the elements."""
            if self.is_function:
                self.answer = self.domain
                self.format_answer = f'\( {latex(self.answer)} \)'
        else:
            prompt_single += """give the range of the function.
            Use set notation or list the elements.
            """
            if self.is_function:
                self.answer = self.range
                self.format_answer = f'\( {latex(self.answer)} \)'

        self.prompt_single = prompt_single

        self.prompt_multiple = """This would need to be rethought."""

        tex_prompt = fix_quotes_for_tex(self.prompt_single)
        self.format_given_for_tex = f"""
{tex_prompt}
{self.format_given}
            """





    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        if self.is_function:
            if 'not' in user_answer:
                return False
            else:
                if self.mode == 'compute':
                    user_answer = user_answer.replace(' ', '')
                    user_answer = user_answer.replace(f'f({str(self.input)})', '')
                    user_answer = user_answer.replace('=','')
                    if user_answer.isnumeric():
                        user_answer = int(user_answer)
                    return user_answer == self.answer
                elif self.mode == 'domain':
                    if 'range' in user_answer:
                        return False
                    user_answer = user_answer.replace('domain','')
                    user_answer = user_answer.replace('dom','')
                    user_answer = user_answer.replace('d','')
                    user_answer = user_answer.replace('the','')
                    user_answer = user_answer.replace('is','')
                    user_answer = user_answer.replace(' ', '')
                    user_answer = user_answer.replace('=','')
                    user_answer = user_answer.replace('{','')
                    user_answer = user_answer.replace('}','')
                    user_answer = user_answer.split(',')
                    user_answer = [int(ans) for ans in user_answer]
                    user_answer = set(user_answer)
                    return user_answer == self.answer
                else:
                    if 'domain' in user_answer:
                        return False
                    user_answer = user_answer.replace('range','')
                    user_answer = user_answer.replace('r','')
                    user_answer = user_answer.replace('the','')
                    user_answer = user_answer.replace('is','')
                    user_answer = user_answer.replace(' ', '')
                    user_answer = user_answer.replace('=','')
                    user_answer = user_answer.replace('{','')
                    user_answer = user_answer.replace('}','')
                    user_answer = user_answer.split(',')
                    user_answer = [int(ans) for ans in user_answer]
                    user_answer = set(user_answer)
                    return user_answer == self.answer
        else:
            if 'not' in user_answer:
                return True




    def format_useranswer(self, user_answer, display=False):
        return user_answer

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('domain','')
            user_answer = user_answer.replace('dom','')
            user_answer = user_answer.replace('d','')
            user_answer = user_answer.replace('range','')
            user_answer = user_answer.replace('r','')
            user_answer = user_answer.replace('the','')
            user_answer = user_answer.replace('is','')
            user_answer = user_answer.replace(' ', '')
            user_answer = user_answer.replace('=','')
            user_answer = user_answer.replace('{','')
            user_answer = user_answer.replace('}','')
            if 'not' not in user_answer:
                user_answer = user_answer.split(',')
                user_answer = [int(ans) for ans in user_answer]
                user_answer = set(user_answer)
        except:
            raise SyntaxError



Question_Class = FunctionFromSetNotation
