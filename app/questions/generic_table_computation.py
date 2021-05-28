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
# import numpy as np
# import json
# from pint import UnitRegistry
# import inflect

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation)
# from app.interpolator import cart_x_to_svg, cart_y_to_svg

# ureg = UnitRegistry()

# inflector = inflect.engine()

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



class GenericTableComputation(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'b' in 'kwargs':
            self.b = kwargs['b']
        else:
            b = random.randint(-255,255)
            self.b = b/10
        if 'm' in 'kwargs':
            self.m = kwargs['m']
        else:
            self.m = random_non_zero_integer(-99,99)/10
            # print(self.m)
        x = Symbol('x')
        self.formula = self.m * x + self.b
        self.input = random.randint(6,20)
        self.answer = self.formula.subs(x, self.input)
        self.format_answer = '\({}\)'.format(self.answer)

        self.prompt_single = f"""
Compute the value of \(y\) when \(x = {self.input}\)
        """

        prompt_multiple = f"""This needs some thinking...
        """

        self.genproblem()

    prob_type = 'math_blank'

    name = 'Table to Computation'
    module_name = 'generic_table_computation'


    # further_instruction = """Just enter the equation in a natural way.
    # """

    loom_link = "https://www.loom.com/share/8ff321d4b7434dc5b42f2536a9129132"

    def genproblem(self):
        table_html = f"""
        <table border="1">
            <tr>
                <th>\(x\)</th>
        """
        for i in range(5):
            table_html += f"""<td style="text-align: center;">{i}</td>"""
        table_html += f"""
            </tr>
            <tr>
                <th>\(y\)</th>
        """
        for i in range(5):
            table_html += f"<td>{round(self.m * i + self.b, 1)}</td>"
        table_html += """
            </tr>
        </table>
        """
        self.table_html = table_html
        self.format_given = self.table_html

        tabular = "\\begin{tabular}{|l||"
        for i in range(5):
            tabular += 'c|'
        tabular += '}\n\\hline\n'
        tabular += f' \\(x\\) & '
        for i in range(5):
            tabular += f'{i} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n'
        tabular += f'\\(y\\) & '
        for i in range(5):
            tabular += f'{round(self.m * i + self.b, 1)} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n\\end{tabular}'

        self.format_fragment_for_tex = tabular


        self.format_given_for_tex = f"""
{self.prompt_single}
\\smallskip

\\begin{{center}}
{tabular}
\\end{{center}}
\\smallskip

"""

    def checkanswer(self, user_answer):
        user_answer = user_answer.replace('y', ' ')
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return abs(user_answer - self.answer) < 0.0005

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.replace('y', ' ')
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return user_answer

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.replace('y', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            # if has_letters(user_answer):
            #     raise SyntaxError
            user_answer = parse_expr(user_answer, transformations=transformations)
            bool(abs(user_answer - 1) < 0.0005)
        except:
            raise SyntaxError






Question_Class = GenericTableComputation
