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

class CompoundLinearInequality(Question):
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
    prob_type = 'math_blank'

    name = 'Compound Linear Inequality'

    prompt_single = """Solve the compound linear inequality."""
    prompt_multiple = """Solve each of the following compound linear inequalities."""
    further_instruction = """Enter \\(\\leq\\) as "<=" and \\(\\geq\\)
    as ">=".  For instance, a possible answer might be "x <= -9/5".
    Enter logical connectors as "and" or "or", as in
    "-4 < x and x <= 5" or "x < -4 or x >= 5".  In particular,
    the answer-checking algorithm has NOT been programmed
    to understand the expression "-4 < x <= 5"---where no logical
    connecter has been supplied.  (Use "and"!)  You were warned!
    """


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
                else:
                    self.answer = Interval.Lopen(self.l, self.r)
                    self.ineq_answers = set([x > self.l, x <= self.r])
            else: # Q1 == '\\leq'
                if Q2 == '\\lt':
                    self.answer = Interval.Ropen(self.l, self.r)
                    self.ineq_answers = set([x >= self.l, x < self.r])
                else:
                    self.answer = Interval(self.l, self.r)
                    self.ineq_answers = set([x >= self.l, x <= self.r])
            self.format_answer = f'\\( {self.l} {self.Q1} x \\; \\textrm{{and}} \\; x {self.Q2} {self.r} \\)'
        else:
            if Q1 == '\\lt':
                if Q2 == '\\gt':
                    self.answer_left = Interval.open(-oo, self.l)
                    self.answer_right = Interval.open(self.r, oo)
                    self.answer = self.answer_left.union(self.answer_right)
                    self.ineq_answers = set([x < self.l, x > self.r])
                else:
                    self.answer_left = Interval.open(-oo, self.l)
                    self.answer_right = Interval(self.r, oo)
                    self.answer = self.answer_left.union(self.answer_right)
                    self.ineq_answers = set([x < self.l, x >= self.r])
            else: # Q1 == '\\leq'
                if Q2 == '\\gt':
                    self.answer_left = Interval(-oo, self.l)
                    self.answer_right = Interval.open(self.r, oo)
                    self.answer = self.answer_left.union(self.answer_right)
                    self.ineq_answers = set([x <= self.l, x > self.r])
                else:
                    self.answer_left = Interval(-oo, self.l)
                    self.answer_right = Interval(self.r, oo)
                    self.answer = self.answer_left.union(self.answer_right)
                    self.ineq_answers = set([x <= self.l, x >= self.r])
            self.format_answer = f'\\( x {self.Q1} {self.l}  \\; \\textrm{{or}} \\; {self.r}  {CompoundLinearInequality.switchQ(Q2)} x \\)'
        if a < 0:
            given_Q1 = CompoundLinearInequality.switchQ(Q1)
        else:
            given_Q1 = Q1
        if e < 0:
            given_Q2 = CompoundLinearInequality.switchQ(Q2)
        else:
            given_Q2 = Q2
        if self.logical_connector == 'and':
            self.given_latex_display = f"""
            \\[ {l1} {given_Q1} {latex(term1 + c)} {given_Q2} {r1} \\]
            """
        else:
            self.given_latex_display = f"""
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
        cong = CompoundLinearInequality.congruent
        user_answer = list(user_answer)
        answers = list(self.ineq_answers)
        one_way = cong(user_answer[0], answers[0]) and cong(user_answer[1], answers[1])
        the_other = cong(user_answer[0], answers[1]) and cong(user_answer[1], answers[0])
        return one_way or the_other

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
        if 'and' in user_answer:
            user_answer = user_answer.split('and')
        elif 'or' in user_answer:
            user_answer = user_answer.split('or')
        else:
            return "Your answer wasn't intellible"
        if len(user_answer) != 2:
            return "Your answer wasn't intellible"
        user_answer[0] = user_answer[0].replace('^', '**')
        user_answer[0] = parse_expr(user_answer[0], transformations=transformations)
        user_answer[1] = user_answer[1].replace('^', '**')
        user_answer[1] = parse_expr(user_answer[1], transformations=transformations)
        if self.logical_connector == 'and':
            return f'\\( {latex(user_answer[0])} \\; \\textrm{{and}} \\; {latex(user_answer[1])} \\)'
        else:
            return f'\\( {latex(user_answer[0])} \\; \\textrm{{or}} \\; {latex(user_answer[1])} \\)'

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



Question_Class = CompoundLinearInequality
