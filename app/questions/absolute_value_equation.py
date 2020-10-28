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
                            permute_equation,
                            has_letters)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general
prob_type = 'math_blank'

class AbsoluteValueEquation(Question):
    """
    The given is
    \\[
        |ax + b| + c = d + c
    \\]
    No solution is possible.  (Use kwarg 'no_solution=True').
    Difficulty levels are determined by the choice
    of a = 1 or c = 0.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'no_solution' in kwargs:
            self.no_solution = kwargs['no_solution']
        else:
            self.no_solution = random.choice([False, False, False, True])
        if 'difficulty' in kwargs:
            self.difficulty = kwargs['difficulty']
        else:
            self.difficulty = random.choice([1, 1, 2, 3])
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            if self.difficulty == 1:
                self.a = 1
            elif self.difficulty == 2:
                _a = random.choice(['a', 'c'])
                if _a == 'a':
                    self.a = random.randint(2,9)
                else:
                    self.a = 1
            else:
                self.a = random.randint(2,9)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random_non_zero_integer(-9,9)
        if 'c' in kwargs:
            self.c = kwargs['c']
        else:
            if self.difficulty == 1:
                self.c = 0
            elif self.difficulty == 2:
                if _a == 'a':
                    self.c = 0
                else:
                    self.c = random_non_zero_integer(-9,9)
            else:
                self.c = random_non_zero_integer(-9,9)
        if 'd' in kwargs:
            self.d = kwargs['d']
        else:
            if self.no_solution:
                self.d = random.randint(-9,-1)
            else:
                self.d = random.randint(0,9)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        self.genproblem()



    name = 'Absolute Value Equation'
    module_name = 'absolute_value_equation'

    prompt_single = 'Solve for \\(x\\).  (Find the solution set.) '
    prompt_multiple = 'For each of the following, solve for \\(x\\).  (Find the solution set.)'
    further_instruction = """If you have more than one number in the
    solution set, enter them separated by commas.  For instance, you might
    enter "-1, 3" as the answer to some problem (possibly but not likely this one!)
    """

    loom_link = "https://www.loom.com/share/4408bcd698d041e9917ba44ed17fbb2e"


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'

    def genproblem(self):
        out = {}
        x = self.x
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        no_solution = self.no_solution

        self.given = Eq(abs(a*x + b) + c, c + d)
        self.format_given = f'\\[{latex(abs(a*x+b)+c)} = {c+d}\\]'

        if no_solution:
            self.format_answer = 'No Solution'
        else:
            self.answer = {Rational(-b-d,a), Rational(-b+d, a)}
            format_answer = ''
            for ans in self.answer:
                format_answer += latex(ans) + ' ,'
            format_answer = format_answer[:-2]
            self.format_answer = '\(' + format_answer + '\)'

        self.format_given_for_tex = f"""
        {self.prompt_single} \n
        {self.format_given}
        """

    def checkanswer(self, user_answer):
        if self.no_solution:
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
            return self.answer == user_answers

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.lower()
        if self.no_solution:
            return user_answer
        elif 'no' in user_answer or 'null' in user_answer or 'empty' in user_answer:
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
                format_answer += latex(ans) + ' ,'
            format_answer = format_answer[:-2]
            return '\(' + format_answer + '\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('or', ',')
            if has_letters(user_answer):
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
                format_answer += latex(ans) + ' ,'
            format_answer = format_answer[:-2]
        except:
            raise SyntaxError


Question_Class = AbsoluteValueEquation
