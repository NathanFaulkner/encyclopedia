#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            list_integer_factors,
                            has_numbers)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class SolvingEquationWithRationalQuadratic(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)

        b1 = random.randint(-5,5)
        b2 = random.randint(-5,5)
        x = sy.Symbol('x')
        c = random_non_zero_integer(-5,5)
        d = b1+b2 - c
        A = c*d - b1*b2
        while A == 0:
            c = random_non_zero_integer(-5,5)
            d = b1+b2 - c
            A = c*d - b1*b2
        factors = list_integer_factors(A)
        a1 = random.choice(factors)
        a2 = int(A/a1)
        n1 = a1
        n2 = x + c
        d1 = x + d
        d2 = a2

        if abs(a2) != 1:
            prob = '\\frac{{{n1}}}{{{d1}}} = \\frac{{{n2}}}{{{d2}}}'.format(n1=n1, n2=n2, d1=d1, d2=d2)
        else:
            prob = '\\frac{{{n1}}}{{{d1}}} = {expr}'.format(n1=n1, d1=d1, expr=latex(n2/d2))

        self.answer = set(sy.solve(n1/d1 - n2/d2, x))
        # print(self.answer)
        if self.answer == set():
            fmt_ans = 'No solution'
            self.has_solutions = False
        else:
            self.has_solutions = True
            fmt_ans = '\\( '
            for ans in self.answer:
                fmt_ans += f'{sy.latex(ans)}, '
            fmt_ans = fmt_ans[:-2]
            fmt_ans += ' \\)'

        self.format_answer = fmt_ans

        self.format_given = f"\\[{prob}\\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Rationals: Solving, Level 2'
    module_name = 'solving_equation_with_rational_quadratic'

    prompt_single = """Find the solution set.  (It is wise to check you answer(s).)"""
    prompt_multiple = """TBA"""

    further_instruction = """
    """

    # loom_link = "https://www.loom.com/share/6cbdb245ddf94247985dc59deac4cbf2?sharedAppSource=personal_library"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        if not self.has_solutions:
            return 'no' in user_answer.lower() or 'null' in user_answer.lower() or 'empty' in user_answer.lower()
        else:
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('or', ',')
            user_answers = user_answer.split(',')
            i = 0
            while i < len(user_answers):
                user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
                i += 1
            user_answers = set(user_answers)
            print('user_answers', user_answers)
            print('answer', self.answer)
            return self.answer == user_answers

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        if 'no' in user_answer or 'null' in user_answer or 'empty' in user_answer:
            return user_answer
        else:
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('or', ',')
            user_answers = user_answer.split(',')
            i = 0
            while i < len(user_answers):
                user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
                i += 1
            user_answers = set(user_answers)
            format_answer = ''
            for ans in user_answers:
                format_answer += sy.latex(ans) + ' ,'
            format_answer = format_answer[:-2]
            return '\(' + format_answer + '\)'


    @staticmethod
    def validator(user_answer):
        try:
            # pass
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('or', ',')
            if not has_numbers(user_answer):
                if 'no' not in user_answer and 'null' not in user_answer and 'empty' not in user_answer:
                    raise SyntaxError
            user_answers = user_answer.split(',')
            i = 0
            while i < len(user_answers):
                user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
                i += 1
            user_answers = set(user_answers)
            format_answer = ''
            for ans in user_answers:
                format_answer += sy.latex(ans) + ' ,'
            format_answer = format_answer[:-2]
        except:
            raise SyntaxError

Question_Class = SolvingEquationWithRationalQuadratic
prob_type = 'math_blank'
