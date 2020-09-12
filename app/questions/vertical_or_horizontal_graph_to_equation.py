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

class VerticalOrHorizontalGraphToEquation(Question):
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

        poly_points = self.get_svg_data([-10,10])
        points = []

        self.format_given = f"""
        <div style="text-align:center">
            {render_template('_static_graph.html',
                            poly_points=poly_points,
                            parameters=get_parameters(),
                            points=points)}
        </div>
        """

        self.format_answer = f'\({self.symb} = {self.value}\)'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
Develop an equation for the given graph.
{self.format_given}

\\begin{{flushright}}
\\includegraphics[scale=0.6]{{../common_imgs/blank}}
\\end{{flushright}}
\\vspace{{-12\\baselineskip}}

"""

    name = 'Equation for Vertical or Horizontal Line'
    module_name = 'vertical_or_horizontal_graph_to_equation'

    prompt_single = """Develop an equation for the given graph"""
    prompt_multiple = """TBA"""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'



    has_img = True

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
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
        except:
            raise SyntaxError



Question_Class = VerticalOrHorizontalGraphToEquation
