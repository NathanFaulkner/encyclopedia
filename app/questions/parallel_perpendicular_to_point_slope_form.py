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
                        fmt_slope_style)
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

class ParallelPerpendicularToPointSlope(Question):
    """
    The given is a description of the graph of

    \\[
        y = Rational(p,q)x + b
    \\]

    The description is that the line is parallel or perpendicular to
    the line with equation
    \[
        y = m1 x + b1
    \]
    The equation is the answer.

    Parallel or perpendicular can be controlled by kwarg
    parallel_or_perp with values 'parallel' and 'perpendicular'
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
            self.q = random_non_zero_integer(-5,5)
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
        if 'b1' in kwargs:
            self.b1 = kwargs['b1']
        else:
            self.b1 = random.randint(-9,9)
        if 'parallel_or_perp' in kwargs:
            self.parallel_or_perp = kwargs['parallel_or_perp']
        else:
            self.parallel_or_perp = random.choice(['parallel', 'perpendicular'])
        if self.parallel_or_perp == 'parallel':
            self.m1 = self.m
        else:
            self.m1 = -1/self.m

        self.genproblem()

        self.format_given = f"""
        <blockquote>
            The line that passes through the point \\( ({self.x0}, {self.y0}) \\)
            and is {self.parallel_or_perp} to the line with equation
            \\[
                y = {fmt_slope_style(self.m1*self.x + self.b1)}
            \\]
        </blockquote>
        """


        self.format_answer = f'\( y = {latex(self.answer)}\)'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)


        self.prompt_single =  """Give an equation for the line described as follows."""
        self.prompt_multiple = """Give an equation for each of the lines described below."""

        self.format_given_for_tex = f"""{self.prompt_single}

            \\begin{{center}}
                The line that passes through the point \\( ({self.x0}, {self.y0}) \\)
                and has slope of \\( m = {latex(self.m)} \\)
            \\end{{center}}
            """

    name = 'Point Slope Form from Description (Parallel or Perpendicular)'
    module_name = 'parallel_perpendicular_to_point_slope_form'



    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        x = self.x
        b = self.y0
        h = self.x0
        # p = self.p
        # q = self.q
        m = self.m
        self.as_lambda = lambda x: m*(x - h) + b
        f = self.as_lambda
        self.given = factor(m*(x-h)) + b
        #print('3rd step: So far its ', expr)
        self.answer = f(x)

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
        user_answer = user_answer.lower()
        if 'y' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        y = Symbol('y')
        user_answer = solve(user_answer, y)[0]
        return self.answer.equals(user_answer)


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
            y = Symbol('y')
            user_answer = solve(user_answer, y)[0]
        except:
            raise SyntaxError



Question_Class = ParallelPerpendicularToPointSlope
