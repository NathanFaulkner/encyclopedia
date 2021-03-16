#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
# from sympy.parsing.sympy_parser import parse_expr
# from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
# transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy
import numpy as np
import json

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            GraphFromLambda,
                            fmt_slope_style,
                            commute_sum,
                            tolerates)
from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general



prob_type = 'graph'

class GraphCbrt(Question):
    """
    The given is of the form

    \\[
        y = a\sqrt[3]{x - x0} + y0
    \\]

    The student is expected to graph by plotting points.  4 is sufficient.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        # if 'p' in kwargs:
        #     self.p = kwargs['p']
        # else:
        #     self.p = random_non_zero_integer(-2,2)
        # if 'q' in kwargs:
        #     self.q = kwargs['q']
        # else:
        #     self.q = random.randint(1,2)
        if 'm' in kwargs:
            self.m = kwargs['m']
        else:
            self.m = random.choice([1, 1, -1, -1, 2, -2, 3, -3])
        if 'x0' in kwargs:
            self.x0 = kwargs['x0']
        else:
            self.x0 = random.randint(-5,5)
        if 'y0' in kwargs:
            self.y0 = kwargs['y0']
        else:
            # y0_min = max(-5, -9 - self.m*4)
            # y0_max = min(5, 9 - self.m*4)
            y0_min = -5
            y0_max = 5
            self.y0 = random.randint(y0_min, y0_max)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('x', Real=True)
        # if 'sign_x' in kwargs:
        #     self.sign_x = kwargs['sign_x']
        # else:
        #     self.sign_x = random.choice([-1, 1])
        # sign_x = self.sign_x
        x = self.x
        k = self.y0
        h = self.x0
        # p = self.p
        # q = self.q
        m = self.m
        self.as_lambda = sy.lambdify(x, m*(x-h)**sy.Rational(1,3)+k)#= lambda x: m*(x - h)**(1/3) + k
        f = self.as_lambda
        self.given = f(x)
        #print('3rd step: So far its ', expr)
        self.answer = f(x)

        term = self.given
        if self.y0 > 0:
            fmt_y0 = sy.latex(self.y0)
            sign = '+'
        elif self.y0 == 0:
            fmt_y0 = ''
            sign = ''
        else:
            fmt_y0 = sy.latex(abs(self.y0))
            sign = '-'
        # print(term)
        if self.m == 1:
            fmt_m = ''
        elif self.m == -1:
            fmt_m = '-'
        else:
            fmt_m = sy.latex(self.m)
        try:
            self.format_given = f"""
            \\[
             y = {fmt_m} {sy.latex(((self.x - self.x0)**sy.Rational(1, 3)))} {sign} {fmt_y0}
            \\]
            """
        except IndexError:
            self.format_given = f"""
            \\[
             y = {sy.latex(term)} {sign} {fmt_y0}
            \\]
            """

        self.format_answer = '\\quad\n'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
Sketch a graph of the given equation.  Make sure your graph is accurate throughout
the window and has at least 5 points clearly marked, including the vertex.
{self.format_given}

\\begin{{flushright}}
\\includegraphics[scale=0.6]{{../common_imgs/blank}}
\\end{{flushright}}
\\vspace{{-12\\baselineskip}}

"""

    name = 'Graph of a Cube Root Function'
    module_name = 'graph_cbrt'

    prompt_single = """Graph the given equation by plotting the "anchor" point and at least 3 other points
that satisfy the equation."""
    prompt_multiple = """TBA"""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    has_img_in_key = True

    def save_img(self, filename):
        graph = GraphFromLambda(self.as_lambda)
        graph.save_fig(filename)

    def get_svg_data(self, window=[-10,10], res=100):
        x_min = -10 - self.x0
        x_max = 10 - self.x0
        x_points_left = np.linspace(x_min, 0, int(res/2))
        x_points_right = np.linspace(0, x_max, int(res/2))
        x_points = np.concatenate([x_points_left, x_points_right])
        x_points = x_points + self.x0
        # print(new_lambda(self.x))
        y_points_left = -self.m*np.cbrt(-(x_points_left))+self.y0
        y_points_right = self.m*np.cbrt(x_points_right)+self.y0
        y_points = np.concatenate([y_points_left, y_points_right])
        # print(self.as_lambda(self.x))
        # print(y_points)
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
        # return tolerates(lambdify(self.x, self.answer), lambdify(self.x, user_answer))
        return tolerates(sy.lambdify(self.x, self.answer), user_answer, window=[self.x0, 10])

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



Question_Class = GraphCbrt
