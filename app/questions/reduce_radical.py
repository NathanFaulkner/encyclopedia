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
                            fmt_abs_value,
                            drop_redundant_abs,
                            commute_AbsMul_to_MulAbs,
                            has_rational_power,
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
        q = random.randint(2, 5)
        # q = 4
        if q == 5:
            base = 2
        elif q == 4:
            base = random.randint(2, 3)
        elif q == 3:
            base = random.randint(2, 5)
        else:
            base = random.randint(2, 10)
        b = base
        raised_b = b**q
        a = random.choice([1, 2, 3, 5, 6])
        variables = random.choice([sy.symbols('x y'), sy.symbols('u v'), sy.symbols('x y z')])
        under = raised_b*a
        out_of_radical_part_of_answer = b
        under_radical_part_of_answer = a
        for i, x in enumerate(variables):
            seed = (i*self.seed) % 1
            random.seed(seed)
            d = random.randint(1,5)
            random.seed(1-seed)
            r = random.randint(0,q-1)
            e = d*q + r
            under *= x**e
            # if q % 2 == 0 and d % 2 == 1:
            #     out_of_radical_part_of_answer *= sy.Abs(x)**d
            # else:
            out_of_radical_part_of_answer *= x**d
            under_radical_part_of_answer *= x**r
            # expos[x] = e
        # print('expos', expos)
        # self.answer = sy.simplify(sy.root(under, q))
        # print('self.answer', self.answer)
        given = sy.root(under, q, evaluate=False)
        expr = f'{sy.latex(given)}'
        if q == 2:
            root_symb = '\\sqrt'
        else:
            root_symb = f'\\sqrt[{q}]'
        # print('self.answer:', self.answer)
        if under_radical_part_of_answer == 1:
            fmt_radical = ''
        else:
            fmt_radical = f'{root_symb}{{ {sy.latex(under_radical_part_of_answer)} }}'
        self.answer = f'{str(out_of_radical_part_of_answer)}*root({under_radical_part_of_answer}, {q})'#sy.Mul(out_of_radical_part_of_answer, sy.root(under_radical_part_of_answer, q, evaluate=False), evaluate=False)
        self.format_answer = f'\( {sy.latex(out_of_radical_part_of_answer)} {fmt_radical} \)'
        self.format_given = f"""
        \\[
            {expr}
        \\]"""

        self.prompt_single = f"""Assume all variables represent positive numbers.
        Simplify in the sense of canceling all available powers with the radical
        ("bringing them out of the radical")."""

        self.format_given_for_tex = f"""
        Assume all variables represent positive numbers.
        Simplify in the sense of canceling all available powers with the radical
        (``bringing them out of the radical'').

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

    further_instruction = """
    To enter a radical, you will use the symbol "root".  For example,
    to enter
    \\[
        \sqrt[3]{2x^2}
    \\]
    you will need to enter
    <div style="margin-left: auto; margin-right: auto; text-align:center">
        root(2x^2, 3)
    </div>
    In case you are curious, this is the syntax for a Python (Sympy)
    function 'root', whose first "argument" (input) is what goes
    under the radical sign and whose second argument is the type
    of root&mdash;e.g.: 3 for cube root, 4 for 4th root, etc.
    """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.replace('X', 'x')
        user_answer = user_answer.replace('Y', 'y')
        user_answer = user_answer.replace('Z', 'z')
        user_answer = user_answer.replace('abs', 'Abs')
        user_answer = fmt_abs_value(user_answer)
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        # user_answer = commute_AbsMul_to_MulAbs(user_answer)
        # user_answer = commute_AbsMul_to_MulAbs(user_answer) #second time really commutes AbsPow to PowAbs
        # user_answer = drop_redundant_abs(user_answer)
        # if has_rational_power(user_answer):
        #     return False
        # print('user stuff', user_answer, type(user_answer))
        # for arg in sy.preorder_traversal(user_answer):
        #     print(arg)
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
        #     else:
        #         user_base = user_answer.args[0]
        #         user_expo = user_answer.args[1]
        #         user_answer = sy.Pow(user_base, sy.simplify(user_expo))
        #         # print('standard', user_answer, type(user_answer))
        #         # for arg in sy.preorder_traversal(user_answer):
        #         #     print(arg)
        # print(self.answer)
        # answer = parse_expr(str(self.answer), transformations=transformations, evaluate=False)
        answer = parse_expr(self.answer, transformations=transformations, evaluate=False)
        # print('answer stuff', answer, type(answer))
        # for arg in sy.preorder_traversal(answer):
        #     print(arg)
        return user_answer == answer

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.replace('X', 'x')
        user_answer = user_answer.replace('Y', 'y')
        user_answer = user_answer.replace('Z', 'z')
        user_answer = user_answer.replace('abs', 'Abs')
        user_answer = fmt_abs_value(user_answer)
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        # user_answer = commute_AbsMul_to_MulAbs(user_answer)
        # user_answer = commute_AbsMul_to_MulAbs(user_answer)
        # user_answer = drop_redundant_abs(user_answer)
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
            user_answer = user_answer.replace('X', 'x')
            user_answer = user_answer.replace('Y', 'y')
            user_answer = user_answer.replace('Z', 'z')
            user_answer = user_answer.replace('abs', 'Abs')
            user_answer = fmt_abs_value(user_answer)
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            # user_answer = commute_AbsMul_to_MulAbs(user_answer)
            # user_answer = commute_AbsMul_to_MulAbs(user_answer)
            # user_answer = drop_redundant_abs(user_answer)
            f'\({sy.latex(user_answer)}\)'
        except:
            raise SyntaxError


Question_Class = ReduceRadical
prob_type = 'math_blank'
