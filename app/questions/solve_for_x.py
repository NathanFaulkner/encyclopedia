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
                            permute_equation)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general
prob_type = 'math_blank'

class SolveForX(Question):
    """
    The given is
    \\[
        a(x+b) + c(x+d) + ex + f = 0,
    \\]
    but permuted with =.
    A fraction, no solution, and all reals are possible.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'num_solutions' in kwargs:
            self.num_solutions = kwargs['num_solutions']
        else:
            self.num_solutions = random.choice([1,1,0,oo])
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
            if self.num_solutions == 1:
                offset = random_non_zero_integer(-9,9)
            else:
                offset = 0
            self.e = -(self.a + self.c) + offset
        if 'f' in kwargs:
            self.f = kwargs['f']
        else:
            if self.num_solutions == 0:
                offset = random_non_zero_integer(-9,9)
            elif self.num_solutions == 1:
                offset = random.randint(-9,9)
            else:
                offset = 0
            self.f = -(self.a*self.b + self.c*self.d) + offset
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        self.problem = self.genproblem()

        self.given = self.problem['given']
        self.answer = self.problem['answer']

        self.given_latex = latex_print(self.given)
        self.given_latex_display = latex_print(self.given, display=True)
        self.format_given = self.given_latex_display
        self.answer_latex = latex_print(self.answer)
        self.answer_latex_display = latex_print(self.answer, display=True)

        if self.num_solutions == 1:
            self.format_answer = self.answer_latex
        else:
            self.format_answer = self.answer

        self.format_given_for_tex = f"""
        {self.prompt_single} \n
        {self.given_latex_display}
        """

    name = 'Solve for x'
    module_name = 'solve_for_x'

    prompt_single = 'Solve for \\(x\\).  (Find the solution set.) '
    prompt_multiple = 'For each of the following, solve for \\(x\\).  (Find the solution set.)'
    further_instruction = """Enter just your numerical answer if you get a solution (not "x=").
Otherwise, enter an English description of the solution set.
    """

    loom_link = "https://www.loom.com/share/331e43b308a64cefbafdb1ac3211c9ac"


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
        terms = [factor(a*(x+b)), factor(c*(x+d)), e*x, f]
        if self.num_solutions in [0,oo]:
            LHS, RHS = permute_equation(terms, as_list=True)
            out['given'] = f'{latex(LHS)} = {latex(RHS)}'
        else:
            out['given'] = permute_equation(terms)
        #print('3rd step: So far its ', expr)
        if self.num_solutions == 1:
            out['answer'] = Rational(-(a*b+c*d+f),(a+c+e))
        elif self.num_solutions == 0:
            out['answer'] = 'No solution'
        else:
            out['answer'] = 'All real numbers'
        return out

    def checkanswer(self, user_answer):
        if self.num_solutions == 1:
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            # print(type(user_answer), type(user_answer) == Float)
            if type(user_answer) == Float:
                return float(self.answer) == user_answer
            else:
                return self.answer == user_answer
        elif self.num_solutions == 0:
            return 'no' in user_answer.lower()
        else:
            return 'all' in user_answer.lower()

    def format_useranswer(self, user_answer, display=False):
        if self.num_solutions == 1:
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            return latex_print(user_answer, display)
        else:
            return user_answer

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            # float(user_answer)
        except:
            raise SyntaxError


Question_Class = SolveForX
