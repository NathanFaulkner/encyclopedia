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
                            random_non_zero_integer,
                            GraphVert, GraphHoriz)
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

class VerticalOrHorizontalInfoToEquation(Question):
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
        if 'x0' in kwargs:
            self.x0 = kwargs['x0']
        else:
            self.x0 = random_non_zero_integer(-8,8)
        if 'y0' in kwargs:
            self.y0 = kwargs['y0']
        else:
            self.y0 = random.randint(-8, 8)
        if 'orientation' in kwargs:
            self.orientation = kwargs['orientation']
        else:
            self.orientation = random.choice(['vert', 'horiz'])
        if 'parallel_or_perp' in kwargs:
            self.parallel_or_perp = kwargs['parallel_or_perp']
        else:
            self.parallel_or_perp = random.choice(['parallel', 'perpendicular'])
        if self.orientation == 'vert':
            self.symb = Symbol('x')
            self.value = self.x0
            if self.parallel_or_perp == 'parallel':
                ax_name = '\(y\)'
                alt_symb = 'x'
            else:
                ax_name = '\(x\)'
                alt_symb = 'y'
        else: #horiz
            self.symb = Symbol('y')
            self.value = self.y0
            if self.parallel_or_perp == 'parallel':
                ax_name = '\(x\)'
                alt_symb = 'y'
            else:
                ax_name = '\(y\)'
                alt_symb = 'x'

        alt_value = random.randint(-9,9)

        alt_line_choices = [
            f'the {ax_name}-axis',
            f'the line with equation \({alt_symb} = {alt_value}\)'
        ]
        self.given_line = random.choice(alt_line_choices)
        self.lhs = self.symb
        self.rhs = self.value
        # self.given = Eq(self.lhs, self.rhs)

        self.answer = self.value

        self.format_given = f"""
<div style="text-align:center">
    The line is {self.parallel_or_perp} to {self.given_line}
    and passes through \(({self.x0}, {self.y0})\).
</div>
        """

        self.format_answer = f'\({self.symb} = {self.value}\)'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
Develop an equation for the line described here.

\\begin{{center}}
The line is {self.parallel_or_perp} to {self.given_line}
and passes through \(({self.x0}, {self.y0})\).
\\end{{center}}

"""
        self.format_fragment_for_tex = f"""
        The line is {self.parallel_or_perp} to {self.given_line}
        and passes through \(({self.x0}, {self.y0})\).
        """

    name = 'Equation for Vertical or Horizontal Line from Information'
    module_name = 'vertical_or_horizontal_info_to_equation'

    prompt_single = """Develop an equation for the line described here."""
    prompt_multiple = """TBA"""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'



    # has_img = True

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
        user_answer = user_answer.lower()
        if self.orientation == 'vert':
            if 'x' not in user_answer:
                return False
        else:
            if 'y' not in user_answer:
                return False
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        user_answer = solve(user_answer, self.symb)[0]
        return self.value == user_answer

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        return f'\({latex(lhs)} = {latex(rhs)}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            if 'x' not in user_answer and 'y' not in user_answer:
                raise SyntaxError
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
        except:
            raise SyntaxError



Question_Class = VerticalOrHorizontalInfoToEquation
