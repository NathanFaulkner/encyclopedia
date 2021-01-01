#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, latex_print, random_non_zero_integer, sgn



class AddingOrSubtractingPolynomials(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        a = []
        b = []
        n = random.randint(3, 7) #number of terms
        # n=3
        for i in range(n):
            a.append(random.randint(-7, 7))
            b.append(random.randint(-7, 7))

        x = sy.Symbol('x')

        fexpr = a[0]
        gexpr = b[0]

        for i in range(n-1):
            fexpr += a[i+1]*x**(i+1)
            gexpr += b[i+1]*x**(i+1)

        sign = random.choice(['+', '-'])
        factor = -1 if sign == '-' else 1
        verb = 'subtract' if sign == '-' else 'add'
        self.answer = sy.expand(fexpr + factor*gexpr)
        self.format_answer = f'\( {sy.latex(self.answer)}\)'

        self.format_given = f"""
        \\[
            \\left({sy.latex(sy.expand(fexpr))}\\right) {sign} \\left({sy.latex(sy.expand(gexpr))}\\right)
        \\]"""

        self.prompt_single = f"""Perform the indicated operation (i.e., {verb})."""

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Add or Subtract Polynomials'
    module_name = 'adding_or_subtracting_polynomials'


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
        return latex_print(user_answer, display)

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError


Question_Class = AddingOrSubtractingPolynomials
prob_type = 'math_blank'
