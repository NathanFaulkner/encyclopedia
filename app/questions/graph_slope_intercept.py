#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
# from sympy.parsing.sympy_parser import parse_expr
# from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
# transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *
import numpy as np
import json

from app.questions import Question, latex_print, random_non_zero_integer
from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general



prob_type = 'graph'

class GraphPointSlope(Question):
    """
    The given is of the form

    \\[
    y = Rational(p,q)x + b
    \\]

    The student is expected to graph by plotting points.  Two is sufficient.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'p' in kwargs:
            self.p = kwargs['p']
        else:
            self.p = random.randint(-5,5)
        if 'q' in kwargs:
            self.q = kwargs['q']
        else:
            self.q = random_non_zero_integer(-5,5)
        self.m = Rational(self.p, self.q)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.randint(-7,7)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        self.genproblem()

        # self.given = self.problem['given']
        # self.answer = self.problem['answer']

        self.given_latex = '\\(y = ' + latex(self.given) + '\\)'
        self.given_latex_display = '\\[y = ' + latex(self.given) + '\\]'
        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.given_latex_display}
        """
        self.format_answer = 'To be coded'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""{self.prompt_single}
            {self.given_latex}

        \\begin{{flishright}}
        \\includegraphics[scale=0.6]{{blank}}
        \\end{{flushright}}

        """

    name = 'Graph from Point Slope Form'
    module_name = 'graph_point_slope'

    prompt_single = """Graph the given equation by plotting at least two points
that satisfy the equation."""
    prompt_multiple = """Graph each of the following equations by plotting at least two points
that satisfy the equation."""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        b = self.b
        # p = self.p
        # q = self.q
        m = self.m
        expr = m*x + b
        self.as_lambda = lambda x: m*x + b
        self.given = expr
        #print('3rd step: So far its ', expr)
        self.answer = expr

    def get_svg_data(self, window):
        x_min = window[0]
        x_max = window[1]
        x_points = np.array([x_min, x_max])
        y_points = self.as_lambda(x_points)
        x_points = cart_x_to_svg(x_points)
        y_points = cart_y_to_svg(y_points)
        poly_points = ""
        l = len(x_points)
        i = 0
        while i < l:
            poly_points += f"{x_points[i]},{y_points[i]} "
            i += 1
        return poly_points


    def checkanswer(self, user_answer):
        user_answer = user_answer(self.x)
        return self.answer.equals(user_answer)

    # def useranswer_latex(self, user_answer, display=False):
    #     user_answer = user_answer.replace('^', '**')
    #     user_answer = parse_expr(user_answer, transformations=transformations)
    #     return latex_print(user_answer, display)

    # @classmethod
    # def validator(self, user_answer):
    #     try:
    #         user_answer = user_answer.replace('^', '**')
    #         user_answer = parse_expr(user_answer, transformations=transformations)
    #     except:
    #         raise SyntaxError



Question_Class = GraphPointSlope
