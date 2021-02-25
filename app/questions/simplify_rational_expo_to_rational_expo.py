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



class SimplifyRationalExpoToRationalExpo(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        bases = list(range(2,10)) + list(sy.symbols('a b c d x y z u v'))
        base = random.choice(bases)
        b = base
        q1 = random.randint(2, 7)
        q2 = random.randint(2, 7)
        p1 = random_non_zero_integer(-7,7)
        p2 = random_non_zero_integer(-7,7)
        while p2/q2 % 1 == 0:
            p2 = random_non_zero_integer(-7,7)
        expr = f'\\left({base}^{{ {sy.latex(sy.Rational(p1,q1))} }}\\right)^{{ {sy.latex(sy.Rational(p2,q2))} }}'
        self.answer = b**sy.Rational(p1*p2, q1*q2)
        # print('self.answer:', self.answer)
        self.format_answer = f'\( {sy.latex(b)}^{{ {sy.latex(sy.Rational(p1*p2, q1*q2))} }} \)'
        self.format_given = f"""
        \\[
            {expr}
        \\]"""

        self.prompt_single = f"""Simplify&mdash;in the sense of rewriting
        as a single exponential term (that is, a term of the form \\(a^b\\)).
        You can assume all variables represent positive numbers in case
        of ambiguity.
        """

        self.format_given_for_tex = f"""
        Simplify---in the sense of rewriting
        as a single exponential term (that is, a term of the form \\(a^b\\)).
        You can assume all variables represent positive numbers in case
        of ambiguity.

        {self.format_given}
        """

    # def non_zero_integer(a,b):
    #     n = 0
    #     while n == 0:
    #         n = random.randint(a,b)
    #     return n



    name = 'Simplify Rational Exponent Raised to Rational Exponent'
    module_name = 'simplify_rational_expo_to_rational_expo'


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
        if isinstance(user_answer, sy.Pow):
            if user_answer.args[1] == -1:
                print('My fault!')
                print(user_answer.args)
                if isinstance(user_answer.args[0], sy.Pow):
                    user_base = user_answer.args[0].args[0]
                    user_expo = -user_answer.args[0].args[1]
                    user_answer = sy.Pow(user_base, sy.simplify(user_expo), evaluate=False)
                    print('alt', user_answer, type(user_answer))
                    for arg in sy.preorder_traversal(user_answer):
                        print(arg)
            else:
                user_base = user_answer.args[0]
                user_expo = user_answer.args[1]
                user_answer = sy.Pow(user_base, sy.simplify(user_expo), evaluate=False)
                print('standard', user_answer, type(user_answer))
                for arg in sy.preorder_traversal(user_answer):
                    print(arg)
        answer = parse_expr(str(self.answer), transformations=transformations)
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
        if isinstance(user_answer, sy.Pow):
            if user_answer.args[1] == -1:
                # print('My fault!')
                # print(user_answer.args)
                if isinstance(user_answer.args[0], sy.Pow):
                    user_base = user_answer.args[0].args[0]
                    user_expo = -user_answer.args[0].args[1]
                    user_answer = sy.Pow(user_base, sy.simplify(user_expo), evaluate=False)
                    # print('alt', user_answer, type(user_answer))
                    # for arg in sy.preorder_traversal(user_answer):
                    #     print(arg)
            else:
                user_base = user_answer.args[0]
                user_expo = user_answer.args[1]
                user_answer = sy.Pow(user_base, sy.simplify(user_expo), evaluate=False)
                # print('standard', user_answer, type(user_answer))
                # for arg in sy.preorder_traversal(user_answer):
                #     print(arg)
            return f'\\(  {{ {sy.latex(user_base)} }}^{{ {sy.latex(user_expo)} }} \\)'
        return f'\({sy.latex(user_answer)}\)'

    @staticmethod
    def validator(user_answer):
        try:
            # pass
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
            # print('user stuff', user_answer, type(user_answer))
            if isinstance(user_answer, sy.Pow):
                if user_answer.args[1] == -1:
                    # print('My fault!')
                    # print(user_answer.args)
                    if isinstance(user_answer.args[0], sy.Pow):
                        user_base = user_answer.args[0].args[0]
                        user_expo = -user_answer.args[0].args[1]
                        user_answer = sy.Pow(user_base, sy.simplify(user_expo), evaluate=False)
                        # print('alt', user_answer, type(user_answer))
                        # for arg in sy.preorder_traversal(user_answer):
                        #     print(arg)
                else:
                    user_base = user_answer.args[0]
                    user_expo = user_answer.args[1]
                    user_answer = sy.Pow(user_base, sy.simplify(user_expo), evaluate=False)
                    # print('standard', user_answer, type(user_answer))
                    # for arg in sy.preorder_traversal(user_answer):
                    #     print(arg)
            f'\({sy.latex(user_answer)}\)'
        except:
            raise SyntaxError


Question_Class = SimplifyRationalExpoToRationalExpo
prob_type = 'math_blank'
