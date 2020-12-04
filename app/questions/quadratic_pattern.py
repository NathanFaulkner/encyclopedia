#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *

from app.questions import Question, latex_print, random_non_zero_integer


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class QuadraticPattern(Question):
    """
    The given is an expanded form of

    \\[
    (x^r+p)(x^r+q)
    \\]

    The directions ``completely factor'' mean that the user should also factor
    $x^r + p$ or $x^r + q$ if r is even and p or q (respectively) is a
    perfect square.  While sympy will support factorization of $x^r + a^r$
    for $r$ odd, the intent is not to require this step for the student at this
    stage.  But if that further functionality is desired, it can
    be added in very easily as an option.
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
            self.p = random_non_zero_integer(-7,7)
        self.p = -1
        if 'q' in kwargs:
            self.q = kwargs['q']
        else:
            self.q = random_non_zero_integer(-5,5)
        self.q = -3
        if 'r' in kwargs:
            self.r = kwargs['r']
        else:
            self.r = random.randint(2,6)
        self.r=4
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        x = self.x
        r = self.r
        p = self.p
        q = self.q
        # expr = 1
        # if r % 2 == 0:
        #     if sqrt(-p) % 1 == 0 and p < 0:
        #         expr *= (x**int(r/2)+sqrt(-p))*(x**int(r/2)-sqrt(-p))
        #         #print('1st step: So far its ', expr)
        #     else:
        #         expr *= (x**r+p)
        #     if sqrt(-q) % 1 == 0 and q < 0:
        #         expr *= (x**int(r/2)+sqrt(-q))*(x**int(r/2)-sqrt(-q))
        #     else:
        #         expr *= (x**r+q)
        #         #print('2nd step: So far its ', expr)
        # else:
        #     expr = (x**r+p)*(x**r+q)

        # self.given = self.problem['given']
        # self.answer = self.problem['answer']
        expr = (x**r + p)*(x**r+q)
        self.answer = factor(expr)
        self.format_answer = '\\(' + latex(self.answer) + '\\)'
        self.format_given = '\\[' + latex(expand(expr)) + '\\]'

        # self.given_latex = latex_print(self.given)
        # self.given_latex_display = latex_print(self.given, display=True)
        # self.answer_latex = latex_print(self.answer)
        # self.format_answer = self.answer_latex
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Quadratic Pattern'
    module_name = 'quadratic_pattern'

    prompt_single = 'Completely factor the following: '
    prompt_multiple = 'Completely factor each of the following.'


    prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        answer = parse_expr(str(self.answer), transformations=transformations)
        return answer == user_answer

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


Question_Class = QuadraticPattern
prob_type = 'math_blank'
