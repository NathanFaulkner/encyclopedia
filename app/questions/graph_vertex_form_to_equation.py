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

class GraphVertexFormToEquation(Question):
    """
    The answer is of the form

    \\[
        y = Rational(p,q)(x - x0)^2 + y0
    \\]

    The given is the graph.
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
            self.p = random_non_zero_integer(-2,2)
        if 'q' in kwargs:
            self.q = kwargs['q']
        else:
            self.q = random.randint(1,2)
        self.m = Rational(self.p, self.q)
        if 'x0' in kwargs:
            self.x0 = kwargs['x0']
        else:
            self.x0 = random_non_zero_integer(-5,5)
        if 'y0' in kwargs:
            self.y0 = kwargs['y0']
        else:
            if self.m == 2 or self.m == Rational(1,2):
                self.y0 = random.randint(-5, 2)
            elif self.m == -2 or self.m == Rational(-1,2):
                self.y0 = random.randint(-2, 5)
            else:
                self.y0 = random.randint(-5,5)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        self.genproblem()

        term = factor(self.m*(self.x - self.x0)**2)
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
        if self.m == 1:
            fmt_m = ''
        elif self.m == -1:
            fmt_m = '-'
        else:
            fmt_m = latex(self.m)
        try:
            self.format_answer = f"""
            \\(
             y = {fmt_m} {latex((self.x - self.x0)**2)} {sign} {fmt_y0}
            \\)
            """
        except IndexError:
            self.format_answer = f"""
            \\(
             y = {latex(term)} {sign} {fmt_y0}
            \\)
            """

        self.prompt_single =  """Develop an equation for the given graph.
        """
        self.prompt_multiple = """For each of the following,
        develop an equation for the given graph."""

        f = self.as_lambda
        m = self.m
        h = self.x0
        if abs(m) == Rational(1,2):
            x_points = [h, h-2, h+2, h-4, h+4]
        else:
            x_points = [h, h-1, h-2, h+1, h+2]
        points = [[x, f(x)] for x in x_points]
        self.points = points

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




    name = 'Vertex Form from Graph'
    module_name = 'graph_vertex_form_to_equation'



    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        k = self.y0
        h = self.x0
        # p = self.p
        # q = self.q
        m = self.m
        self.as_lambda = lambda x: m*(x - h)**2 + k
        f = self.as_lambda
        self.given = factor(m*(x-h)**2) + k
        #print('3rd step: So far its ', expr)
        self.answer = f(x)

    has_img = True

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
        user_answer = Eq(lhs, rhs)
        y = Symbol('y')
        user_answer = solve(user_answer, y)[0]
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
        user_answer = Eq(lhs, rhs)
        y = Symbol('y')
        user_answer = solve(user_answer, y)[0]
        return f'\(y = {latex(user_answer)}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.replace('X', 'x')
            user_answer = user_answer.replace('Y', 'y')
            user_answer = user_answer.replace('abs', 'Abs')
            user_answer = fmt_abs_value(user_answer)
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
            y = Symbol('y')
            user_answer = solve(user_answer, y)[0]
        except:
            raise SyntaxError




Question_Class = GraphVertexFormToEquation
