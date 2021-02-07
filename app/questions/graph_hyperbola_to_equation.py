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

class GraphHyperbolaToEquation(Question):
    """
    The answer is of the form

    \\[
        y = Rational(p,q)(x - x0)^2 + y0
    \\]

    The given is the graph.
    """
    def __init__(self, **kwargs):
        if 'basic' in kwargs:
            self.basic = kwargs['basic']
        else:
            self.basic = False
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['a']
            a = self.a
        else:
            a = 1
        if 'x0' in kwargs:
            self.x0 = kwargs['x0']
            h = self.x0
        else:
            h = 0
        if 'y0' in kwargs:
            self.y0 = kwargs['y0']
            k = self.y0
        else:
            k = 0
        if not self.basic:
            while a == 1 and h == 0 and k == 0:
            	a = random.choice([-2,-1,-1,1,1,2,2])
            	h = random.randint(-5,5)
            	k = random.randint(-5,5)
        self.x0 = h
        self.y0 = k
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('x')
        x = self.x

        expr = a/(x-h) + k

        self.as_lambda = lambda x: a/(x - h) + k
        f = self.as_lambda

        self.prompt_single =  """Develop an equation for the given graph.
        """
        self.prompt_multiple = """For each of the following,
        develop an equation for the given graph."""

        f = self.as_lambda
        self.answer = f(x)
        self.format_answer = f"""
        \\(
         y = {sy.latex(a/(x-h) + k)}
        \\)
        """
        # a = self.a
        # h = self.x0
        # if abs(m) == Rational(1,2):
        #     x_points = [h, h-2, h+2, h-4, h+4]
        # else:
        #     x_points = [h, h-1, h-2, h+1, h+2]
        # points = [[x, f(x)] for x in x_points]
        # self.points = points

        # self.piecewise = True
        poly_points = self.get_svg_data([-10,10])['poly_points']

        self.format_given = f"""
        <div style="text-align:center">
            {render_template('_static_graph.html',
                            piecewise=True,
                            list_of_poly_data=poly_points,
                            parameters=get_parameters())
                            }
        </div>
        """

        self.format_given_for_tex = f"""{self.prompt_single}
        """


    name = 'Equation from Graph of Hyperbola'
    module_name = 'graph_hyperbola_to_equation'

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    has_img = True

    def save_img(self, filename):
        graph = GraphFromLambda(self.as_lambda)
        graph.save_fig(filename)

    def get_svg_data(self, window=[-10,10], res=1001):
        x_min = window[0]
        x_max = window[1]
        x_left = np.linspace(x_min, self.x0-(x_max-x_min)/res, res)
        y_left = self.as_lambda(x_left)
        x_left = cart_x_to_svg(x_left)
        y_left = cart_y_to_svg(y_left)
        x_right = np.linspace(self.x0+(x_max-x_min)/res, x_max, res)
        y_right = self.as_lambda(x_right)
        x_right = cart_x_to_svg(x_right)
        y_right = cart_y_to_svg(y_right)
        poly_points = []
        current = ''
        l = len(x_left)
        i = 0
        while i < l:
            current += f"{x_left[i]},{y_left[i]} "
            i += 1
        poly_points.append(current)
        current = ''
        l = len(x_right)
        i = 0
        while i < l:
            current += f"{x_right[i]},{y_right[i]} "
            i += 1
        poly_points.append(current)
        # print('poly', poly_points[1])
        return {'piecewise': True, 'poly_points': poly_points}


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


    def format_useranswer(self, user_answer, display=False):
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




Question_Class = GraphHyperbolaToEquation
