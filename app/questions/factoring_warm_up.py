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


class FactoringWarmUp(Question):
    """
    The given is an expanded form of

    \\[
        rx^e(ax+b)
    \\]

    The directions are to factor.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-9,9)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random_non_zero_integer(-9,9)
        if 'r' in kwargs:
            self.r = kwargs['r']
        else:
            r = random_non_zero_integer(-9,9)
            while r == 1 or r == -1:
                r = random_non_zero_integer(-9,9)
            self.r = r
        if 'e' in kwargs:
            self.e = kwargs['e']
        else:
            self.e = random.choice([0,1])
        # if 'gcf' in kwargs:
        #     self.gcf = kwargs['gcf']
        # else:
        #     self.gcf = random.choice([False, False, True])
        # if self.gcf:
        #     self.x2 = 0
        # else:
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        a = self.a
        b = self.b
        r = self.r
        e = self.e
        x = self.x
        self.answer = factor(r*x**e*(a*x+b))
        self.format_answer = f'\( {latex(self.answer)}\)'

        self.format_given = f"\\[{latex(expand(self.answer))} \\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Factoring Warm-Up'
    module_name = 'factoring_warm_up'

    prompt_single = """Completely factor.  Also, factor out a negative if the leading coefficient is negative."""
    prompt_multiple = """TBA"""

    further_instruction = """
    """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        print(self.answer, user_answer)
        print(set(self.answer.args), set(user_answer.args))
        constraints = [FactoringWarmUp.sets_evaluate_equal(set(self.answer.args), set(user_answer.args)), type(self.answer) == type(user_answer)]
        print([type(elem) for elem in self.answer.args], [type(elem) for elem in user_answer.args])
        print(type(self.answer), type(user_answer))
        print(constraints)
        return False not in constraints

    @staticmethod
    def sets_evaluate_equal(set1, set2):
        if len(set1) != len(set2):
            return False
        elif len(set1) == 0 and len(set2) == 0:
            return True
        else:
            element = list(set1)[0]
            for elem in set2:
                if element.equals(elem):
                    new_set1 = set1.remove(element)
                    new_set2 = set2.remove(elem)
                    return FactoringWarmUp.sets_evaluate_equal(set1, set2)
            return False


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


Question_Class = FactoringWarmUp
prob_type = 'math_blank'
