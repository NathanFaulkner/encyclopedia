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
from pint import UnitRegistry
import inflect

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation)
# from app.interpolator import cart_x_to_svg, cart_y_to_svg

ureg = UnitRegistry()

inflector = inflect.engine()

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



class GenericTableHard(Question):
    """
    Given is table of data from function
    \\[
        f(x) = \\frac{delta_y}{delta_x}(x-x0) + y0
    \\]
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'x0' in 'kwargs':
            self.x0 = kwargs['x0']
        else:
            x0 = random.randint(-255,255)
            self.x0 = x0/10
        if 'y0' in 'kwargs':
            self.y0 = kwargs['y0']
        else:
            y0 = random.randint(-255,255)
            self.y0 = y0/10
        if 'delta_x' in kwargs:
            self.delta_x = kwargs['delta_x']
        else:
            self.delta_x = random_non_zero_integer(1,99)/10
        if 'delta_y' in kwargs:
            self.delta_y = kwargs['delta_y']
        else:
            self.delta_y = random_non_zero_integer(1,99)/10
        if 'l' in kwargs:
            self.l = kwargs['l']
        else:
            self.l = random.randint(6,10)
        x = Symbol('x')
        self.answer = self.y0 + self.delta_y/self.delta_x*(x - self.x0)
        self.m = self.delta_y/self.delta_x
        if self.m > 0:
            sign_m = '+'
        elif self.m < 0:
            sign_m = '-'
        else:
            sign_m = ''
        self.b = self.answer.coeff(x, 0)
        self.format_answer = """
        \(y =
            {y0} {sign} \\frac{{{delta_y}}}{{{delta_x}}}({expr})\)
        """.format(y0=self.y0,
                    delta_y=self.delta_y,
                    delta_x=self.delta_x,
                    sign=sign_m,
                    expr=latex(x - self.x0))
        # self.format_answer = f'\\( {latex(self.answer)} \\)'


        self.prompt_single = f"""
Consider the following table, depicting a relationship between \(x\) and \(y\).
"""

        prompt_multiple = f"""To be coded."""

        table_html = f"""
        <table border="1">
            <tr>
                <th>\(x\)</th>
        """
        for i in range(self.l + 1):
            table_html += f"""<td style="text-align: center;">{round(self.x0 + i*self.delta_x,1)}</td>"""
        table_html += f"""
            </tr>
            <tr>
                <th>\(y\)</th>
        """
        for i in range(self.l + 1):
            table_html += f"<td>{round(self.m * (self.delta_x * i) + self.y0, 1)}</td>"
        table_html += """
            </tr>
        </table>
        """
        self.table_html = table_html
        self.format_given = self.table_html

        tabular = "\\begin{tabular}{|l||"
        for i in range(self.l + 1):
            tabular += 'c|'
        tabular += '}\n\\hline\n'
        tabular += f' \\(x\\) & '
        for i in range(self.l + 1):
            tabular += f'{round(self.x0 + i*self.delta_x,1)} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n'
        tabular += f'\\(y\\) & '
        for i in range(self.l + 1):
            tabular += f'{round(self.m * (self.delta_x * i) + self.y0, 1)} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n\\end{tabular}'


        self.format_given_for_tex = f"""
Develop an equation that captures the relationship
between \(x\) and \(y\) that is represented
in this table.
\\smallskip

\\begin{{center}}
{tabular}
\\end{{center}}
\\smallskip

"""

    prob_type = 'math_blank'

    name = 'Harder Generic Table Problem'
    module_name = 'generic_table_hard'


    further_instruction = """Enter an equation that uses
    \(y\) and \(x\).  Also, the coefficients (numbers) in your equation
    have to be accurate to 4 decimal places.  Use exact figures
    wherever possible just in case.  But, as a helpful hint,
    you can enter things like, "-0.6/70" and the checking algorithm
    will be perfectly happy to do reduce this to a decimal for you.
    You DO NOT have to simplify your answer.
    """

    # loom_link = ""



    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        if 'y' not in user_answer:
            return False
        if 'x' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        y, x  = symbols('y x')
        user_answer = solve(user_answer, y)[0]
        user_answer_m = user_answer.coeff(x)
        user_answer_b = user_answer.coeff(x, 0)
        # print('m:', user_answer_m, self.m)
        return abs(user_answer_m - self.m) < 0.00005 and abs(user_answer_b - self.b) < 0.00005



    def format_useranswer(self, user_answer, display=False):
        if 'y' in user_answer:
            user_y = 'y'
        elif 'Y' in user_answer:
            user_y = 'Y'
        else:
            user_y = ''
        if 'x' in user_answer:
            user_x = 'x'
        elif 'X' in user_answer:
            user_x = 'X'
        else:
            user_x = ''
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        y, x  = symbols('y x')
        user_answer = solve(user_answer, y)[0]
        user_m = float(user_answer.coeff(x))
        user_b = float(user_answer.coeff(x, 0))
        sign = '+' if user_m >= 0 else '-'
        return f'\({user_y} = {user_b:.4f} {sign} {abs(user_m):.4f} {user_x}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            if 'y' in user_answer:
                user_y = 'y'
            elif 'Y' in user_answer:
                user_y = 'Y'
            else:
                user_y = ''
            if 'x' in user_answer:
                user_x = 'x'
            elif 'X' in user_answer:
                user_x = 'X'
            else:
                user_x = ''
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
            y, x  = symbols('y x')
            user_answer = solve(user_answer, y)[0]
            user_m = float(user_answer.coeff(x))
            user_b = float(user_answer.coeff(x, 0))
            # print('m:', user_answer_m, self.m)
            f'\({user_y} = {user_b:.4f} - {abs(user_m):.4f} {user_x}\)'
        except:
            raise SyntaxError






Question_Class = GenericTableHard
