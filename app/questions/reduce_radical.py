#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            get_integer_divisors,
                            )



class ReduceRadical(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        base = random.randint(2, 10)
        b = base
        q = random.randint(2, 5)
        raised_b = b**q
        a = random.randint(2,9)
        variables = random.choice([sy.symbols('x y', real=True), [sy.symbols('x', real=True)], sy.symbols('x y z', real=True)])
        under = raised_b*a
        for x in variables:
            e = random.randint(0,5)*q + random.randint(0,q-1)
            under *= x**e
        given = sy.root(under, q, evaluate=False)
        expr = f'{sy.latex(given)}'
        self.answer = sy.simplify(given)
        # print('self.answer:', self.answer)
        self.format_answer = f'\( {sy.latex(self.answer)} \)'
        self.format_given = f"""
        \\[
            {expr}
        \\]"""

        self.prompt_single = f"""Simplify."""

        self.format_given_for_tex = f"""
        Simplify.

        {self.format_given}
        """

    # def non_zero_integer(a,b):
    #     n = 0
    #     while n == 0:
    #         n = random.randint(a,b)
    #     return n



    name = 'Reduce Radical'
    module_name = 'reduce_radical'


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
                # print('My fault!')
                # print(user_answer.args)
                if isinstance(user_answer.args[0], sy.Pow):
                    user_base = user_answer.args[0].args[0]
                    user_expo = -user_answer.args[0].args[1]
                    user_answer = sy.Pow(user_base, sy.simplify(user_expo))
                    # print('alt', user_answer, type(user_answer))
                    # for arg in sy.preorder_traversal(user_answer):
                    #     print(arg)
            else:
                user_base = user_answer.args[0]
                user_expo = user_answer.args[1]
                user_answer = sy.Pow(user_base, sy.simplify(user_expo))
                # print('standard', user_answer, type(user_answer))
                # for arg in sy.preorder_traversal(user_answer):
                #     print(arg)
        answer = parse_expr(str(self.answer), transformations=transformations, evaluate=False)
        print('answer stuff', answer, type(answer))
        # for arg in sy.preorder_traversal(answer):
        #     print(arg)
        return user_answer == answer

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        # print('user stuff', user_answer, type(user_answer))
        # if isinstance(user_answer, sy.Pow):
        #     if user_answer.args[1] == -1:
        #         # print('My fault!')
        #         # print(user_answer.args)
        #         if isinstance(user_answer.args[0], sy.Pow):
        #             user_base = user_answer.args[0].args[0]
        #             user_expo = -user_answer.args[0].args[1]
        #             user_answer = sy.Pow(user_base, sy.simplify(user_expo))
        #             # print('alt', user_answer, type(user_answer))
        #             # for arg in sy.preorder_traversal(user_answer):
        #             #     print(arg)
        #         else:
        #
        #     else:
        #         user_base = user_answer.args[0]
        #         user_expo = user_answer.args[1]
        #         user_answer = sy.Pow(user_base, sy.simplify(user_expo))
        #         # print('standard', user_answer, type(user_answer))
        #         # for arg in sy.preorder_traversal(user_answer):
        #         #     print(arg)
        #     return f'\\(  {sy.latex(user_base)}^{{ {sy.latex(user_expo)} }} \\)'
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
                        user_answer = sy.Pow(user_base, sy.simplify(user_expo))
                        # print('alt', user_answer, type(user_answer))
                        # for arg in sy.preorder_traversal(user_answer):
                        #     print(arg)
                else:
                    user_base = user_answer.args[0]
                    user_expo = user_answer.args[1]
                    user_answer = sy.Pow(user_base, sy.simplify(user_expo))
                    # print('standard', user_answer, type(user_answer))
                    # for arg in sy.preorder_traversal(user_answer):
                    #     print(arg)
            f'\({sy.latex(user_answer)}\)'
        except:
            raise SyntaxError


Question_Class = ReduceRadical
prob_type = 'math_blank'
