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

class PolynomialCurveSketching(Question):
    """
    The given is of the form

    \\[
        y = Rational(p,q)(x - x0)^2 + y0
    \\]

    The student is expected to graph by plotting points.  4 is sufficient.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        x = Symbol('x', real=True)
        self.x = x
        degree = random.choice([3,4])
        #degree = 4
        zeroes = []
        force_duplicate = random.choice([True, False])
        # force_duplicate = True

        def have_duplicate(a):
            return len(a) != len(set(a))

        if force_duplicate:
            while not(have_duplicate(zeroes)):
                zeroes = []
                for i in range(degree):
                    zeroes.append(random.randint(-5,5))
        else:
            for i in range(degree):
                    zeroes.append(random.randint(-5,5))
        #print(zeroes)

        y_0 = random.randint(-9,9)
        prod = 1
        x_0 = 0
        while x_0 in zeroes:
            x_0 = random_non_zero_integer(-5,5)
        for z in zeroes:
            prod *= (x_0-z)
        LC = Rational(y_0, prod)

        def f(x):
            out = LC
            for i in range(degree):
                out *= (x-zeroes[i])
            return out

        expr = simplify(1/LC*f(x))

        self.as_lambda = lambdify(x, f(x))
        f = self.as_lambda
        self.given = factor(f(x))
        self.format_given = f'\\(f(x) = {latex(LC)}{latex(expr)}\\)'
        #print('3rd step: So far its ', expr)
        self.answer = f(x)

        self.format_answer = '\\quad\n'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
Sketch a graph of the given equation.  Make sure your graph is accurate throughout
the window and has at least 5 points clearly marked.
{self.format_given}

\\begin{{flushright}}
\\includegraphics[scale=0.6]{{../common_imgs/blank}}
\\end{{flushright}}
\\vspace{{-12\\baselineskip}}

"""

    name = 'Polynomial Curve Sketching'
    module_name = 'polynomial_curve_sketching'

    prompt_single = """Graph all the zeroes of the function, plus
    one more point."""
    prompt_multiple = "TBA"

    further_instruction = """Right click on a point to add it in as a
    "repeated" point.  (What the graphing tool does is take
    the points you click on and serves up different graphs
    that it thinks you might have in mind.  I have set it up
    so that, when you graph a point twice, it will interpret
    this is a "repeated" zero of a factored polynomial.) 
    """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    has_img_in_key = True

    def save_img(self, filename):
        graph = GraphFromLambda(self.as_lambda)
        graph.save_fig(filename)

    def get_svg_data(self, window=[-10,10], res=100):
        x_min = window[0]
        x_max = window[1]
        x_points = np.linspace(x_min, x_max, res)
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
        return tolerates(user_answer, self.as_lambda)

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



Question_Class = PolynomialCurveSketching
