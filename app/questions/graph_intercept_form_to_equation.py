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

class GraphInterceptFormToEquation(Question):
    """
    The given is of the form

    \\[
        y = a(x-x1)(x-x2)
    \\]

    The student is expected to graph by plotting points.  4 is sufficient.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'x1' in kwargs:
            self.x1 = kwargs['x1']
        else:
            self.x1 = random_non_zero_integer(-8,5)
        if 'x2' in kwargs:
            self.x2 = kwargs['x2']
        else:
            max_diff = min(10-self.x1, 8)
            diff = random.randint(1, max_diff)
            self.x2 = self.x1 + diff
        d = self.x2 - self.x1
        self.avg = Rational(self.x1 + self.x2, 2)
        self.x1, self.x2 = random.choice([[self.x1, self.x2], [self.x2, self.x1]])
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            a = 0
            while a == 0 or a > 40/d**2:
                a = random.choice([Rational(1, 2), 2, 1, 1])
            self.a = random.choice([-1, 1]) * a
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        x = self.x
        x1 = self.x1
        x2 = self.x2
        a = self.a
        if a == 1:
            fmt_a = ''
        elif a == -1:
            fmt_a = '-'
        else:
            fmt_a = latex(a)

        def fmt_factor(fact):
            if fact == 'x':
                return 'x'
            else:
                return f'\\left({latex(fact)}\\right)'
        # p = self.p
        # q = self.q
        self.as_lambda = lambda x: a*(x - x1)*(x - x2)
        f = self.as_lambda
        self.given = factor(a*(x - x1)*(x - x2))
        #print('3rd step: So far its ', expr)
        self.answer = f(x)

        self.format_answer = f"""
    \\(
        y = {fmt_a}{fmt_factor(x - x1)}{fmt_factor(x - x2)}
    \\)
        """


        self.prompt_single =  f"""Develop an equation for the given graph.
        Note that the vertex is at
        \\(
            (x, y) = \\left({latex(self.avg)}, {latex(f(self.avg))}\\right).
        \\)
        """
        self.prompt_multiple = """For each of the following,
        develop an equation for the given graph."""

        avg = self.avg
        x_points = [x1, x2, avg]
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


    name = 'Intercept-Form from Graph'
    module_name = 'graph_intercept_form_to_equation'


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
        return f'\(y = {commute_sum(user_answer)}\)'

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




Question_Class = GraphInterceptFormToEquation
