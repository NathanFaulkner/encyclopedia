#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            sgn, leading_coeff, signed_coeff,
                            fmt_slope_style,
                            find_numbers,
                            has_numbers)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class GenericMaxMin(Question):
    """
    The given is an expanded form of

    \\[
        a(x - h)^2 + k
    \\]

    The directions are to find the max or min.  Answer example:
    "Max at x= h  of y = k"
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['p']
        else:
            a=0
            while a == 0:
                a = int(random.triangular(-19,19))
            add_on = random.choice([Rational(1, 2), 0])
            a = a + add_on
        self.a = a
        symb_a = '{}'.format(a)
        if a == 1:
            symb_a = ''
        elif a == -1:
            symb_a = '-'
        if 'h' in kwargs:
            self.h = kwargs['h']
        else:
            self.h = random.randint(-5,5)
        # self.h = 0
        if 'k' in kwargs:
            self.k = kwargs['k']
        else:
            k = random_non_zero_integer(-10,10)
            add_on = random.choice([Rational(1, 2), 0])
            k = k + add_on
            self.k = k
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')


        a = self.a
        h = self.h
        k = self.k
        x = self.x
        self.given = expand(a*(x - h)**2 + k)
        max_or_min = 'Min' if a > 0 else 'Max'
        self.format_answer = f"""
        {max_or_min} at x = {self.h} of y = {self.k}
        """

        expr = self.given
        # print(latex(self.given))
        b = expr.coeff(x, 1)
        format_middle_term = ''
        if b != 0:
            format_middle_term = signed_coeff(b) + 'x'
        c = expr.coeff(x, 0)
        format_last_term = ''
        if c!= 0:
            format_last_term = latex(abs(c))
        self.format_given = f"""
        \\[
            f(x) = {leading_coeff(a)}x^2 {format_middle_term} {sgn(c)} {format_last_term}
        \\]
        """

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Generic Max/Min Problem'
    module_name = 'generic_max_min'

    prompt_single = """Identify whether the quadratic has a max value or a
    min value, where (on the \(x\)-axis) it attains it, and what that
    \(y\)-value is."""
    prompt_multiple = """TBA"""

    further_instruction = """
    Your answer should be of the following style (or close to it), with items highlighted in
    red replaced by your answer:

    <blockquote>
        <span style="color: red">Max</span> at x = <span style="color: red">12.5</span>
        of y = <span style="color: red">-3.5</span>
    </blockquote>
    """

    loom_link = "https://www.loom.com/share/ac60fe1ba6094af1b630def7bfc15083?sharedAppSource=personal_library"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        if self.a > 0:
            if 'min' not in user_answer:
                return False
        else:
            if 'max' not in user_answer:
                return False
        if 'at x' not in user_answer or 'of y' not in user_answer:
            return False
        i = user_answer.find('at x')
        user_x = user_answer[i+4:]
        i = user_x.find('=')
        user_x = user_x[i+1:]
        user_x = user_x.strip()
        i = user_x.find(' ')
        if i != -1:
            user_x = user_x[:i]
        user_x = user_x.replace('^', '**')
        user_x = parse_expr(user_x, transformations=transformations)
        i = user_answer.find('of y')
        user_y = user_answer[i+4:]
        i = user_y.find('=')
        user_y = user_y[i+1:]
        user_y = user_y.strip()
        i = user_y.find(' ')
        if i != -1:
            user_y = user_y[:i]
        user_y = user_y.replace('^', '**')
        user_y = parse_expr(user_y, transformations=transformations)
        return user_x == float(self.h) and user_y == float(self.k)

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.split(' ')
        for i in range(len(user_answer)):
            word = user_answer[i]
            try:
                if has_numbers(word):
                    word = word.replace('^', '**')
                    word = parse_expr(word, transformations=transformations)
                    user_answer[i] = latex(word)
            except:
                pass
        formatted = ''
        for word in user_answer:
            formatted += str(word) + ' '
        return formatted

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            if 'max' not in user_answer and 'min' not in user_answer:
                raise SyntaxError
            if 'at x' not in user_answer or 'of y' not in user_answer:
                raise SyntaxError
            i = user_answer.find('at x')
            user_x = user_answer[i+4:]
            i = user_x.find('=')
            user_x = user_x[i+1:]
            user_x = user_x.strip()
            i = user_x.find(' ')
            if i != -1:
                user_x = user_x[:i]
            user_x = user_x.replace('^', '**')
            user_x = parse_expr(user_x, transformations=transformations)
            i = user_answer.find('of y')
            user_y = user_answer[i+4:]
            i = user_y.find('=')
            user_y = user_y[i+1:]
            user_y = user_y.strip()
            i = user_y.find(' ')
            if i != -1:
                user_y = user_y[:i]
            user_y = user_y.replace('^', '**')
            user_y = parse_expr(user_y, transformations=transformations)
        except:
            raise SyntaxError


Question_Class = GenericMaxMin
prob_type = 'math_blank'
