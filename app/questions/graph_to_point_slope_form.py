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
                        poly_points_from_nparrays,
                        GraphFromLambda,
                        fmt_slope_style,
                        commute_sum)
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

class GraphToPointSlope(Question):
    """
    The given is a graph of

    \\[
    y = Rational(p,q)x + b
    \\]

    The equation is the answer.
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
        while abs(self.p/self.q) == 1:
            self.p = random.randint(-5,5)
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

        self.genproblem()

        points = [[self.x0, self.y0], [self.x0 + self.q, self.as_lambda(self.x0 + self.q)]]
        poly_points = self.get_svg_data([-10,10])

        self.format_given = f"""
        <div style="text-align:center">
            {render_template('_static_graph.html',
                            poly_points=poly_points,
                            parameters=get_parameters(),
                            points=points)}
        </div>
        """
        m = self.m
        x0 = self.x0
        y0 = self.y0
        x = self.x
        term = factor(self.m*(self.x - self.x0))
        if self.y0 > 0:
            fmt_y0 = latex(self.y0)
            sign = '+'
        elif self.y0 == 0:
            fmt_y0 = ''
            sign = ''
        else:
            fmt_y0 = latex(abs(self.y0))
            sign = '-'
        # print(term)
        try:
            self.format_answer = f"""
            \\(
             y = {latex(term.args[0])} ({latex(term.args[1])}) {sign} {fmt_y0}
            \\)
            """
        except IndexError:
            self.format_answer = f"""
            \\(
             y = ({latex(term)}) {sign} {fmt_y0}
            \\)
            """
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)


        self.prompt_single =  """Develop an equation for the graphed line."""
        self.prompt_multiple = """Develop an equation for each of the graphed lines."""

        self.format_given_for_tex = f"""{self.prompt_single}
            """

    name = 'Point-Slope Form from Graph'
    module_name = 'graph_to_point_slope_form'



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

    has_img = True

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



Question_Class = GraphToPointSlope
