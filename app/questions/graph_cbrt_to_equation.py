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

class GraphCbrtToEquation(Question):
    """
    The answer is of the form

    \\[

    \\]

    The given is the graph.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
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
            self.x = sy.Symbol('x')
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
        # expr = parse_expr(f'{self.m}cbrt(x-{self.x0})+{self.y0}', transformations=transformations)
        expr = m*(x - h)**sy.Rational(1,3) + k
        print(expr)
        self.as_lambda = sy.lambdify(x, expr) #sy.lambdify(x, m*(x-h)**sy.Rational(1,3)+k)#= lambda x: m*(x - h)**(1/3) + k
        f = self.as_lambda
        self.given = f(x)
        #print('3rd step: So far its ', expr)
        self.answer = expr

        term = self.given
        self.format_given = f'\\(y = {sy.latex(self.answer)}\\)'
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

        # f = self.as_lambda
        # self.answer = f(x)
        self.format_answer = self.format_given
        # a = self.a
        # h = self.x0
        # x_points_left = [h-1, h-8]
        x_points_right = [h, h+1, h+8]
        points_right = [[x, f(x)] for x in x_points_right]
        points_left = [[-x**3+h, -m*x+k] for x in [1, 2]]
        points = points_left + points_right
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


    name = 'Equation from Graph of Cube Root Function'
    module_name = 'graph_cbrt_to_equation'

    further_instruction = """You can enter a cube root function using the
    symbol 'cbrt'.  For example, if your answer is \\(y = -\\sqrt[3]{x-3}+4 \\),
    you would enter
    <div style="margin-left:auto; margin-right:auto; text-align:center">
        y = -cbrt(x-3)+4
    </div>
    """

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    has_img = True

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




Question_Class = GraphCbrtToEquation
