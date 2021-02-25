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
                            apply_positive_integer_powers,
                            )



class SimplifyRationalExponentJustExpoOfQuotient(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        b1 = random.randint(1, 5)
        b2 = random.randint(1, 5)
        while b1/b2 % 1 == 0:
            b2 = random.randint(1, 5)
        q = random.randint(2, 5)
        p = random_non_zero_integer(-7,7)
        while p/q % 1 == 0:
            p = random_non_zero_integer(-7,7)
        numer = b1**q
        denom = b2**q
        quot = sy.Rational(numer, denom)
        expr = f'\\left({sy.latex(quot)}\\right)^{{ {sy.latex(sy.Rational(p,q))} }}'
        self.answer = sy.Pow(sy.Rational(b1, b2), p)
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



    name = 'Simplify Rational Exponents: Quotient Raised to Exponent'
    module_name = 'simplify_rational_exponent_just_expo_of_quotient'


    prompt_multiple = """TBA"""

    # further_instruction = """
    # Just enter the final expression.  You shouldn't enter
    # "y =" or "f(x) = ".
    # """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        print('user stuff', user_answer, type(user_answer))
        user_answer = apply_positive_integer_powers(user_answer)
        # if isinstance(user_answer, sy.Pow):
        #     if user_answer.args[1] == -1:
        #         print('My fault!')
        #         print(user_answer.args)
        #         if isinstance(user_answer.args[0], sy.Pow):
        #             user_base = user_answer.args[0].args[0]
        #             user_expo = -user_answer.args[0].args[1]
        #             user_answer = sy.Pow(user_base, sy.simplify(user_expo), evaluate=False)
        #             print('alt', user_answer, type(user_answer))
        #             for arg in sy.preorder_traversal(user_answer):
        #                 print(arg)
        #     else:
        #         user_base = user_answer.args[0]
        #         user_expo = user_answer.args[1]
        #         print('type user base', type(user_base))
        #         print('type user_expo', type(user_expo))
        #         if isinstance(user_expo, sy.Integer):
        #             user_answer = sy.Pow(user_base, sy.simplify(user_expo))
        #         else:
        #             user_answer = sy.Pow(user_base, sy.simplify(user_expo), evaluate=False)
        #         print('standard', user_answer, type(user_answer))
        #         for arg in sy.preorder_traversal(user_answer):
        #             print(arg)
        print('pre answer', self.answer)
        answer = parse_expr(str(self.answer), transformations=transformations, evaluate=False)
        answer = apply_positive_integer_powers(answer)
        print('answer stuff', answer, type(answer))
        for arg in sy.preorder_traversal(answer):
            print(arg)
        return user_answer == answer

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        # print('user stuff', user_answer, type(user_answer))
        user_answer = apply_positive_integer_powers(user_answer)
        return f'\({sy.latex(user_answer)}\)'

    @staticmethod
    def validator(user_answer):
        try:
            # pass
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
            # print('user stuff', user_answer, type(user_answer))
            user_answer = apply_positive_integer_powers(user_answer)
            f'\({sy.latex(user_answer)}\)'
        except:
            raise SyntaxError

    # def checkanswer(self, user_answer):
    #     user_answer = user_answer.lower()
    #     user_answer = user_answer.replace('^', '**')
    #     # user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
    #     # print('userans', user_answer, type(user_answer))
    #     # if isinstance(user_answer, sy.Pow):
    #     #     print('user_power', user_answer.args[1], type(user_answer.args[1]))
    #     #     initial_power
    #     answer = parse_expr(str(self.answer), transformations=transformations)
    #     # print('answer', answer, type(answer))
    #     user_quotient = Quotient(user_answer)
    #     user_numer, user_denom = [user_quotient.numer.normal_form, user_quotient.denom.normal_form]
    #     user_answer = f'{user_numer}/{user_denom}'
    #     user_answer = parse_expr(user_answer, transformations=transformations)
    #     return user_answer == answer
    #
    # @staticmethod
    # def format_useranswer(user_answer, display=False):
    #     # user_answer = user_answer.lower()
    #     # user_answer = user_answer.replace('^', '**')
    #     # user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
    #     user_answer = user_answer.lower()
    #     user_answer = user_answer.replace('^', '**')
    #     # user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
    #     # print('userans', user_answer, type(user_answer))
    #     # if isinstance(user_answer, sy.Pow):
    #     #     print('user_power', user_answer.args[1], type(user_answer.args[1]))
    #     #     initial_power
    #     # answer = parse_expr(str(self.answer), transformations=transformations, evaluate=False)
    #     # print('answer', answer, type(answer))
    #     user_quotient = Quotient(user_answer)
    #     user_numer, user_denom = [user_quotient.numer.normal_form, user_quotient.denom.normal_form]
    #     # print(user_numer, user_denom)
    #     fmt = user_quotient.fmt_for_tex
    #     # print(repr(user_answer))
    #     # if SimplifyIntegerExponent.non_positive_power(user_answer):
    #     #     return unchanged
    #     return f'\({fmt}\)'
    #
    # @staticmethod
    # def validator(user_answer):
    #     try:
    #         # pass
    #         user_answer = user_answer.lower()
    #         user_answer = user_answer.replace('^', '**')
    #         user_quotient = Quotient(user_answer)
    #         user_numer, user_denom = [user_quotient.numer.normal_form, user_quotient.denom.normal_form]
    #         fmt = user_quotient.fmt_for_tex
    #         user_answer = f'{user_numer}/{user_denom}'
    #         user_answer = parse_expr(user_answer, transformations=transformations)
    #     except:
    #         raise SyntaxError


Question_Class = SimplifyRationalExponentJustExpoOfQuotient
prob_type = 'math_blank'
