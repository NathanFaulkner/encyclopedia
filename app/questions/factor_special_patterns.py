#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            sets_evaluate_equal)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class FactorSpecialPatterns(Question):
    """
    The given is an expanded form of

    \\[
        (x - x1)(x - x2)
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
            a = random.randint(1,9)
        b = random.randint(1,9)
        sign1 = random.choice([-1,1])
        sign2 = random.choice([-1,1])
        x, t, r, y = sy.symbols('x t r y')
        vars = random.choice([(x,1),(x,y),(r,t),(1,y)])

        A = a*vars[0]
        B1 = sign1*b*vars[1]
        B2 = sign2*b*vars[1]

        expr = (A+B1)*(A+B2)

        self.answer = expr
        expr1 = sy.factor(A+B1)*(A+B2)
        expr2 = (A+B1)*sy.factor(A+B2)
        expr3 = sy.factor((A+B1)*(A+B2))
        self.answers = [expr, expr1, expr2, expr3]
        self.format_answer = f'\( {sy.latex(self.answer)}\)'

        self.format_given = f"\\[{sy.latex(sy.expand(self.answer))} \\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Factoring Special Patterns'
    module_name = 'factor_special_patterns'

    prompt_single = """Factor."""
    prompt_multiple = """TBA"""

    further_instruction = """
    """

    loom_link = "https://www.loom.com/share/0dd641248d0742c4b7908a3164c2bb91?sharedAppSource=personal_library"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        # check_factors = any([sets_evaluate_equal(set(answer.args), set(user_answer.args)) for answer in self.answers])
        # constraints = [check_factors,
        #                 type(self.answer) == type(user_answer)]
        # print([type(elem) for elem in self.answer.args], [type(elem) for elem in user_answer.args])
        # print(type(self.answer), type(user_answer))
        # print(constraints)
        # print([answer for answer in self.answers])
        # return any([sets_evaluate_equal(set(answer.args), set(user_answer.args)) for answer in self.answers])
        # print(type(user_answer), type(self.answer))
        return (isinstance(user_answer, sy.core.power.Pow) or isinstance(user_answer, sy.core.mul.Mul)) and sy.expand(user_answer) == sy.expand(self.answer)

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


Question_Class = FactorSpecialPatterns
prob_type = 'math_blank'
