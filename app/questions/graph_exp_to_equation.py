#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy
import numpy as np
import json

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            GraphFromLambda,
                            fmt_slope_style,
                            commute_sum,
                            fmt_abs_value)
from app.interpolator import cart_x_to_svg, cart_y_to_svg, get_parameters

from flask import render_template

# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general



prob_type = 'math blank'

class GraphExpToEquation(Question):
    """
    The given is of the form

    \\[
        y = A b^(x-x0) + y0
    \\]

    The student is expected to graph by plotting points.  4 is sufficient.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'A' in kwargs:
            self.A = kwargs['A']
        else:
            self.A = random.choice([1, 1, -1, -1, 2, -2])
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.choice([2, 3, sy.Rational(1, 2), sy.Rational(1, 3)])
        if 'x0' in kwargs:
            self.x0 = kwargs['x0']
        else:
            self.x0 = random.randint(-5,5)
        if 'k' in kwargs:
            self.k = kwargs['k']
        else:
            # y0_min = max(-5, -9 - self.m*4)
            # y0_max = min(5, 9 - self.m*4)
            y0_min = -5
            y0_max = 5
            self.k = random.randint(y0_min, y0_max)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('x')
        x = self.x
        k = self.k
        x0 = self.x0
        A = self.A
        b = self.b
        self.as_lambda = lambda x: A*float(b)**(x-x0)+k
        f = self.as_lambda
        self.given = A*b**(x-x0)+k
        #print('3rd step: So far its ', expr)
        self.answer = f(x)

        # term = self.given
        # if self.y0 > 0:
        #     fmt_y0 = sy.latex(self.y0)
        #     sign = '+'
        # elif self.y0 == 0:
        #     fmt_y0 = ''
        #     sign = ''
        # else:
        #     fmt_y0 = sy.latex(abs(self.y0))
        #     sign = '-'
        # # print(term)
        # if self.m == 1:
        #     fmt_m = ''
        # elif self.m == -1:
        #     fmt_m = '-'
        # else:
        #     fmt_m = sy.latex(self.m)
        # try:
        #     self.format_given = f"""
        #     \\[
        #      y = {fmt_m} {sy.latex((sy.factor(sign_x*(self.x - self.x0))**sy.Rational(1,2)))} {sign} {fmt_y0}
        #     \\]
        #     """
        # except IndexError:
        #     self.format_given = f"""
        #     \\[
        #      y = {sy.latex(term)} {sign} {fmt_y0}
        #     \\]
        #     """

        self.format_given = f'\\[ y = {sy.latex(self.given)}\\]'
        # if self.y0 > 0:
        #     fmt_y0 = sy.latex(self.y0)
        #     sign = '+'
        # elif self.y0 == 0:
        #     fmt_y0 = ''
        #     sign = ''
        # else:
        #     fmt_y0 = sy.latex(abs(self.y0))
        #     sign = '-'
        # # print(term)
        # if self.m == 1:
        #     fmt_m = ''
        # elif self.m == -1:
        #     fmt_m = '-'
        # else:
        #     fmt_m = sy.latex(self.m)
        # try:
        #     self.format_given = f"""
        #     \\[
        #      y = {fmt_m} {sy.latex((sy.factor(sign_x*(self.x - self.x0))**sy.Rational(1,2)))} {sign} {fmt_y0}
        #     \\]
        #     """
        # except IndexError:
        #     self.format_given = f"""
        #     \\[
        #      y = {sy.latex(term)} {sign} {fmt_y0}
        #     \\]
        #     """

        # self.format_answer = '\\quad\n'

        self.prompt_single =  """Develop an equation for the given graph.
        """
        self.prompt_multiple = """For each of the following,
        develop an equation for the given graph."""

        f = self.as_lambda
        self.answer = self.given
        self.format_answer = f'\\( y = {sy.latex(self.given)}\\)'
        # a = self.a
        # h = self.x0
        x_points = [x0-3, x0-2, x0-1, x0, x0+1, x0+2, x0+3]
        points = [[x, f(x)] for x in x_points]
        self.points = points


        # self.piecewise = True
        poly_points = self.get_svg_data([-10,10])

        self.format_given = f"""
        <div style="text-align:center">
            {render_template('_static_graph.html',
                            poly_points=poly_points,
                            parameters=get_parameters(),
                            points=points)}
        </div>
        """

        self.format_given_for_tex = f"""{self.prompt_single}
        """
        self.format_fragment_for_tex = ' '


    name = 'Equation from Graph of Exponential Function'
    module_name = 'graph_exp_to_equation'

    # further_instruction = """You can enter a square root function using the
    # symbol 'sqrt'.  For example, if your answer is \\(y = -\\sqrt{x-3}+4 \\),
    # you would enter
    # <div style="margin-left:auto; margin-right:auto; text-align:center">
    #     y = -sqrt(x-3)+4
    # </div>
    # """

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    has_img = True

    def save_img(self, filename):
        graph = GraphFromLambda(self.as_lambda)
        graph.save_fig(filename)

    def get_svg_data(self, window=[-10,10], res=100):
        x_min = window[0]
        x_max = window[1]
        x_points = np.linspace(x_min, x_max, res)
        y_points = self.as_lambda(x_points)
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
        user_answer = user_answer.replace('X', 'x')
        user_answer = user_answer.replace('Y', 'y')
        user_answer = user_answer.replace('abs', 'Abs')
        user_answer = fmt_abs_value(user_answer)
        if 'y' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = sy.Eq(lhs, rhs)
        y = sy.Symbol('y')
        user_answer = sy.solve(user_answer, y)[0]
        return self.answer.equals(user_answer)

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.replace('X', 'x')
        user_answer = user_answer.replace('Y', 'y')
        user_answer = user_answer.replace('abs', 'Abs')
        user_answer = fmt_abs_value(user_answer)
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = sy.Eq(lhs, rhs)
        y = sy.Symbol('y')
        user_answer = sy.solve(user_answer, y)[0]
        return f'\(y = {sy.latex(user_answer)}\)'

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.replace('X', 'x')
            user_answer = user_answer.replace('Y', 'y')
            user_answer = user_answer.replace('abs', 'Abs')
            user_answer = fmt_abs_value(user_answer)
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = sy.Eq(lhs, rhs)
            y = sy.Symbol('y')
            user_answer = sy.solve(user_answer, y)[0]
        except:
            raise SyntaxError




Question_Class = GraphExpToEquation
