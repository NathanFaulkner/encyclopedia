#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *

from app.questions import Question, latex_print, random_non_zero_integer, sgn


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class VertexFormToStandardForm(Question):
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
        if 'a' in kwargs:
            self.a = kwargs['p']
        else:
            a=0
            while a == 0:
                a = int(random.triangular(-9,9))
        self.a = a
        symb_a = '{}'.format(a)
        if a == 1:
            symb_a = ''
        elif a == -1:
            symb_a = '-'
        if 'h' in kwargs:
            self.h = kwargs['h']
        else:
            self.h = random.randint(-5,5)
        if 'k' in kwargs:
            self.k = kwargs['k']
        else:
            self.k = random_non_zero_integer(-5,5)

        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')


        a = self.a
        h = self.h
        k = self.k
        x = self.x
        self.answer = expand(a*(x - h)**2 + k)
        self.format_answer = f'\( {latex(self.answer)}\)'

        self.format_given = f"\\[f(x) = {symb_a}\\left({x-h}\\right)^2{sgn(k)}{abs(k)}\\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Vertex Form to Standard Form'
    module_name = 'vertex_form_to_standard_form'

    prompt_single = """Rewrite the following quadratic, putting it into standard
    form (by multiplying everything out and combining like terms)."""
    prompt_multiple = """Rewrite each quadratic, putting it into standard
    form (by multiplying everything out and combining like terms)."""

    further_instruction = """
    Just enter the final expression.  You shouldn't enter
    "y =" or "f(x) = ".
    """


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


Question_Class = VertexFormToStandardForm
prob_type = 'math_blank'
