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

class GraphOfCompoundLinearInequality(Question):
    """
    The given is
    \\[
        l1 Q1 a(x + b) + c Q2 r1 ,
    \\]
    where QX is \\lt or \\leq
    or
    \\[
        a(x + b) + c Q1 l1 \\quad \\textrm{or} \\quad e(x+f) + g Q2 r1,
    \\]
    where Q1 is \\lt or \\leq and Q2 is \\gt or \\geq.
    All the values are actually generated from the answer, which
    is either of the form
    \\[
        l Q1 x Q2 r
    \\]
    or
    \\[
        x Q1 l \\quad \\textrm{or} \\quad x Q2 r
    \\]

    Which is returned is determined by self.logical_connector,
    which is either 'and' or 'or'.

    Terms are randomly allowed to collapse depending on difficulty.

    e(x+f) + g can be forced same as a(x+b) + c using
    self.force_same = True, provided the logical connector is 'or'.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'logical_connector' in kwargs:
            self.logical_connector = kwargs['logical_connector']
        else:
            self.logical_connector = random.choice(['and', 'or'])
        if 'Q1' in kwargs:
            self.Q1 = kwargs['Q1']
        else:
            signs = ['\\leq', '\\lt']
            self.Q1 = random.choice(signs)
        if 'Q2' in kwargs:
            self.Q2 = kwargs['Q2']
        else:
            if self.logical_connector == 'and':
                signs = ['\\leq', '\\lt']
                self.Q2 = random.choice(signs)
            else:
                signs = ['\\geq', '\\gt']
                self.Q2 = random.choice(signs)
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
        if 'difficulty' in kwargs:
            self.difficulty = kwargs['difficulty']
        else:
            self.difficulty = random.choice([1, 1, 2])
        if self.difficulty == '1':
            self.force_same = True
        else:
            self.force_same = random.choice([True, False])
        if self.logical_connector == 'and':
            self.force_same = True
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
            self.c = random.randint(-9,9)
        if self.force_same:
            self.e = self.a
            self.f = self.b
            self.g = self.c
        else:
            if 'e' in kwargs:
                self.e = kwargs['e']
            else:
                self.e = random_non_zero_integer(-9,9)
            if 'f' in kwargs:
                self.f = kwargs['f']
            else:
                self.f = random.randint(-9,9)
            if 'g' in kwargs:
                self.g = kwargs['g']
            else:
                self.g = random.randint(-9,9)
        self.l1 = self.a*(self.l+self.b)+self.c
        if self.logical_connector == 'and':
            self.r1 = self.a*(self.r+self.b)+self.c
        else:
            self.r1 = self.e*(self.r+self.f)+self.g

        self.genproblem()
        # self.given_latex = latex_print(self.given)
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        # self.format_answer = self.answer
    prob_type = prob_type

    name = 'Graph of Compound Linear Inequality'
    module_name = 'graph_of_compound_linear_inequality' #added in the course of creating test generator

    prompt_single = """Solve the compound linear inequality."""
    prompt_multiple = """Solve each of the following compound linear inequalities."""
    further_instruction = """Give your answer by graphing on the real line.
    """

    loom_link = """https://www.loom.com/share/533779725fae4424b50e71c8f51bd888"""

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        a = self.a
        b = self.b
        c = self.c
        e = self.e
        f = self.f
        g = self.g
        l1 = self.l1
        r1 = self.r1
        if self.difficulty == 1:
            term1 = a*(x+b)
            term2 = e*(x+f)
        else:
            term1 = factor(a*(x+b))
            term2 = factor(e*(x+f))
        Q1 = self.Q1
        Q2 = self.Q2
        if self.logical_connector == 'and':
            if Q1 == '\\lt':
                if Q2 == '\\lt':
                    self.answer = Interval.open(self.l, self.r)
                    self.ineq_answers = set([x > self.l, x < self.r])
                    points_info = [{'x': self.l, 'type': 'empty'}, {'x': self.r, 'type': 'empty'}]
                    self.answer_points = json.dumps(points_info)
                    intervals_info = [[self.l, self.r]]
                    self.answer_intervals = json.dumps(intervals_info)
                else:
                    self.answer = Interval.Lopen(self.l, self.r)
                    self.ineq_answers = set([x > self.l, x <= self.r])
                    points_info = [{'x': self.l, 'type': 'empty'}, {'x': self.r, 'type': 'filled'}]
                    self.answer_points = json.dumps(points_info)
                    intervals_info = [[self.l, self.r]]
                    self.answer_intervals = json.dumps(intervals_info)
            else: # Q1 == '\\leq'
                if Q2 == '\\lt':
                    self.answer = Interval.Ropen(self.l, self.r)
                    self.ineq_answers = set([x >= self.l, x < self.r])
                    points_info = [{'x': self.l, 'type': 'filled'}, {'x': self.r, 'type': 'empty'}]
                    self.answer_points = json.dumps(points_info)
                    intervals_info = [[self.l, self.r]]
                    self.answer_intervals = json.dumps(intervals_info)
                else:
                    self.answer = Interval(self.l, self.r)
                    self.ineq_answers = set([x >= self.l, x <= self.r])
                    points_info = [{'x': self.l, 'type': 'filled'}, {'x': self.r, 'type': 'filled'}]
                    self.answer_points = json.dumps(points_info)
                    intervals_info = [[self.l, self.r]]
                    self.answer_intervals = json.dumps(intervals_info)
            self.format_answer = f'\\( {self.l} {self.Q1} x \\; \\textrm{{and}} \\; x {self.Q2} {self.r} \\)'
        else:
            if Q1 == '\\lt':
                if Q2 == '\\gt':
                    self.answer_left = Interval.open(-oo, self.l)
                    self.answer_right = Interval.open(self.r, oo)
                    self.answer = self.answer_left.union(self.answer_right)
                    self.ineq_answers = set([x < self.l, x > self.r])
                    points_info = [{'x': self.l, 'type': 'empty'}, {'x': self.r, 'type': 'empty'}]
                    self.answer_points = json.dumps(points_info)
                    intervals_info = [[-20, self.l], [self.r, 20]]
                    self.answer_intervals = json.dumps(intervals_info)
                else:
                    self.answer_left = Interval.open(-oo, self.l)
                    self.answer_right = Interval(self.r, oo)
                    self.answer = self.answer_left.union(self.answer_right)
                    self.ineq_answers = set([x < self.l, x >= self.r])
                    points_info = [{'x': self.l, 'type': 'empty'}, {'x': self.r, 'type': 'filled'}]
                    self.answer_points = json.dumps(points_info)
                    intervals_info = [[-20, self.l], [self.r, 20]]
                    self.answer_intervals = json.dumps(intervals_info)
            else: # Q1 == '\\leq'
                if Q2 == '\\gt':
                    self.answer_left = Interval(-oo, self.l)
                    self.answer_right = Interval.open(self.r, oo)
                    self.answer = self.answer_left.union(self.answer_right)
                    self.ineq_answers = set([x <= self.l, x > self.r])
                    points_info = [{'x': self.l, 'type': 'filled'}, {'x': self.r, 'type': 'empty'}]
                    self.answer_points = json.dumps(points_info)
                    intervals_info = [[-20, self.l], [self.r, 20]]
                    self.answer_intervals = json.dumps(intervals_info)
                else:
                    self.answer_left = Interval(-oo, self.l)
                    self.answer_right = Interval(self.r, oo)
                    self.answer = self.answer_left.union(self.answer_right)
                    self.ineq_answers = set([x <= self.l, x >= self.r])
                    points_info = [{'x': self.l, 'type': 'filled'}, {'x': self.r, 'type': 'filled'}]
                    self.answer_points = json.dumps(points_info)
                    intervals_info = [[-20, self.l], [self.r, 20]]
                    self.answer_intervals = json.dumps(intervals_info)
            self.format_answer = f'\\( x {self.Q1} {self.l}  \\; \\textrm{{or}} \\; {self.r}  {GraphOfCompoundLinearInequality.switchQ(Q2)} x \\)'
        if a < 0:
            given_Q1 = GraphOfCompoundLinearInequality.switchQ(Q1)
        else:
            given_Q1 = Q1
        if e < 0:
            given_Q2 = GraphOfCompoundLinearInequality.switchQ(Q2)
        else:
            given_Q2 = Q2
        if self.logical_connector == 'and':
            self.given_latex_display = f"""
            \\[ {l1} {given_Q1} {latex(term1 + c)} {given_Q2} {r1} \\]
            """
            self.format_given_for_tex = f"""
            {self.prompt_single}

            \\[ {l1} {given_Q1} {latex(term1 + c)} {given_Q2} {r1} \\]
            """
        else:
            self.given_latex_display = f"""
            \\[ {latex(term1 + c)} {given_Q1} {l1} \\quad
                \\textrm{{or}} \\quad
               {latex(term2 + g)} {given_Q2} {r1}\\]
            """
            self.format_given_for_tex = f"""
            Solve the compound linear inequality. Graph your answer on the real line.

            \\[ {latex(term1 + c)} {given_Q1} {l1} \\quad
                \\textrm{{or}} \\quad
               {latex(term2 + g)} {given_Q2} {r1}\\]
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
                type_of_left = GraphOfCompoundLinearInequality.get_point(left, user_points)['type']
            if right >= 20:
                right = oo
                type_of_right = 'empty'
            else:
                type_of_right = GraphOfCompoundLinearInequality.get_point(right, user_points)['type']
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
        # print(self.answer, sympy_answer)
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



Question_Class = GraphOfCompoundLinearInequality
