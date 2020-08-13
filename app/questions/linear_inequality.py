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

class LinearInequality(Question):
    """
    The given is
    \\[
        a(x+b) + c(x+d) + ex + f Q 0,
    \\]
    but permuted with Q, where Q is an inequality.
    .  Terms are randomly allowed to collapse.
    A fraction, no solution, and all reals are possible.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'Q' in kwargs:
            self.Q = kwargs['Q']
        else:
            signs = ['\\leq', '\\geq', '\\lt', '\\gt']
            self.Q = random.choice(signs)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-9,9)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.randint(-9,9)
        if 'c' in kwargs:
            self.c = kwargs['c']
        else:
            self.c = random_non_zero_integer(-9,9)
        if 'd' in kwargs:
            self.d = kwargs['d']
        else:
            self.d = random.randint(-9,9)
        if 'e' in kwargs:
            self.e = kwargs['e']
        else:
            offset = random_non_zero_integer(-9,9)
            self.e = -(self.a + self.c) + offset
        if 'f' in kwargs:
            self.f = kwargs['f']
        else:
            offset = random_non_zero_integer(-9,9)
            self.f = -(self.a*self.b + self.c*self.d) + offset
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')
        if 'difficulty' in kwargs:
            self.difficulty = kwargs['difficulty']
        else:
            self.difficulty = random.choice([1, 1, 2, 3])

        self.genproblem()

        # self.given_latex = latex_print(self.given)
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        # self.format_answer = self.answer
    prob_type = 'math_blank'

    name = 'Linear Inequality'

    prompt_single = """Solve the linear inequality."""
    prompt_multiple = """Solve each of the following linear inequalities."""
    further_instruction = """Enter \\(\\leq\\) as "<=" and \\(\\geq\\)
    as ">=".  For instance, a possible answer might be "x <= -9/5".
    """


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
            Q = LinearInequality.switchQ(Q)
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

    @staticmethod
    def switchQ(Q):
        if Q == '\\lt':
            return '\\gt'
        if Q == '\\gt':
            return '\\lt'
        if Q == '\\geq':
            return '\\leq'
        if Q == '\\leq':
            return '\\geq'

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



Question_Class = LinearInequality
