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
                            tolerates,
                            get_coeff)
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

class PolynomialCurveToEquation(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        x = sy.Symbol('x')
        self.x = x
        degree = random.choice([3,4])
        #degree = 4
        zeroes = []
        force_duplicate = random.choice([True, False])
        # force_duplicate = True

        def have_duplicate(a):
            return len(a) != len(set(a))

        if force_duplicate:
            while not(have_duplicate(zeroes)):
                zeroes = []
                for i in range(degree):
                    z = random.randint(-5,5)
                    while any([abs(z-r) == 1 for r in zeroes]):
                        z = random.randint(-5,5)
                    zeroes.append(z)
        else:
            for i in range(degree):
                    z = random.randint(-5,5)
                    while any([abs(z-r) == 1 for r in zeroes]):
                        z = random.randint(-5,5)
                    zeroes.append(z)
        # print(zeroes)

        y_0 = random.randint(-9,9)
        prod = 1
        x_0 = 0
        while x_0 in zeroes:
            x_0 = random_non_zero_integer(-5,5)
        for z in zeroes:
            prod *= (x_0-z)
        LC = sy.Rational(y_0, prod)

        def f(x):
            out = LC
            for i in range(degree):
                out *= (x-zeroes[i])
            return out

        self.answer = f(x)
        # print('answer', self.answer)

        expr = sy.simplify(1/LC*f(x))

        self.as_lambda = sy.lambdify(x, f(x))
        # f = self.as_lambda
        self.given = sy.factor(f(x))
        # self.format_given = f'\\(f(x) = {sy.latex(LC)}{sy.latex(expr)}\\)'


        self.format_answer = f'\\(f(x) = {sy.latex(LC)}{sy.latex(expr)}\\)'

        self.prompt_single = f"""Give an equation for the given graph.  Note
        that the graph passes through the point \\({sy.latex((x_0, y_0))}\\)"""

        self.further_instruction = """Write 'f(x) =' or 'y = ' and then
        and expression for your function.
        """

        self.format_given_for_tex = f"""
        {self.prompt_single}
        """

        points = [[z, 0] for z in zeroes]
        points += [[x_0, y_0]]
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

    name = 'Polynomial Curve To Equation'
    module_name = 'polynomial_curve_to_equation'

    prompt_multiple = """TBA"""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    has_img = True

    def save_img(self, filename):
        graph = GraphFromLambda(self.as_lambda)
        graph.save_fig(filename)

    def get_svg_data(self, window=[-10,10], res=100):
        x_min = window[0]
        x_max = window[1]
        x_points = np.linspace(x_min, x_max, res)
        # print('x_points', x_points)
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
        user_answer = user_answer.replace(' ', '')
        user_answer = user_answer.replace('f(x)', 'y')
        if 'y' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = sy.Eq(lhs, rhs)
        y = sy.Symbol('y')
        user_answer = sy.solve(user_answer, y)[0]
        # print(sy.expand(self.answer), '\n', sy.expand(user_answer))
        # print('LC = ', lc)
        return self.answer.equals(user_answer)


    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace(' ', '')
        user_answer = user_answer.replace('f(x)', 'y')
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = sy.Eq(lhs, rhs)
        y = sy.Symbol('y')
        user_answer = sy.solve(user_answer, y)[0]
        lc = get_coeff(user_answer)
        if lc == 1:
            fmt_lc = ''
        elif lc == -1:
            fmt_lc = '-'
        else:
            fmt_lc = sy.latex(lc)
        expr = user_answer/lc
        return f'\({sy.latex(lhs)} = {fmt_lc}{sy.latex(sy.factor(expr))}\)'

    @staticmethod
    def validator(user_answer):
        try:
            # pass
            user_answer = user_answer.lower()
            user_answer = user_answer.replace(' ', '')
            user_answer = user_answer.replace('f(x)', 'y')
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = sy.Eq(lhs, rhs)
            y = sy.Symbol('y')
            user_answer = sy.solve(user_answer, y)[0]
            lc = get_coeff(user_answer)
            if lc == 1:
                fmt_lc = ''
            elif lc == -1:
                fmt_lc = '-'
            else:
                fmt_lc = sy.latex(lc)
            expr = user_answer/lc
        except:
            raise SyntaxError




Question_Class = PolynomialCurveToEquation
