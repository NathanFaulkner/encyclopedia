#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, \
                EqualTo, Length, InputRequired

import random
# from sympy.parsing.sympy_parser import parse_expr
# from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
# transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *
import numpy as np
import json

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation)
# from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general

class RealLineForm(FlaskForm):
    points = HiddenField(id="points_field")
    intervals = HiddenField(id="intervals_field")
    submit = SubmitField('Submit')

form = RealLineForm

prob_type = 'real_line_graph'

class GraphOfLinearInequality(Question):
    """
    The given is
    \\[
        a(x+b) + c(x+d) + ex - f Q 0,
    \\]
    but permuted with Q, where Q is an inequality.
    .  Terms are randomly allowed to collapse.
    A fraction, no solution, and all reals are possible.
    f = a(bdry+b) + c(bdry+d) + e*bdry
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'Q' in kwargs:
            self.Q = kwargs['Q']
        else:
            signs = ['\\leq', '\\geq', '\\lt', '\\gt']
            self.Q = random.choice(signs)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-9,9)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.randint(-9,9)
        if 'c' in kwargs:
            self.c = kwargs['c']
        else:
            self.c = random_non_zero_integer(-9,9)
        if 'd' in kwargs:
            self.d = kwargs['d']
        else:
            self.d = random.randint(-9,9)
        if 'e' in kwargs:
            self.e = kwargs['e']
        else:
            offset = random_non_zero_integer(-9,9)
            self.e = -(self.a + self.c) + offset
        if 'bdry' in kwargs:
            self.bdry = kwargs['bdry']
        else:
            p = random.randint(-15,15)
            q = int(random.triangular(1,1,9))
            self.bdry = Rational(p,q)
        if 'f' in kwargs:
            self.f = kwargs['f']
        else:
            self.f = self.a*(self.bdry+self.b) + self.c*(self.bdry+self.d) + self.e*self.bdry
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')
        if 'difficulty' in kwargs:
            self.difficulty = kwargs['difficulty']
        else:
            self.difficulty = random.choice([1, 1, 1, 2, 3])

        self.genproblem()

        # self.given_latex = latex_print(self.given)
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        # self.format_answer = self.answer
    prob_type = prob_type

    name = 'Linear Inequality'
    module_name = 'graph_of_linear_inequality'

    prompt_single = """Solve the linear inequality."""
    prompt_multiple = """Solve each of the following linear inequalities."""
    further_instruction = """Give your answer by graphing on the real line.
    """

    loom_link = """https://www.loom.com/share/018b59d2e8074858b9379b736377bf4d"""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        f = self.f
        if self.difficulty == 2:
            term1 = factor(a*(x+b))
        else:
            term1 = a*(x+b)
        if self.difficulty == 3:
            term2 = factor(c*(x+d))
        else:
            term2 = c*(x+d)
        terms = [term1, term2, e*x, -f]
        LHS, RHS = permute_equation(terms, as_list=True)
        Q = self.Q
        self.given_latex_display = f'\\[ \n \t {latex(LHS)} {Q} {latex(RHS)} \n \\]'
        self.format_given = self.given_latex_display
        self.format_given_for_tex = f"""
        {self.prompt_single}

        \\[ \n \t {latex(LHS)} {Q} {latex(RHS)} \n \\]
        """
        self.given = [LHS, RHS]
        #print('3rd step: So far its ', expr)
        bdry = self.bdry #Rational(-(a*b+c*d-f), a+c+e)
        if a + c + e < 0:
            Q = GraphOfLinearInequality.switchQ(Q)
        if Q == '\\lt':
            self.answer = Interval.Ropen(-oo, float(bdry))
            self.ineq_answer = x < bdry
            points_info = [{'x': float(bdry), 'type': 'empty'}]
            self.answer_points = json.dumps(points_info)
            intervals_info = [[-20, float(bdry)]]
            self.answer_intervals = json.dumps(intervals_info)
        if Q == '\\leq':
            self.answer = Interval(-oo, float(bdry))
            self.ineq_answer = x <= bdry
            points_info = [{'x': float(bdry), 'type': 'filled'}]
            self.answer_points = json.dumps(points_info)
            intervals_info = [[-20, float(bdry)]]
            self.answer_intervals = json.dumps(intervals_info)
        if Q == '\\gt':
            self.answer = Interval.Lopen(float(bdry), oo)
            self.ineq_answer = x > bdry
            points_info = [{'x': float(bdry), 'type': 'empty'}]
            self.answer_points = json.dumps(points_info)
            intervals_info = [[float(bdry), 20]]
            self.answer_intervals = json.dumps(intervals_info)
        if Q == '\\geq':
            self.answer = Interval(float(bdry), oo)
            self.ineq_answer = x >= bdry
            points_info = [{'x': float(bdry), 'type': 'filled'}]
            self.answer_points = json.dumps(points_info)
            intervals_info = [[float(bdry), 20]]
            self.answer_intervals = json.dumps(intervals_info)
        self.format_answer = f'\\( x {Q} {latex(bdry)} \\)'

    # def get_svg_data(self, window):
    #     x_min = window[0]
    #     x_max = window[1]
    #     x_points = np.array([x_min, x_max])
    #     y_points = self.as_lambda(x_points)
    #     x_points = cart_x_to_svg(x_points)
    #     y_points = cart_y_to_svg(y_points)
    #     poly_points = ""
    #     l = len(x_points)
    #     i = 0
    #     while i < l:
    #         poly_points += f"{x_points[i]},{y_points[i]} "
    #         i += 1
    #     return poly_points


    def checkanswer(self, user_answer):
        user_intervals = user_answer['user_intervals']
        user_points = user_answer['user_points']
        # user_points.sort(key=lambda point: point["x"])
        # print(user_points)
        sympy_intervals = []
        for interval in user_intervals:
            # print('interval', interval)
            left, right = interval
            # print(left, right)
            if left <= -20:
                left = -oo
                type_of_left = 'empty'
            else:
                type_of_left = GraphOfLinearInequality.get_point(left, user_points)['type']
            if right >= 20:
                right = oo
                type_of_right = 'empty'
            else:
                type_of_right = GraphOfLinearInequality.get_point(right, user_points)['type']
            if type_of_left == 'filled':
                if type_of_right == 'filled':
                    sympy_interval = Interval(left, right)
                else:
                    sympy_interval = Interval.Ropen(left, right)
            else:
                if type_of_right == 'filled':
                    sympy_interval = Interval.Lopen(left, right)
                else:
                    sympy_interval = Interval.open(left, right)
            sympy_intervals.append(sympy_interval)
        sympy_answer = Union(*sympy_intervals)
        print(self.answer, sympy_answer)
        # difference = sympy_answer.symmetric_difference(self.answer)
        # measure_difference = difference.measure
        # return measure_difference < 0.001
        return self.answer == sympy_answer

    @staticmethod
    def get_point(value, list_of_dictionaries, key='x'):
        """The value of the key searched on is assumed unique for
        the dictionaries on this list"""
        for d in list_of_dictionaries:
            if d[key] == value:
                return d

    @staticmethod
    def switchQ(Q):
        if Q == '\\lt':
            return '\\gt'
        if Q == '\\gt':
            return '\\lt'
        if Q == '\\geq':
            return '\\leq'
        if Q == '\\leq':
            return '\\geq'

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return latex_print(user_answer, display)

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError



Question_Class = GraphOfLinearInequality
