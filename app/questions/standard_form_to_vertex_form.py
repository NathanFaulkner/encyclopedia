#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            signed_coeff, leading_coeff, sgn,
                            fmt_slope_style)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class StandardFormToVertexForm(Question):
    """
    The given is an expanded form of

    \\[
        a(x - h)^2 + k
    \\]

    The directions are to completely multiply it out (put in standard form).
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
        self.a = Rational(self.p, self.q)
        if 'x0' in kwargs:
            self.x0 = kwargs['x0']
        else:
            self.x0 = random_non_zero_integer(-5,5)
        if 'y0' in kwargs:
            self.y0 = kwargs['y0']
        else:
            if self.a == 2 or self.a == Rational(1,2):
                self.y0 = random.randint(-5, 2)
            elif self.a == -2 or self.a == Rational(-1,2):
                self.y0 = random.randint(-2, 5)
            else:
                self.y0 = random.randint(-5,5)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')


        a = self.a
        h = self.x0
        k = self.y0
        x = self.x
        self.answer = factor(a*(x - h)**2) + k
        term = factor(self.a*(self.x - self.x0)**2)
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
        if self.a == 1:
            fmt_a = ''
        elif self.a == -1:
            fmt_a = '-'
        else:
            fmt_a = latex(self.a)
        try:
            self.format_answer = f"""
            \\(
             {fmt_a} {latex((self.x - self.x0)**2)} {sign} {fmt_y0}
            \\)
            """
        except IndexError:
            self.format_answer = f"""
            \\(
             {latex(term)} {sign} {fmt_y0}
            \\)
            """

        expr = expand(self.answer)
        b = expr.coeff(x, 1)
        c = expr.coeff(x, 0)
        self.format_given = f"""
        \\[
            f(x) = {leading_coeff(a)}x^2 {signed_coeff(b)}x {sgn(c)} {latex(abs(c))}
        \\]
        """

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Standard Form to Vertex Form'
    module_name = 'standard_form_to_vertex_form'

    prompt_single = """Rewrite the following quadratic, putting it into vertex form."""
    prompt_multiple = """Rewrite each quadratic, putting it into vertex
    form."""

    further_instruction = """
    Just enter the final expression.  You shouldn't enter
    "y =" or "f(x) =".
    """


    loom_link = "https://www.loom.com/share/11e5d7f20e994650ac8175ac0a2a1b8b?sharedAppSource=personal_library"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return self.answer == user_answer

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return latex_print(user_answer, display)

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError


Question_Class = StandardFormToVertexForm
prob_type = 'math_blank'
