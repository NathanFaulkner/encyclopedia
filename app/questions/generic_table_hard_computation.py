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



class GenericTableHardComputation(Question):
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
        input = random.choice([self.x0 - self.delta_x*random.randint(10,100)/10,
                        self.x0 + self.l*self.delta_x + self.delta_x*random.randint(10,100)/10])
        self.input = round(input, 1)
        self.float_answer = self.answer.subs(x, self.input)
        self.m = self.delta_y/self.delta_x
        if self.m > 0:
            sign_m = '+'
        elif self.m < 0:
            sign_m = '-'
        else:
            sign_m = ''
        self.b = self.answer.coeff(x, 0)
        self.format_answer = f"""
        \(
            {self.float_answer}
        \)
        """
        # self.format_answer = f'\\( {latex(self.answer)} \\)'


        self.prompt_single = f"""
        Develop an equation that captures the relationship between the variables
        \(x\) and \(y\) represented in the following table.
        ."""

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

        self.further_instruction = f"""Using a linear model based on this data,
        predict the value of \(y\)
        when \(x = {self.input} \).
        """

        self.format_given_for_tex = 'Under construction'

    prob_type = 'math_blank'

    name = 'Harder Generic Table Computation'
    module_name = 'generic_table_hard_computation'




    # loom_link = ""



    def checkanswer(self, user_answer):
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        # print(abs(user_answer - self.float_answer) < 0.0005, self.checkunits(user_units))
        # print(us)
        return abs(user_answer - self.float_answer) < 0.0005


    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return f'\({latex(user_answer)}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            float(user_answer)
        except:
            raise SyntaxError







Question_Class = GenericTableHardComputation
