#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, random_non_zero_integer, latex_print



class SyntheticDivisionOfPolynomials(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        a = []
        len_a = random.randint(3, 5)
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

        # a = random.randint(1,9)
        b = 0
        while b == 0:
            b = random.randint(-7,7)

        pexpr = qexpr*(x-b) + r
        x = sy.Symbol('x')

        self.answer = qexpr + r/(x-b)
        self.format_answer = f'\\({sy.latex(self.answer)}\\)'

        self.format_given = f"""
        \\[
            \\left({sy.latex(sy.expand(pexpr))}\\right) \\div \\left({sy.latex(x-b)}\\right)
        \\]"""

        self.prompt_single = f"""
            Use <span style="color: red">synthetic division</span> to determine quotient and remainder
            resulting from each of the following.
            Put your answer in the form
              \\[
                q(x) + \\frac{{r}}{{d(x)}}
              \\]
            where \\(q(x)\\) is the quotient, \\(d(x)\\) is the divisor, and \\(r\\) is the remainder.
        """

        self.format_given_for_tex = f"""
        Use {{\color{{red}}synthetic division}} to
        determine quotient and remainder
        resulting from each of the following.
        Put your answer in the form
          \\[
            q(x) + \\frac{{r}}{{d(x)}}
          \\]
        where \\(q(x)\\) is the quotient, \\(d(x)\\) is the
        divisor, and \\(r\\) is the remainder.

        {self.format_given}
        """

    name = "Synthetic Division of Polynomials"
    module_name = 'synthetic_division_of_polynomials'

    loom_link = "https://www.loom.com/share/93ddbd75014048a686fa46498a436c1b"

    prompt_multiple = """TBA"""

    # further_instruction = """
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


Question_Class = SyntheticDivisionOfPolynomials
prob_type = 'math_blank'
