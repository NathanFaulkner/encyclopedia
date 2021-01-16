#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, random_non_zero_integer, latex_print



class SyntheticDivisionOfPolynomialsHarder(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        # prob_type = random.choice(['divisor is quadratic', 'dividend has a zero coeff'])
        #prob_type = 'divisor is quadratic'
        # prob_type = 'dividend has a zero coeff'
        b = [] # coefficients for divisor
        a = [] # coefficients for quotient
        r = [] # coefficients of remainder
        x = sy.Symbol('x')

        def at_least_one_zero(a):
            output = False
            for x in a:
                if x == 0:
                    output = True
            return output

        def make_polynomial(coeffs,x):
            expr = coeffs[0]
            for i in range(len(coeffs)-1):
                expr += coeffs[i+1]*x**(i+1)
            return expr

        z = 0
        while z == 0:
            z = random.randint(-9,9)
        divisorexpr = x - z
        d = [] # coeffs of dividend
        deg_d = 4
        # while not(at_least_one_zero(d)):
            # d = []
        for i in range(deg_d):
            if i == deg_d-1:
                d.append(random.randint(1, 7) )
            else:
                d.append(random.randint(-7, 7))
        zero_index = random.randint(0, deg_d - 2)
        d[zero_index] = 0
        pexpr = make_polynomial(d,x)
        q, r = sy.div(pexpr,divisorexpr, domain='ZZ')
        self.answer = q + r/(divisorexpr)


        self.format_answer = f'\\({sy.latex(self.answer)}\\)'

        self.format_given = f"""
        \\[
            \\left({sy.latex(sy.expand(pexpr))}\\right) \\div \\left({sy.latex(sy.expand(divisorexpr))}\\right)
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

    name = "Synthetic Division of Polynomials: Harder Problems"
    module_name = 'synthetic_division_of_polynomials_harder'


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


Question_Class = SyntheticDivisionOfPolynomialsHarder
prob_type = 'math_blank'
