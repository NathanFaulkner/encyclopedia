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
                            permute_equation)
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

class PizzaProblem(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'size' in kwargs:
            self.size= kwargs['size']
        else:
            sizes = [8, 10, 12, 15, 18, 20]
            self.size = random.choice(sizes)
        if 'b' in 'kwargs':
            self.b = kwargs['b']
        else:
            self.b = self.size + random.randint(-3,3) + random.choice([-0.5, 0, 0.5])
        if 'm' in 'kwargs':
            self.m = kwargs['m']
        else:
            self.m = round(self.size/10, 0) + random.choice([-0.5, -0.25, 0, 0.25, 0.5])
        if self.size == 8:
            self.size_display = random.choice(['8"', 'small'])
        elif self.size == 12:
            self.size_display = random.choice(['12"', 'medium'])
        elif self.size == 18:
            self.size_display = random.choice(['18"', 'large'])
        elif self.size == 20:
            self.size_display = random.choice(['20"', 'extra-large'])
        else:
            self.size_display = f'{self.size}"'
        n = Symbol('n')
        self.answer = self.m * n + self.b
        self.format_answer = f'\(P = {latex(self.answer)}\)'

        self.prompt_single = f"""
        The following table depicts the price of a {self.size_display} pizza
        depending on the number of toppings you order.
        Develop an equation that relates the price of the pizza
        to the number of toppings.  Use the letter \(P\) for
        the price of the pizza.  Use the letter \(n\) for the number
        of toppings you use."""

        self.genproblem()

    prob_type = 'math_blank'

    name = 'Pizza Problem'
    module_name = 'pizza_problem'


    prompt_multiple = """For each of the following tables,
    develop an equation that relates the price of the pizza
    to the number of toppings you order.  Use the letter \(P\) for
    the price of the pizza.  Use the letter \(n\) for the number
    of toppings you use.
    """
    further_instruction = """Just enter the equation in a natural way.
    """

    loom_link = "https://www.loom.com/share/8ff321d4b7434dc5b42f2536a9129132"

    def genproblem(self):
        table_html = f"""
        <table border="1">
            <tr>
                <th>Number of toppings</th>
        """
        for i in range(5):
            table_html += f"""<td style="text-align: center;">{i}</td>"""
        table_html += """
            </tr>
            <tr>
                <th>Price of Pizza (in $)</th>
        """
        for i in range(5):
            table_html += f"<td>{self.m * i + self.b}</td>"
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
        tabular += f' Number of toppings & '
        for i in range(5):
            tabular += f'{i} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n'
        tabular += f'Price of Pizza (in \\$) & '
        for i in range(5):
            tabular += f'{self.m * i + self.b} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n\\end{tabular}'


        self.format_given_for_tex = f"""
{self.prompt_single}
\\smallskip

{tabular}
\\smallskip
"""

    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('y', 'p')
        user_answer = user_answer.replace('x', 'n')
        if 'p' not in user_answer:
            return False
        if 'n' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        p = Symbol('p')
        user_answer = solve(user_answer, p)[0]
        return self.answer.equals(user_answer)


    def format_useranswer(self, user_answer, display=False):
        if 'p' in user_answer:
            user_p = 'p'
        elif 'P' in user_answer:
            user_p = 'P'
        elif 'y' in user_answer:
            user_p = 'y'
        elif 'Y' in user_answer:
            user_p = 'Y'
        else:
            user_p = ''
        if 'n' in user_answer:
            user_n = 'n'
        elif 'N' in user_answer:
            user_n = 'N'
        elif 'x' in user_answer:
            user_n = 'x'
        elif 'X' in user_answer:
            user_n = 'X'
        else:
            user_n = ''
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('y', 'p')
        user_answer = user_answer.replace('x', 'n')
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        p = Symbol('p')
        user_answer = solve(user_answer, p)[0]
        return f'\({user_p} = {latex(user_answer)}\)'.replace('n', user_n)

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('y', 'p')
            user_answer = user_answer.replace('x', 'n')
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
            p = Symbol('p')
            user_answer = solve(user_answer, p)[0]
        except:
            raise SyntaxError






Question_Class = PizzaProblem
