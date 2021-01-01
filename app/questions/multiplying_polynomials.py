#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, random_non_zero_integer, latex_print



class MultiplyingPolynomials(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        a = []
        len_a = random.choice([2, 3])
        b = []
        len_b = random.choice([3, 4])
        temp = 0
        for i in range(len_a):
            if i == 0:
                while temp == 0:
                    temp =  random.randint(-7, 7)
                a.append(temp)
            elif i == len_a -1:
                a.append(random.randint(1, 7) )
            else:
                temp = 0
                temp =  random.randint(-7, 7)
                a.append(temp)


        for i in range(len_b):
            temp =  random.randint(-7, 7)
            b.append(temp)

        while all([item == 0 for item in b]):
            for i in range(len_b):
                temp =  random.randint(-7, 7)
                b.append(temp)

        x = sy.Symbol('x')

        fexpr = a[0]
        gexpr = b[0]

        for i in range(len_a-1):
            fexpr += a[i+1]*x**(i+1)
        for i in range(len_b-1):
            gexpr += b[i+1]*x**(i+1)
        self.answer = sy.expand(fexpr*gexpr)
        self.format_answer = f'\( {sy.latex(self.answer)}\)'

        self.format_given = f"""
        \\[
            \\left({sy.latex(sy.expand(fexpr))}\\right) \\left({sy.latex(sy.expand(gexpr))}\\right)
        \\]"""

        self.prompt_single = f"""Perform the indicated operation (i.e., multiply it all out)."""

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Multiply Polynomials'
    module_name = 'multiplying_polynomials'


    prompt_multiple = """TBA"""

    # further_instruction = """
    # Just enter the final expression.  You shouldn't enter
    # "y =" or "f(x) = ".
    # """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return self.answer == user_answer

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return f'\({sy.latex(user_answer)}\)'

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError


Question_Class = MultiplyingPolynomials
prob_type = 'math_blank'
