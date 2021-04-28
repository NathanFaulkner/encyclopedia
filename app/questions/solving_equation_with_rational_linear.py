#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            sets_evaluate_equal,
                            check_congruence_after_factoring_out_gcf,
                            get_numer_denom,
                            congruence_of_quotient,
                            has_numbers)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class SolvingEquationWithRationalLinear(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        a1 = random_non_zero_integer(-5,5)
        a2 = random_non_zero_integer(-5,5)
        b1 = random.randint(-5,5)
        b2 = random.randint(-5,5)
        x = sy.Symbol('x')
        d1 = x - b1
        d2 = x - b2

        prob = '\\frac{{{a1}}}{{{d1}}} = \\frac{{{a2}}}{{{d2}}}'.format(a1=a1, a2=a2, d1=d1, d2=d2)

        self.answer = set(sy.solve(a1/d1 - a2/d2, x))
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

    name = 'Rationals: Solving, Level 1'
    module_name = 'solving_equation_with_rational_linear'

    prompt_single = """Find the solution set.  (It is wise to check you answer(s).)"""
    prompt_multiple = """TBA"""

    # further_instruction = """
    # """

    loom_link = "https://www.loom.com/share/6a4dfb67b2e54348b267a685472fc176?sharedAppSource=personal_library"

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

Question_Class = SolvingEquationWithRationalLinear
prob_type = 'math_blank'
