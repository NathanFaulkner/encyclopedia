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
            m = 0
            while m == 0:
                m = round(self.size/10, 1) + random.choice([-0.5, -0.25, 0, 0.25, 0.5])
            self.m = m
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
        self.format_answer = f'\(P = {latex({self.answer})}\)'

        self.genproblem()

    prob_type = 'math_blank'

    name = 'Basic Function from a Table'
    module_name = 'basic_function_from_table'

    prompt_single = """Develop an equation that relates the price of the pizza
    to the number of toppings you order.  Use the letter \(P\) for
    the price of the pizza.  Use the letter \(n\) for the number
    of toppings you use."""
    prompt_multiple = """For each of the following tables,
    develop an equation that relates the price of the pizza
    to the number of toppings you order.  Use the letter \(P\) for
    the price of the pizza.  Use the letter \(n\) for the number
    of toppings you use.
    """
    further_instruction = """Just enter the equation in a natural way.
    """

    # loom_link = ""

    def genproblem(self):
        table_html = f"""
        <table>
            <tr>
                <th>Number of toppings</th>
        """
        for i in range(5):
            table_html += f"<td>{i}</td>"
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
        for i in range(self.l):
            tabular += 'c|'
        tabular += '}\n\\hline\n'
        tabular += f' \(y\) & '
        for i in range(self.l):
            tabular += f'{self.m * i + self.b} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n'
        tabular += f'Temperature (in {temp_abbrev[self.temp_unit]}) & '
        for i in range(self.l):
            tabular += f'{round(self.m * (alt_delta *i) + self.lower_temp.magnitude, 1)} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n\\end{tabular}'


        self.format_given_for_tex = f"""
{self.prompt_single}
\\smallskip

{tabular}
\\smallskip

Using a linear model based on this data,
predict the temperature at an altitude of {self.input}
{inflector.plural(str(self.alt_unit))}.  Include units in the following way:
Enter the numerical part of your answer, then a space, and then
`F' for Fahrenheit, `C' for Celsius, `m' for meters, or `ft' for feet,
whichever is applicable.
"""

    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer.replace('y', 'p')
        if 'p' not in user_answer:
            return False
        user_answer.replace('x', 'n')
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
            user_p = None
        if 'n' in user_answer:
            user_n = 'n'
        elif 'N' in user_answer:
            user_n = 'N'
        elif 'x' in user_answer:
            user_n = 'x'
        elif 'X' in user_answer:
            user_n = 'X'
        else:
            user_n = None
        user_answer = user_answer.lower()
        user_answer.replace('y', 'p')
        if 'p' not in user_answer:
            return False
        user_answer.replace('x', 'n')
        if 'n' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        p = Symbol('p')
        user_answer = solve(user_answer, p)[0]
        return f'{user_p} = {latex(user_answer)}'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer.replace('y', 'p')
            if 'p' not in user_answer:
                return False
            user_answer.replace('x', 'n')
            if 'n' not in user_answer:
                return False
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
            p = Symbol('p')
            user_answer = solve(user_answer, p)[0]
        except:
            raise SyntaxError



class BasicFunctionFromTable(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        Q = random.choice([PizzaProblem])


        self.genproblem()

        # self.given_latex = latex_print(self.given)
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        # self.format_answer = self.answer
    prob_type = 'math_blank'

    name = 'Linear Inequality'
    module_name = 'linear_inequality'

    prompt_single = """Solve the linear inequality."""
    prompt_multiple = """Solve each of the following linear inequalities."""
    further_instruction = """Enter \\(\\leq\\) as "<=" and \\(\\geq\\)
    as ">=".  For instance, a possible answer might be "x <= -9/5".
    """

    # loom_link = ""

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f
        if self.difficulty == 2:
            term1 = factor(a*(x+b))
        else:
            term1 = a*(x+b)
        if self.difficulty == 3:
            term2 = factor(c*(x+d))
        else:
            term2 = c*(x+d)
        terms = [term1, term2, e*x, f]
        LHS, RHS = permute_equation(terms, as_list=True)
        Q = self.Q
        self.given_latex_display = f'\\[ \n \t {latex(LHS)} {Q} {latex(RHS)} \n \\]'
        self.format_given = self.given_latex_display
        self.format_given_for_tex = f"""
        {self.prompt_single}

        \\[ \n \t {latex(LHS)} {Q} {latex(RHS)} \n \\]
        """
        self.given = [LHS, RHS]
        #print('3rd step: So far its ', expr)
        bdry = Rational(-(a*b+c*d+f), a+c+e)
        if a + c + e < 0:
            Q = BasicFunctionFromTable.switchQ(Q)
        if Q == '\\lt':
            self.answer = Interval.Ropen(-oo, bdry)
            self.ineq_answer = x < bdry
        if Q == '\\leq':
            self.answer = Interval(-oo, bdry)
            self.ineq_answer = x <= bdry
        if Q == '\\gt':
            self.answer = Interval.Lopen(bdry, oo)
            self.ineq_answer = x > bdry
        if Q == '\\geq':
            self.answer = Interval(bdry, oo)
            self.ineq_answer = x >= bdry
        self.format_answer = f'\\( x {Q} {latex(bdry)} \\)'

    # def get_svg_data(self, window):
    #     x_min = window[0]
    #     x_max = window[1]
    #     x_points = np.array([x_min, x_max])
    #     y_points = self.as_lambda(x_points)
    #     x_points = cart_x_to_svg(x_points)
    #     y_points = cart_y_to_svg(y_points)
    #     poly_points = ""
    #     l = len(x_points)
    #     i = 0
    #     while i < l:
    #         poly_points += f"{x_points[i]},{y_points[i]} "
    #         i += 1
    #     return poly_points


    def checkanswer(self, user_answer):
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return self.ineq_answer.equals(user_answer)


    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return latex_print(user_answer, display)

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError



Question_Class = BasicFunctionFromTable
