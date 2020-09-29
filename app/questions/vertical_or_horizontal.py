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
                            GraphHoriz, GraphVert)
from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general



prob_type = 'graph'

class VerticalOrHorizontal(Question):
    """
    The given is of the form

    \\[
        y  = value
    \\]
    or
    \\[
        x = value
    \\]

    kwarg orientation is either vert or horiz

    The student is expected to graph by plotting points.  Two is sufficient.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'orientation' in kwargs:
            self.orientation = kwargs['orientation']
        else:
            self.orientation = random.choice(['vert', 'horiz'])
        if 'value' in kwargs:
            self.value = kwargs['value']
        else:
            self.value = random.randint(-8,8)
        if self.orientation == 'vert':
            self.symb = Symbol('x')
        else:
            self.symb = Symbol('y')

        self.lhs = self.symb
        self.rhs = self.value
        self.given = Eq(self.lhs, self.rhs)

        self.format_given = f"\\[ {latex(self.lhs)} = {latex(self.rhs)} \\]"

        self.answer = self.value

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

    name = 'Vertical or Horizontal Lines'
    module_name = 'vertical_or_horizontal'

    prompt_single = """Graph the given equation by plotting at least two points
that satisfy the equation."""
    prompt_multiple = """Graph each of the following equations by plotting at least two points
that satisfy the equation."""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'



    has_img_in_key = True

    def save_img(self, filename):
        if self.orientation == 'vert':
            graph = GraphVert(self.value)
        else:
            graph = GraphHoriz(self.value)
        graph.save_fig(filename)

    def get_svg_data(self, xwindow=[-10,10], ywindow=[-10,10]):
        x_min, x_max = xwindow
        y_min, y_max = ywindow
        if self.orientation == 'vert':
            x_points = np.array([self.value, self.value])
            y_points = np.array([y_min, y_max])
        else:
            x_points = np.array([x_min, x_max])
            y_points = np.array([self.value, self.value])
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
        if self.orientation == 'vert':
            return user_answer == self.value
        else:
            # print(type(user_answer))
            if type(user_answer) == type(5):
                return False
        x = Symbol('x')
        user_answer = user_answer(x)
        answer = self.value
        print(answer, user_answer)
        return answer == user_answer

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



Question_Class = VerticalOrHorizontal
