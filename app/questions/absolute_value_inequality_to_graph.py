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

class AbsoluteValueInequalityToGraph(Question):
    """
    The given is
    \\[
        |a(x - mid)| Q a(r - mid),
    \\]
    where Q is any inequality and mid = (l + r)/2.
    (The answer involves just l and r.)

    For difficulty == 1, a == 1.
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
            signs = ['\\leq', '\\lt', '\\geq', '\\gt']
            self.Q = random.choice(signs)
        if self.Q in ['\\leq', '\\lt']:
            self.logical_connector = 'and'
        else:
            self.logical_connector = 'or'
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')
        if 'l' in kwargs:
            self.l = kwargs['l']
        else:
            self.l = random.randint(-18,15)
        if 'r' in kwargs:
            self.r = kwargs['r']
        else:
            offset_max = abs((20-self.l)) - 2
            self.r = self.l + random.randint(1, offset_max)
        self.mid = Rational(self.l + self.r, 2)
        if 'difficulty' in kwargs:
            self.difficulty = kwargs['difficulty']
        else:
            self.difficulty = random.choice([1, 1, 2])
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            if self.difficulty == '1':
                self.a = 1
            else:
                if (self.r - self.l) % 2 == 1:
                    self.a = random.choice([2, 4, 6])
                else:
                    self.a = random.randint(2,5)

        self.genproblem()

        # self.given_latex = latex_print(self.given)
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        # self.format_answer = self.answer
    prob_type = prob_type

    name = 'Absolute Value Inequality to Graph'
    module_name = 'absolute_value_inequality_to_graph' #added in the course of creating test generator

    prompt_single = """Graph the solution set."""
    prompt_multiple = """For each of the following, graph the solution set."""
    further_instruction = """Give your answer by graphing on the real line.
    """

    loom_link = """https://www.loom.com/share/61ff8ffe777b480c97625562f3ad5475"""

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        a = self.a
        mid = self.mid
        l = self.l
        r = self.r
        Q = self.Q
        if self.logical_connector == 'and':
            if Q == '\\lt':
                self.answer = Interval.open(self.l, self.r)
                self.ineq_answers = set([x > self.l, x < self.r])
                points_info = [{'x': self.l, 'type': 'empty'}, {'x': self.r, 'type': 'empty'}]
                self.answer_points = json.dumps(points_info)
                intervals_info = [[self.l, self.r]]
                self.answer_intervals = json.dumps(intervals_info)
            else: # Q == '\\leq'
                self.answer = Interval(self.l, self.r)
                self.ineq_answers = set([x >= self.l, x <= self.r])
                points_info = [{'x': self.l, 'type': 'filled'}, {'x': self.r, 'type': 'filled'}]
                self.answer_points = json.dumps(points_info)
                intervals_info = [[self.l, self.r]]
                self.answer_intervals = json.dumps(intervals_info)
            self.format_answer = f'\\( {self.l} {self.Q} x \\; \\textrm{{and}} \\; x {self.Q} {self.r} \\)'
        else:
            if Q == '\\gt':
                self.answer_left = Interval.open(-oo, self.l)
                self.answer_right = Interval.open(self.r, oo)
                self.answer = self.answer_left.union(self.answer_right)
                self.ineq_answers = set([x < self.l, x > self.r])
                points_info = [{'x': self.l, 'type': 'empty'}, {'x': self.r, 'type': 'empty'}]
                self.answer_points = json.dumps(points_info)
                intervals_info = [[-20, self.l], [self.r, 20]]
                self.answer_intervals = json.dumps(intervals_info)
            else: # Q == '\\geq'
                self.answer_left = Interval(-oo, self.l)
                self.answer_right = Interval(self.r, oo)
                self.answer = self.answer_left.union(self.answer_right)
                self.ineq_answers = set([x <= self.l, x >= self.r])
                points_info = [{'x': self.l, 'type': 'filled'}, {'x': self.r, 'type': 'filled'}]
                self.answer_points = json.dumps(points_info)
                intervals_info = [[-20, self.l], [self.r, 20]]
                self.answer_intervals = json.dumps(intervals_info)
            self.format_answer = f'\\( x {AbsoluteValueInequalityToGraph.switchQ(Q)} {self.l}  \\; \\textrm{{or}} \\; {self.r}  {AbsoluteValueInequalityToGraph.switchQ(Q)} x \\)'

        self.given_latex_display = f"""
        \\[ {latex(abs(a*(x-mid)))} {Q} {latex(a*(r-mid))} \\]
        """
        self.format_given_for_tex = f"""
        {self.prompt_single}

        \\[ {latex(abs(a*(x-mid)))} {Q} {latex(a*(r-mid))} \\]
        """

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
            left, right = interval
            print(left, right)
            if left <= -20:
                left = -oo
                type_of_left = 'empty'
            else:
                type_of_left = AbsoluteValueInequalityToGraph.get_point(left, user_points)['type']
            if right >= 20:
                right = oo
                type_of_right = 'empty'
            else:
                type_of_right = AbsoluteValueInequalityToGraph.get_point(right, user_points)['type']
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



Question_Class = AbsoluteValueInequalityToGraph
