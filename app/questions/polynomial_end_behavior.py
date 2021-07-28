#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation,
                            has_numbers)

prob_type = 'math_blank'

class PolynomialEndBehavior(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        a = [] # coefficients
        degree = random.randint(3,6)
        x = sy.Symbol('x')

        def make_polynomial(coeffs,x):
            expr = coeffs[0]
            for i in range(len(coeffs)-1):
                expr += coeffs[i+1]*x**(i+1)
            return expr

        for i in range(degree+1):
            if i == degree+1:
                temp = 0
                while temp == 0:
                    temp = random.randint(-7, 7)
                a.append(temp)
            else:
                a.append(random.randint(-7, 7))

        expr = make_polynomial(a,x)
        self.format_given = ''
        self.answer = [sy.limit(expr, x, -sy.oo), sy.limit(expr, x, sy.oo)]
        self.format_answer = f'\\({sy.latex(self.answer[0])}, {sy.latex(self.answer[1])}\\)'

        self.prompt_single = f"""Identify the end behavior of the polynomial,
            \\[ f(x) = {sy.latex(sy.expand(expr))}\\]
            by
            indicating how to fill in the blanks:
                <ul>
                  <li>
                    As \\(x \\rightarrow -\\infty\\), \\(f(x) \\rightarrow\\)
                    <u><span style="color:white">mmmmmmmmmmmmm</span></u>
                  </li>
                  <li>
                    As \\(x \\rightarrow \\infty\\), \\(f(x) \\rightarrow\\)
                    <u><span style="color:white">mmmmmmmmmmmmm</span></u>
                  </li>
                </ul>
            """

        self.format_given_for_tex = f"""
        Identify the end behavior of the polynomial,
        \\[ f(x) = {sy.latex(sy.expand(expr))}\\]
        by
        indicating how to fill in the blanks:
        \\begin{{itemize}}
            \\item As \\(x \\rightarrow -\\infty\\), \\(f(x) \\rightarrow$ \\ul{{\\quad\\quad\\quad}}
            \\item As \\(x \\rightarrow \\infty\\), \\(f(x) \\rightarrow$ \\ul{{\\quad\\quad\\quad}}
        \\end{{itemize}}

        """
        self.format_fragment_for_tex = f'\\[ f(x) = {sy.latex(sy.expand(expr))}\\]'

    name = 'End Behavior of Polynomial'
    module_name = 'polynomial_end_behavior'


    prompt_multiple = 'TBA'
    further_instruction = """
    For each blank, the possible answers are \\(\\infty\\) or \\(-\\infty\\).
    Enter your answers as either 'oo' (little-oh, little-oh) or '-oo'.
    Enter the answer for the first blank, and then the answer for the
    second blank, separated by commas.
    """

    prob_type = prob_type

    loom_link = "https://www.loom.com/share/430998fe42704fdbba0a9cc1cd1c1ab8"


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('x', ' ')
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = user_answer.replace('or', ',')
        user_answers = user_answer.split(',')
        i = 0
        while i < len(user_answers):
            user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
            i += 1
        return self.answer == user_answers

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('x', ' ')
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = user_answer.replace('or', ',')
        user_answers = user_answer.split(',')
        i = 0
        while i < len(user_answers):
            user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
            i += 1
        format_answer = ''
        for ans in user_answers:
            format_answer += sy.latex(ans) + ' ,'
        format_answer = format_answer[:-2]
        return '\(' + format_answer + '\)'


    @staticmethod
    def validator(user_answer):
        try:
            # pass
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('or', ',')
            user_answers = user_answer.split(',')
            i = 0
            while i < len(user_answers):
                user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
                i += 1
            format_answer = ''
            for ans in user_answers:
                format_answer += sy.latex(ans) + ' ,'
            format_answer = format_answer[:-2]
        except:
            raise SyntaxError



Question_Class = PolynomialEndBehavior
