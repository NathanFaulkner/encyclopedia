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

class AbsoluteValueBasicGraphToEquation(Question):
    """
    The given is of the form

    \\[
        y = Rational(p,q)|x - x0| + y0
    \\]

    The student is expected to graph by plotting points.  3 is sufficient.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'num_transformations' in kwargs:
            self.num_transformations = kwargs['num_transformation']
        else:
            self.num_transformations = random.choice([1, 2, 3])
        transformation_options = ['vert', 'horiz', 'refl']
        if 'transformations' in kwargs:
            self.transformations = kwargs['transformations']
        else:
            self.transformations = random.sample(transformation_options, self.num_transformations)
        if 'refl' in self.transformations:
            self.m = -1
        else:
            self.m = 1
        if 'm' in kwargs:
            self.m = kwargs['m']
        if 'x0' in kwargs:
            self.x0 = kwargs['x0']
        else:
            if 'horiz' in self.transformations:
                self.x0 = random_non_zero_integer(-5,5)
            else:
                self.x0 = 0
        if 'y0' in kwargs:
            self.y0 = kwargs['y0']
        else:
            if 'vert' in self.transformations:
                self.y0 = random.randint(-5,5)
            else:
                self.y0 = 0
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        self.genproblem()

        # self.given = self.problem['given']
        # self.answer = self.problem['answer']
        # term = factor(self.m*(self.x - self.x0))
        # if self.y0 > 0:
        #     fmt_y0 = latex(self.y0)
        #     sign = '+'
        # elif self.y0 == 0:
        #     fmt_y0 = ''
        #     sign = ''
        # else:
        #     fmt_y0 = latex(abs(self.y0))
        #     sign = '-'
        # # print(term)
        # try:
        #     self.format_given = f"""
        #     \\[
        #      y = {latex(term.args[0])} ({latex(term.args[1])}) {sign} {fmt_y0}
        #     \\]
        #     """
        # except IndexError:
        #     self.format_given = f"""
        #     \\[
        #      y = ({latex(term)}) {sign} {fmt_y0}
        #     \\]
        #     """

        self.prompt_single =  """Develop an equation for the line
        that passes through the given points.
        """
        self.prompt_multiple = """For each of the following,
        develop an equation for the line
        that passes through the given points."""

        points = []
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

        self.format_answer = f'\( y = {commute_sum(self.answer)}\)'





    name = 'Equation from Basic Absolute Value Graph'
    module_name = 'graph_absolute_value_basic_to_equation'




    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        b = self.y0
        h = self.x0
        # p = self.p
        # q = self.q
        m = self.m
        self.as_lambda = lambda x: m*abs(x - h) + b
        f = self.as_lambda
        self.given = factor(m*abs(x-h)) + b
        #print('3rd step: So far its ', expr)
        self.answer = f(x)

    has_img = True

    def save_img(self, filename):
        graph = GraphFromLambda(self.as_lambda)
        graph.save_fig(filename)

    def get_svg_data(self, window=[-10,10], res=1000):
        x_min = window[0]
        x_max = window[1]
        x_points = np.array([-10, self.x0, 10])
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
        return f'\({latex(lhs)} = {latex(rhs)}\)'

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




Question_Class = AbsoluteValueBasicGraphToEquation
