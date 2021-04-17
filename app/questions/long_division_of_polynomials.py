#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            latex_print,
                            simplify_for_long_division,
                            )



class LongDivisionOfPolynomials(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        a = []
        len_a = 3
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

        x = sy.Symbol('x')

        qexpr = a[0]
        for i in range(len_a-1):
            qexpr += a[i+1]*x**(i+1)

        r = random.randint(-10,10)

        a = random.randint(1,9)
        b = 0
        while b == 0:
            b = random.randint(-7,7)

        pexpr = qexpr*(a*x+b) + r
        x = sy.Symbol('x')

        self.answer = qexpr + r/(a*x+b)
        self.format_answer = f'\\({sy.latex(self.answer)}\\)'

        self.format_given = f"""
        \\[
            \\left({sy.latex(sy.expand(pexpr))}\\right) \\div \\left({sy.latex(a*x+b)}\\right)
        \\]"""

        self.prompt_single = f"""
            Determine quotient and remainder resulting from the following.
            Put your answer in the form
              \\[
                q(x) + \\frac{{r}}{{d(x)}}
              \\]
            where \\(q(x)\\) is the quotient, \\(d(x)\\) is the divisor, and \\(r\\) is the remainder.
        """

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = "Long Division of Polynomials"
    module_name = 'long_division_of_polynomials'

    loom_link = "https://www.loom.com/share/98a286b3f95b4c239e79850bda55f937"


    prompt_multiple = """TBA"""

    # further_instruction = """
    # """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        answer = simplify_for_long_division(self.answer)
        user_answer = simplify_for_long_division(user_answer)
        return answer == user_answer
        # return self.answer == user_answer

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        user_answer = simplify_for_long_division(user_answer)
        return f'\({sy.latex(user_answer)}\)'

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            user_answer = simplify_for_long_division(user_answer)
        except:
            raise SyntaxError


Question_Class = LongDivisionOfPolynomials
prob_type = 'math_blank'
