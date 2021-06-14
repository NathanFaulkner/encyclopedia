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

class GraphSlopeInterceptFromEnglish(Question):
    """
    The given is slope and y-intercept of

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
        # self.p = 0
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

        self.format_given = """
        <blockquote>
            The line that has \\(y\\)-intercept of {b}
            and has slope of \\( m = {m} \\)
        </blockquote>
        """.format(b=latex(self.b),
                    m=latex(self.m))


        self.format_answer = '\\quad\n'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)


        self.prompt_single = """Graph the line described by plotting at least
        two points."""
        self.prompt_multiple = """This needs to be rethought."""

        self.format_given_for_tex = f"""
Graph the line described.  Make sure your graph is accurate throughout
the window and has at least two points clearly marked.

\\begin{{center}}
The line that has \\(y\\)-intercept of \\({self.b}\\)
and has slope of \\( m = {latex(self.m)} \\)
\\end{{center}}

\\begin{{flushright}}
    \\includegraphics[scale=0.6]{{../common_imgs/blank}}
\\end{{flushright}}
\\vspace{{-9\\baselineskip}}

"""
        self.format_fragment_for_tex = f"""
        The line that has \\(y\\)-intercept of \\({self.b}\\)
        and has slope of \\( m = {latex(self.m)} \\)
        """


    name = 'Graph from Slope and Intercept'
    module_name = 'graph_slope_intercept_from_english'




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

    has_img_in_key = True

    def save_img(self, filename):
        graph = GraphFromLambda(self.as_lambda)
        graph.save_fig(filename)

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



Question_Class = GraphSlopeInterceptFromEnglish
