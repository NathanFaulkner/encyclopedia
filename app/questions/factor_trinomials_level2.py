#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            sets_evaluate_equal,
                            check_congruence_after_factoring_out_gcf)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class FactorTrinomialsLevel2(Question):
    """
    The given is an expanded form of

    \\[

    \\]

    The directions are to factor.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'p' in kwargs:
            p = kwargs['p']
        else:
            p = random.choice([-5,-3,-2,-1,1,2,3,5])
        if 'q' in kwargs:
            q = kwargs['q']
        else:
            q = random.choice([-5,-3,-2,-1,1,2,3,5])
        if 'm' in kwargs:
            m = kwargs['m']
        else:
            m = random.choice([1, 2, 3, 5])
        if 'n' in kwargs:
            n = kwargs['n']
        else:
            n = random.choice([-5,-3,-2,-1,1,2,3,5])

        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('x')
        x = self.x

        expr = (m*x+p)*(n*x+q)

        self.answer = sy.factor(expr)
        # expr1 = sy.factor(A+B1)*(A+B2)
        # expr2 = (A+B1)*sy.factor(A+B2)
        # expr3 = sy.factor((A+B1)*(A+B2))
        # self.answers = [expr, expr1, expr2, expr3]
        self.format_answer = f'\( {sy.latex(self.answer)}\)'

        self.format_given = f"\\[{sy.latex(sy.expand(self.answer))} \\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Factoring Trinomials, Level 2'
    module_name = 'factor_trinomials_level2'

    prompt_single = """Completely factor."""
    prompt_multiple = """TBA"""

    further_instruction = """
    """

    loom_link = "https://www.loom.com/share/6cbdb245ddf94247985dc59deac4cbf2?sharedAppSource=personal_library"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        if 'x' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        # if not (isinstance(user_answer, sy.core.power.Pow) or isinstance(user_answer, sy.core.mul.Mul)):
        #     return False
        # if isinstance(user_answer, sy.core.mul.Mul):
        #     user_factors = user_answer.args
        #     user_factors = [sy.factor(factor) for factor in user_factors]
        #     check_factors = sets_evaluate_equal(set(self.answer.args), set(user_factors))
        # constraints = [check_factors,
        #                 type(self.answer) == type(user_answer)]
        # print([type(elem) for elem in self.answer.args], [type(elem) for elem in user_answer.args])
        # print(type(self.answer), type(user_answer))
        # print(constraints)
        # print([answer for answer in self.answers])
        # return any([sets_evaluate_equal(set(answer.args), set(user_answer.args)) for answer in self.answers])
        # print(type(user_answer), type(self.answer))
        # return (isinstance(user_answer, sy.core.power.Pow) or isinstance(user_answer, sy.core.mul.Mul)) and sy.expand(user_answer) == sy.expand(self.answer)
        # return user_answer == self.answer
        answer = parse_expr(str(self.answer), transformations=transformations)
        check_congruence_after_factoring_out_gcf(sy.Symbol('x'), user_answer)
        # return answer ==  user_answer
        return check_congruence_after_factoring_out_gcf(answer, user_answer)

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        return f'\\({user_answer}\\)'

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            # type(user_answer) == type(parse_expr('5', transformations=transformations))
            if 'x' in str(user_answer):
                check_congruence_after_factoring_out_gcf(sy.Symbol('x'), user_answer)
        except:
            raise SyntaxError


Question_Class = FactorTrinomialsLevel2
prob_type = 'math_blank'
