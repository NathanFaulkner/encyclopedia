#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *

from app.questions import Question, latex_print, random_non_zero_integer, sgn, has_letters


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class SolvingByFactoringLevel1(Question):
    """
    The given is an expanded form of

    \\[
        (x - x1)(x - x2) = 0
    \\]

    The directions are to solve.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            a=0
            while a == 0:
                a = int(random.triangular(-9,9))
        self.a = 1
        symb_a = '{}'.format(a)
        if a == 1:
            symb_a = ''
        elif a == -1:
            symb_a = '-'
        if 'x1' in kwargs:
            self.x1 = kwargs['x1']
        else:
            self.x1 = random_non_zero_integer(-9,9)
        # if 'gcf' in kwargs:
        #     self.gcf = kwargs['gcf']
        # else:
        #     self.gcf = random.choice([False, False, True])
        # if self.gcf:
        #     self.x2 = 0
        # else:
        if 'x2' in kwargs:
            self.x2 = kwargs['x2']
        else:
            self.x2 = random_non_zero_integer(-9,9)
        # self.x2 = self.x1
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        a = self.a
        x1 = self.x1
        x2 = self.x2
        x = self.x
        self.answer = set([x1, x2])
        ans = ''
        for answer in self.answer:
            ans += latex(answer) + ', '
        ans = ans[:-2]
        self.format_answer = f'\( {ans}\)'

        expr = expand((x-x1)*(x-x2))
        self.format_given = f"\\[{latex(expr)} = 0 \\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Solve by Factoring, Level 1'
    module_name = 'solving_by_factoring_level1'

    prompt_single = """Solve by factoring."""
    prompt_multiple = """TBA"""

    further_instruction = """If you get more than one solution,
    enter your answers separated by commas.  For instance, if you
    get \(2, -1\) as your solutions, then would just enter "2, -1".
    """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        if has_letters(user_answer):
            if 'x' not in user_answer:
                return False
            else:
                user_answer = user_answer.replace('x', '')
                user_answer = user_answer.replace('=', '')
                user_answer = user_answer.replace(',', '')
                user_answers = user_answer.split('or')
        else:
            user_answers = user_answer.split(',')
        user_answers = [parse_expr(ans, transformations=transformations) for ans in user_answers]
        user_answers = set(user_answers)
        return self.answer == user_answers

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        if has_letters(user_answer):
            if 'x' not in user_answer:
                return user_answer
            else:
                user_answer = user_answer.replace('x', '')
                user_answer = user_answer.replace('=', '')
                user_answer = user_answer.replace(',', '')
                user_answers = user_answer.split('or')
                user_answers = [parse_expr(ans, transformations=transformations) for ans in user_answers]
                out = ''
                for ans in user_answers:
                    out += latex(ans) + ', '
                out = out[:-2]
                return f'\\({out}\\)'
        else:
            return f'\\({user_answer}\\)'

    @classmethod
    def validator(self, user_answer):
        try:
            # pass
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            if has_letters(user_answer):
                if 'x' not in user_answer:
                    raise SyntaxError
                elif ',' in user_answer and 'or' not in user_answer:
                    raise SyntaxError
                else:
                    user_answer = user_answer.replace('x', '')
                    user_answer = user_answer.replace('=', '')
                    user_answer = user_answer.replace(',', '')
                    user_answers = user_answer.split('or')
            else:
                user_answers = user_answer.split(',')
            user_answers = [parse_expr(ans, transformations=transformations) for ans in user_answers]
            user_answers = set(user_answers)
        except:
            raise SyntaxError


Question_Class = SolvingByFactoringLevel1
prob_type = 'math_blank'
