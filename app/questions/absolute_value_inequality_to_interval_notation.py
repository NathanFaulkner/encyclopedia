#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from flask_wtf import FlaskForm
# from wtforms import SubmitField, StringField, HiddenField
# from wtforms.validators import DataRequired, ValidationError, Email, \
#                 EqualTo, Length, InputRequired

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
                            permute_equation)
# from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general

# class RealLineForm(FlaskForm):
#     points = HiddenField(id="points_field")
#     intervals = HiddenField(id="intervals_field")
#     submit = SubmitField('Submit')

# form = RealLineForm

prob_type = 'math_blank'

class AbsoluteValueInequalityToIntervalNotation(Question):
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
    prob_type = 'math_blank'

    name = 'Absolute Value Inequality Notation to Interval Notation'
    module_name = 'absolute_value_inequality_to_interval_notation'

    prompt_single = """Write the solution set in interval notation."""
    prompt_multiple = """For each of the following, write the the solution set in interval notation."""
    further_instruction = """
    <ul>
        <li>Use 'U' (capitalized, no quotes) for union.</li>
        <li>Type 'oo'  (no quotes) for \(\infty\) or '-oo'  for \(-\infty\).
    </ul>
    """

    loom_link = """https://www.loom.com/share/c4df440b24104dddbcb3360063721607"""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        a = self.a
        l = self.l
        r = self.r
        Q = self.Q
        mid = self.mid
        if self.logical_connector == 'and':
            if Q == '\\lt':
                self.answer = Interval.open(self.l, self.r)
                self.ineq_answers = set([x > self.l, x < self.r])
                self.format_answer = f'\\( ({l}, {r}) \\)'
            else: # Q == '\\leq'
                self.answer = Interval(self.l, self.r)
                self.ineq_answers = set([x >= self.l, x <= self.r])
                self.format_answer = f'\\( [{l}, {r}] \\)'
        else:
            if Q == '\\gt':
                self.answer_left = Interval.open(-oo, self.l)
                self.answer_right = Interval.open(self.r, oo)
                self.answer = self.answer_left.union(self.answer_right)
                self.ineq_answers = set([x < self.l, x > self.r])
                self.format_answer = f'\\( (-\\infty, {l}) \\cup ({r}, \\infty) \\)'
            else: # Q == '\\geq'
                self.answer_left = Interval(-oo, self.l)
                self.answer_right = Interval(self.r, oo)
                self.answer = self.answer_left.union(self.answer_right)
                self.ineq_answers = set([x <= self.l, x >= self.r])
                self.format_answer = f'\\( (-\\infty, {l}] \\cup [{r}, \\infty) \\)'

        self.given_latex_display = f"""
        \\[ {latex(abs(a*(x-mid)))} {Q} {latex(a*(r-mid))} \\]
        """
        self.format_given_for_tex = f"""
        {self.prompt_single}

        \\[ {latex(abs(a*(x-mid)))} {Q} {latex(a*(r-mid))} \\]
        """

    @staticmethod
    def parse_as_interval(interval_string):
        left_open = False
        right_open = False
        interval_string = interval_string.replace(' ', '')
        if '(' in interval_string:
            left_open = True
        if ')' in interval_string:
            right_open = True
        interval_string = interval_string.replace('(', '')
        interval_string = interval_string.replace(')', '')
        interval_string = interval_string.replace('[', '')
        interval_string = interval_string.replace(']', '')
        a, b = interval_string.split(',')
        a = sympify(a)
        b = sympify(b)
        if left_open:
            if right_open:
                return Interval.open(a, b)
            else:
                return Interval.Lopen(a,b)
        else:
            if right_open:
                return Interval.Ropen(a, b)
            else:
                return Interval(a,b)

    def checkanswer(self, user_answer):
        if 'U' in user_answer:
            if self.logical_connector == 'and':
                return False
            user_intervals = user_answer.split('U')
            i = 0
            while i < len(user_intervals):
                user_intervals[i] = AbsoluteValueInequalityToIntervalNotation.parse_as_interval(user_intervals[i])
                i += 1
            user_answer = user_intervals[0]
            for interval in user_intervals:
                user_answer = user_answer.union(interval)
        else:
            if self.logical_connector == 'or':
                return False
            user_answer = AbsoluteValueInequalityToIntervalNotation.parse_as_interval(user_answer)
        return user_answer == self.answer

    @staticmethod
    def congruent(ineq1, ineq2):
        return ineq1.equals(ineq2)


    # @staticmethod
    # def set_congruence(set1, set2, congr_rel):
    #     for elem in set1:
    #         while len(set2) > 0:
    #             list_set2 = list(set2)
    #             for comp_elem in list_set2:
    #                 if congruent(elem, comp_elem):
    #                     set2.remove(comp_elem)
    #                     break


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
        if 'U' in user_answer:
            user_intervals = user_answer.split('U')
            i = 0
            while i < len(user_intervals):
                user_intervals[i] = AbsoluteValueInequalityToIntervalNotation.parse_as_interval(user_intervals[i])
                i += 1
            user_answer = user_intervals[0]
            for interval in user_intervals:
                user_answer = user_answer.union(interval)
        else:
            user_answer = AbsoluteValueInequalityToIntervalNotation.parse_as_interval(user_answer)
        return f'\\( {latex(user_answer)} \\)'

    @classmethod
    def validator(self, user_answer):
        try:
            if 'U' in user_answer:
                user_intervals = user_answer.split('U')
                i = 0
                while i < len(user_intervals):
                    user_intervals[i] = AbsoluteValueInequalityToIntervalNotation.parse_as_interval(user_intervals[i])
                    i += 1
                user_answer = user_intervals[0]
                for interval in user_intervals:
                    user_answer = user_answer.union(interval)
            else:
                user_answer = AbsoluteValueInequalityToIntervalNotation.parse_as_interval(user_answer)
        except:
            raise SyntaxError



Question_Class = AbsoluteValueInequalityToIntervalNotation
