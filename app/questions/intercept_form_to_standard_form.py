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


class InterceptFormToStandardForm(Question):
    """
    The given is an expanded form of

    \\[
        a(x - x1)(x - x2)
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
        if 'x1' in kwargs:
            self.x1 = kwargs['x1']
        else:
            self.x1 = random_non_zero_integer(-9,9)
        if 'x2' in kwargs:
            self.x2 = kwargs['x2']
        else:
            self.x2 = random_non_zero_integer(-9,9)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        a = self.a
        x1 = self.x1
        x2 = self.x2
        x = self.x
        self.answer = expand(a*(x - x1)*(x - x2))
        self.format_answer = f'\( {latex(self.answer)}\)'

        self.format_given = f"\\[f(x) = {symb_a}\\left({latex(x-x1)}\\right)\left({latex(x-x2)}\\right)\\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Intercept Form to Standard Form'
    module_name = 'intercept_form_to_standard_form'

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
        return f'\\({user_answer}\\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError


Question_Class = InterceptFormToStandardForm
prob_type = 'math_blank'
