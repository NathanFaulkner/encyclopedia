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


class Good():
    def __init__(self, plural_name, plausible_optimums):
        self.plural_name = plural_name
        self.plausible_optimums = plausible_optimums

cans_of_soup = Good('cans of soup', [75, 595])
bagels = Good('bagels', [20, 295])
yoyos = Good('yo-yos', [125, 1995])
sport_coats = Good('sport coats', [1995, 99500])
turkeys = Good('pounds of Thanksgiving turkey', [45, 495])
electric_blankets = Good('electric blankets', [595, 2995])
sunglasses = Good('sunglasses', [325, 25500])

class MaxRevenue(Question):
    """
    The given is an expanded form of

    \\[
        a(x - h)^2 + k
    \\]

    The directions are to find the max or min.  Answer example:
    "Max at x = h  of y = k"
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        item = random.choice([cans_of_soup,
                                    bagels,
                                    yoyos,
                                    sport_coats,
                                    turkeys,
                                    electric_blankets,
                                    sunglasses])
        item_plural = item.plural_name
        l, u = item.plausible_optimums
        optimum = 0.01*random.randint(l, u)
        b = 0.01*random.randint(1500,6000)
        a = float(str(round(-b/2/optimum, 3)))

        self.item_plural = item_plural
        self.a = a
        self.b = b

        u = lambda x: b + a*x
        y = lambda x: x*u(x)

        x = Symbol('x')
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')


        h = -b/2/a
        k = y(h)
        self.h = h
        self.k = k
        self.format_answer = f"""
        Max revenue of y = {k:.5f} million dollars at x = {h:.2f} dollars apiece
        """

        self.prompt_single = f"""
        Say that it has been determined through market research that the
        number \(u\) of millions of  {item_plural} sold can be given as a function of
        the price \(x\) at which they are sold (in dollars less than ${round(-b/a, 2):.2f})
        using the following formula:
        \[
        u = {latex(u(x))}
        \]
        Find the price \(x\) that maximizes the revenue.
        """

        self.format_given_for_tex = f"""
        Say that it has been determined through market research that the
        number \(u\) of millions of  {item_plural} sold can be given as a function of
        the price \(x\) (in dollars less than \${latex(round(-b/a, 2))})
        using the following formula:
        \[
        u = {latex(b+a*x)}
        \]
        Find the price \(x\) that maximizes the revenue.
        """

        self.further_instruction = f"""
        Your answer should be of the following style (or close to it), with items highlighted in
        red replaced by your answer:

        <blockquote>
            Max revenue of y = <span style="color: red">200</span> million dollars at
            x = <span style="color: red">100</span> dollars apiece
        </blockquote>

        Do NOT use commas to format numbers.  For instance, write '2220' not '2,220'.
        Your answer must be accurate to two decimal places.
        """

    name = 'Max Revenue Problem'
    module_name = 'max_revenue_problem'





    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        if 'min' in user_answer:
            return False
        if ' x' not in user_answer or ' y' not in user_answer:
            return False
        i = user_answer.find(' x')
        user_x = user_answer[i+2:]
        i = user_x.find('=')
        user_x = user_x[i+1:]
        user_x = user_x.strip()
        i = user_x.find(' ')
        if i != -1:
            user_x = user_x[:i]
        user_x = user_x.replace('^', '**')
        user_x = parse_expr(user_x, transformations=transformations)
        i = user_answer.find(' y')
        user_y = user_answer[i+2:]
        i = user_y.find('=')
        user_y = user_y[i+1:]
        user_y = user_y.strip()
        i = user_y.find(' ')
        if i != -1:
            user_y = user_y[:i]
        user_y = user_y.replace('^', '**')
        user_y = parse_expr(user_y, transformations=transformations)
        return abs(user_x - self.h) < 0.005 and abs(user_y -self.k) < max(-self.a*0.01*self.h + self.b*0.005, 0.005)

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
            if ' x' not in user_answer or ' y' not in user_answer:
                raise SyntaxError
            i = user_answer.find(' x')
            user_x = user_answer[i+2:]
            i = user_x.find('=')
            user_x = user_x[i+1:]
            user_x = user_x.strip()
            i = user_x.find(' ')
            if i != -1:
                user_x = user_x[:i]
            user_x = user_x.replace('^', '**')
            user_x = parse_expr(user_x, transformations=transformations)
            i = user_answer.find(' y')
            user_y = user_answer[i+2:]
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


Question_Class = MaxRevenue
prob_type = 'math_blank'
