#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
# from sympy.parsing.sympy_parser import parse_expr
# from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
# transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *
import numpy as np
import json

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            GraphFromLambda)
from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general



prob_type = 'graph'

class GraphStandardFormLine(Question):
    """
    The given is of the form

    \\[
     bdx + ady = abd
    \\]


    Intercepts are a and b.

    The student is expected to graph by plotting points.  Two is sufficient.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-8,8)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random_non_zero_integer(-8,8)
        if 'd' in kwargs:
            self.d = kwargs['d']
        else:
            self.d = random_non_zero_integer(-8,8)
        self.m = -Rational(self.b, self.a)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')
        if 'y' in kwargs:
            self.y = kwargs['y']
        else:
            self.y = Symbol('y')

        self.genproblem()
        self.lhs = self.b*self.d*self.x + self.a*self.d*self.y
        self.rhs = self.a*self.b*self.d
        self.given = Eq(self.lhs, self.rhs)

        self.format_given = f"\\[ {latex(self.lhs)} = {latex(self.rhs)} \\]"



        self.format_answer = '\\quad\n'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
Graph the line with the given equation.  Make sure your graph is accurate throughout
the window and has at least two points clearly marked.
{self.format_given}

\\begin{{flushright}}
\\includegraphics[scale=0.6]{{../common_imgs/blank}}
\\end{{flushright}}
\\vspace{{-12\\baselineskip}}

"""

    name = 'Graph Line from Standard Form'
    module_name = 'graph_standard_form_line'

    prompt_single = """Graph the given equation by plotting at least two points
that satisfy the equation."""
    prompt_multiple = """Graph each of the following equations by plotting at least two points
that satisfy the equation."""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        b = self.b
        m = self.m
        self.as_lambda = lambda x: m*x + b
        f = self.as_lambda
        self.answer = f(x)

    has_img_in_key = True

    def save_img(self, filename):
        graph = GraphFromLambda(self.as_lambda)
        graph.save_fig(filename)

    def get_svg_data(self, window=[-10,10]):
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
        if type(user_answer) == type(5):
            return False
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



Question_Class = GraphStandardFormLine
