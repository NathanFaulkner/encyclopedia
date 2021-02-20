#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            alt_congruence_of_quotient,
                            congruence_of_quotient,
                            Monomial,
                            Quotient,
                            )



class SimplifyIntegerExponent(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        b = random.randint(2, 5)
        q = random.randint(2, 5)
        p = random_non_zero_integer(-7,7)
        while p/q % 1 == 0:
            p = random_non_zero_integer(-7,7)
        given_base = b**q
        self.b, self.p, self.q = [b, p, q]
        expr = f'{given_base}^{{ {sy.latex(sy.Rational(p,q))} }}'
        self.answer = sy.Pow(b, p)
        # print('self.answer:', self.answer)
        self.format_answer = f'\( {sy.latex(self.answer)} \)'
        self.format_given = f"""
        \\[
            {expr}
        \\]"""

        self.prompt_single = f"""Simplify.  In particular, rewrite the term without
        the use of any negative exponents."""

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    # def non_zero_integer(a,b):
    #     n = 0
    #     while n == 0:
    #         n = random.randint(a,b)
    #     return n



    name = 'Simplify Rational Exponents: Just an Exponent'
    module_name = 'simplify_rational_exponent_just_expo'


    prompt_multiple = """TBA"""

    # further_instruction = """
    # Just enter the final expression.  You shouldn't enter
    # "y =" or "f(x) = ".
    # """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        # user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        # print('userans', user_answer, type(user_answer))
        # if isinstance(user_answer, sy.Pow):
        #     print('user_power', user_answer.args[1], type(user_answer.args[1]))
        #     initial_power
        answer = parse_expr(str(self.answer), transformations=transformations)
        # print('answer', answer, type(answer))
        user_quotient = Quotient(user_answer)
        user_numer, user_denom = [user_quotient.numer.normal_form, user_quotient.denom.normal_form]
        user_answer = f'{user_numer}/{user_denom}'
        user_answer = parse_expr(user_answer, transformations=transformations)
        return user_answer == answer

    @staticmethod
    def format_useranswer(user_answer, display=False):
        # user_answer = user_answer.lower()
        # user_answer = user_answer.replace('^', '**')
        # user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        # user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        # print('userans', user_answer, type(user_answer))
        # if isinstance(user_answer, sy.Pow):
        #     print('user_power', user_answer.args[1], type(user_answer.args[1]))
        #     initial_power
        # answer = parse_expr(str(self.answer), transformations=transformations, evaluate=False)
        # print('answer', answer, type(answer))
        user_quotient = Quotient(user_answer)
        user_numer, user_denom = [user_quotient.numer.normal_form, user_quotient.denom.normal_form]
        # print(user_numer, user_denom)
        fmt = user_quotient.fmt_for_tex
        # print(repr(user_answer))
        # if SimplifyIntegerExponent.non_positive_power(user_answer):
        #     return unchanged
        return f'\({fmt}\)'

    @staticmethod
    def validator(user_answer):
        try:
            # pass
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_quotient = Quotient(user_answer)
            user_numer, user_denom = [user_quotient.numer.normal_form, user_quotient.denom.normal_form]
            fmt = user_quotient.fmt_for_tex
            user_answer = f'{user_numer}/{user_denom}'
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError


Question_Class = SimplifyIntegerExponent
prob_type = 'math_blank'
