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
                            GraphFromLambda,
                            fmt_slope_style,
                            commute_sum,
                            tolerates,
                            )
from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general



prob_type = 'graph'

class GraphAbsoluteValue(Question):
    """
    The given is of the form

    \\[
        y = Rational(p,q)|x - x0| + y0
    \\]

    The student is expected to graph by plotting points.  3 is sufficient.
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
            self.p = random_non_zero_integer(-5,5)
        if 'q' in kwargs:
            self.q = kwargs['q']
        else:
            self.q = random.randint(1,5)
        self.m = Rational(self.p, self.q)
        if 'x0' in kwargs:
            self.x0 = kwargs['x0']
        else:
            self.x0 = random_non_zero_integer(-5,5)
        if 'y0' in kwargs:
            self.y0 = kwargs['y0']
        else:
            self.y0 = random.randint(-5,5)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        self.genproblem()

        # self.given = self.problem['given']
        # self.answer = self.problem['answer']
        # term = factor(self.m*(self.x - self.x0))
        # if self.y0 > 0:
        #     fmt_y0 = latex(self.y0)
        #     sign = '+'
        # elif self.y0 == 0:
        #     fmt_y0 = ''
        #     sign = ''
        # else:
        #     fmt_y0 = latex(abs(self.y0))
        #     sign = '-'
        # # print(term)
        # try:
        #     self.format_given = f"""
        #     \\[
        #      y = {latex(term.args[0])} ({latex(term.args[1])}) {sign} {fmt_y0}
        #     \\]
        #     """
        # except IndexError:
        #     self.format_given = f"""
        #     \\[
        #      y = ({latex(term)}) {sign} {fmt_y0}
        #     \\]
        #     """
        term = self.as_lambda(self.x)
        self.format_given = f"""
        \[
            y = {commute_sum(term)}
        \]
        """



        self.format_answer = '\\quad\n'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
Sketch a graph of the given equation.  Make sure your graph is accurate throughout
the window and has at least three points clearly marked.
{self.format_given}

\\begin{{flushright}}
\\includegraphics[scale=0.6]{{../common_imgs/blank}}
\\end{{flushright}}
\\vspace{{-12\\baselineskip}}

"""

    name = 'Graph of an Absolute Value Function'
    module_name = 'graph_absolute_value'

    prompt_single = """Graph the given equation by plotting at least three points
that satisfy the equation."""
    prompt_multiple = """Graph each of the following equations by plotting at least three points
that satisfy the equation."""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        b = self.y0
        h = self.x0
        # p = self.p
        # q = self.q
        m = self.m
        self.as_lambda = lambda x: m*abs(x - h) + b
        f = self.as_lambda
        self.given = factor(m*abs(x-h)) + b
        #print('3rd step: So far its ', expr)
        self.answer = f(x)

    has_img_in_key = True

    def save_img(self, filename):
        graph = GraphFromLambda(self.as_lambda)
        graph.save_fig(filename)

    def get_svg_data(self, window=[-10,10], res=1000):
        x_min = window[0]
        x_max = window[1]
        x_points = np.array([-10, self.x0, 10])
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
        # user_answer = user_answer(self.x)
        # return self.answer.equals(user_answer)
        return tolerates(lambdify(self.x, self.answer), user_answer)

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



Question_Class = GraphAbsoluteValue
