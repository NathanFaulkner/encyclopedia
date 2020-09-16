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

class AbsoluteValueInequality(Question):
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

    name = 'Absolute Value Inequality'
    module_name = 'absolute_value_inequality'

    prompt_single = """Solve the absolute value inequality."""
    prompt_multiple = """Solve each of the following absolute value inequalities."""
    further_instruction = """Enter \\(\\leq\\) as "<=" and \\(\\geq\\)
    as ">=".  For instance, a possible answer might be "x <= -9/5".
    Enter logical connectors as "and" or "or", as in
    "-4 < x and x <= 5" or "x < -4 or x >= 5".  In particular,
    the answer-checking algorithm has NOT been programmed
    to understand the expression "-4 < x <= 5"---where no logical
    connecter has been supplied.  (Use "and"!)  You were warned!
    """

    loom_link = """https://www.loom.com/share/094b113d2d28457fbed0398171325949"""

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
            else: # Q == '\\leq'
                self.answer = Interval(self.l, self.r)
                self.ineq_answers = set([x >= self.l, x <= self.r])
            self.format_answer = f'\\( {self.l} {Q} x \\; \\textrm{{and}} \\; x {Q} {self.r} \\)'
        else:
            if Q == '\\gt':
                self.answer_left = Interval.open(-oo, self.l)
                self.answer_right = Interval.open(self.r, oo)
                self.answer = self.answer_left.union(self.answer_right)
                self.ineq_answers = set([x < self.l, x > self.r])
            else: # Q == '\\geq'
                self.answer_left = Interval(-oo, self.l)
                self.answer_right = Interval(self.r, oo)
                self.answer = self.answer_left.union(self.answer_right)
                self.ineq_answers = set([x <= self.l, x >= self.r])
            self.format_answer = f'\\( x {AbsoluteValueInequality.switchQ(Q)} {self.l}  \\; \\textrm{{or}} \\; {self.r}  {AbsoluteValueInequality.switchQ(Q)} x \\)'

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
        if 'and' in user_answer:
            if self.logical_connector == 'or':
                return False
            user_answer = user_answer.split('and')
        elif 'or' in user_answer:
            if self.logical_connector == 'and':
                return False
            user_answer = user_answer.split('or')
        else:
            return False
        if len(user_answer) != 2:
            return False
        user_answer[0] = user_answer[0].replace('^', '**')
        user_answer[0] = parse_expr(user_answer[0], transformations=transformations)
        user_answer[1] = user_answer[1].replace('^', '**')
        user_answer[1] = parse_expr(user_answer[1], transformations=transformations)
        user_answer = set(user_answer)
        print('correct', self.ineq_answers, type(list(self.ineq_answers)[0]), 'user', user_answer, type(list(user_answer)[0]))
        print('union', self.ineq_answers.union(user_answer))
        # return self.ineq_answers == user_answer
        cong = AbsoluteValueInequality.congruent
        user_answer = list(user_answer)
        answers = list(self.ineq_answers)
        one_way = cong(user_answer[0], answers[0]) and cong(user_answer[1], answers[1])
        the_other = cong(user_answer[0], answers[1]) and cong(user_answer[1], answers[0])
        return one_way or the_other

    @staticmethod
    def congruent(ineq1, ineq2):
        try:
            return ineq1.equals(ineq2)
        except TypeError:
            return false


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
        if 'and' in user_answer:
            user_splitter = 'and'
            user_answer = user_answer.split('and')
        elif 'or' in user_answer:
            user_splitter = 'or'
            user_answer = user_answer.split('or')
        else:
            return "Your answer wasn't intellible"
        if len(user_answer) != 2:
            return "Your answer wasn't intellible"
        user_answer[0] = user_answer[0].replace('^', '**')
        user_answer[0] = parse_expr(user_answer[0], transformations=transformations)
        user_answer[1] = user_answer[1].replace('^', '**')
        user_answer[1] = parse_expr(user_answer[1], transformations=transformations)
        return f'\\( {latex(user_answer[0])} \\; \\textrm{{ {user_splitter} }} \\; {latex(user_answer[1])} \\)'


    @classmethod
    def validator(self, user_answer):
        try:
            if 'and' in user_answer:
                user_answer = user_answer.split('and')
            elif 'or' in user_answer:
                user_answer = user_answer.split('or')
            else:
                raise SyntaxError
            user_answer[0] = user_answer[0].replace('^', '**')
            user_answer[0] = parse_expr(user_answer[0], transformations=transformations)
            user_answer[1] = user_answer[1].replace('^', '**')
            user_answer[1] = parse_expr(user_answer[1], transformations=transformations)
            user_answer = set(user_answer)
        except:
            raise SyntaxError



Question_Class = AbsoluteValueInequality
