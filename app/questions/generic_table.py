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



class GenericTable(Question):
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
        self.answer = self.m * x + self.b
        self.format_answer = f'\(y = {latex(self.answer)}\)'

        self.prompt_single = f"""
        Develop an equation that captures the relationship between \(x\)
        and \(y\).
        """

        prompt_multiple = f"""For each of the following tables,
        develop an equation that captures the relationship between \(x\)
        and \(y\).
        """

        self.genproblem()

    prob_type = 'math_blank'

    name = 'Table to Formula'
    module_name = 'generic_table'


    further_instruction = """Just enter the equation in a natural way.
    """

    # loom_link = ""

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
        y = Symbol('y')
        user_answer = solve(user_answer, y)[0]
        return self.answer.equals(user_answer)


    def format_useranswer(self, user_answer, display=False):
        if 'y' in user_answer:
            user_y = 'y'
        elif 'Y' in user_answer:
            user_y = 'Y'
        else:
            user_y = None
        if 'x' in user_answer:
            user_x = 'x'
        elif 'X' in user_answer:
            user_x = 'X'
        else:
            user_n = None
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        return f'\({latex(lhs)} = {latex(rhs)}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
            y = Symbol('y')
            user_answer = solve(user_answer, y)[0]
        except:
            raise SyntaxError






Question_Class = GenericTable
