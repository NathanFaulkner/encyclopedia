#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *
import numpy as np
import json

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer)
from app.interpolator import cart_x_to_svg, cart_y_to_svg, get_parameters

from flask import render_template

# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general



prob_type = 'math_blank'

class HowManySolutionsToSystem(Question):
    """
    The given is a graph of an equation of the form

    \\[
        y  = value
    \\]
    or
    \\[
        x = value
    \\]

    kwarg orientation is either vert or horiz

    The answer is the equation.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'answer' in kwargs:
            self.answer = kwargs['answer']
        else:
            self.answer = random.choice([0, 1, oo])
        # self.p1 = random.randint(-5,5)
        # self.q1 = random.randint(1,6)
        # self.m1 = Rational(self.p1, self.q1)
        # self.b1 = random.randint(-8, 8)
        # self.p2 = random.randint(-5,5)
        # self.q2 = random.randint(1,6)
        # self.m2 = Rational(self.p2, self.q2)
        # self.b2 = random.randint(-8, 8)
        for i in ['1', '2']:
            exec(f'self.p{i} = random.randint(-5,5)')
            exec(f'self.q{i} = random.randint(1,6)')
            exec(f'self.m{i} = Rational(self.p{i}, self.q{i})')
            exec(f'self.b{i} = random.randint(-8, 8)')
        if self.answer == 1:
            while self.m1 == self.m2:
                self.p2 = random.randint(-5,5)
                self.q2 = random.randint(1,6)
                self.m2 = Rational(self.p2, self.q2)
        else:
            self.p2 = self.p1
            self.q2 = self.q1
            self.m2 = self.m1
            if self.answer == 0:
                while self.b1 == self.b2:
                    self.b2 = random.randint(-8, 8)
            else:
                self.b2 = self.b1

        self.d1 = random.choice([1, -1]) * int(random.triangular(1, 3, 1))
        self.d2 = random.choice([1, -1]) * int(random.triangular(1, 3, 1))
        if self.answer == oo:
            while self.d2 ==self.d1:
                self.d2 = random.choice([1, -1]) * int(random.triangular(1, 3, 1))

        x, y = symbols('x y')
        self.eq1 = Eq(-self.p1*self.d1*x + self.q1*self.d1*y,self.b1*self.q1*self.d1)
        self.eq2 = Eq(-self.p2*self.d2*x + self.q2*self.d2*y,self.b2*self.q2*self.d2)


        self.format_given = f"""
        \\[
            \\begin{{cases}}
                {latex(self.eq1)}\\\\
                {latex(self.eq2)}
            \\end{{cases}}
        \\]
        """

        self.format_answer = f'\({latex(self.answer)}\)'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
{self.prompt_single}
{self.format_given}
"""

    name = 'Equation for Vertical or Horizontal Line'
    module_name = 'vertical_or_horizontal_graph_to_equation'

    prompt_single = """How many solutions does the following system have?
    The possibilities are \(0\), \(1\), or \(\infty\)."""
    prompt_multiple = """TBA"""

    further_instruction = "Enter \(\infty\) as 'oo', where appropriate."


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'



    # has_img = True
    #
    # def save_img(self, filename):
    #     if self.orientation == 'vert':
    #         graph = GraphVert(self.value)
    #     else:
    #         graph = GraphHoriz(self.value)
    #     graph.save_fig(filename)

    # def get_svg_data(self, xwindow=[-10,10], ywindow=[-10,10]):
    #     x_min, x_max = xwindow
    #     y_min, y_max = ywindow
    #     if self.orientation == 'vert':
    #         x_points = np.array([self.value, self.value])
    #         y_points = np.array([y_min, y_max])
    #     else:
    #         x_points = np.array([x_min, x_max])
    #         y_points = np.array([self.value, self.value])
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
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return self.answer == user_answer

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return f'\({latex(user_answer)}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError



Question_Class = HowManySolutionsToSystem
