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

class AbsoluteValueEquationPlusLinear(Question):
    """
    The given is
    \\[
        |ax + b| + c = dx + e
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
        if 'num_solutions' in kwargs:
            self.num_solutions = kwargs['num_solutions']
        else:
            self.num_solutions = random.choice([0, 1, 2, 0, 1, 2, oo])
            # self.num_solutions = oo
        num_solutions = self.num_solutions
        print('num_solutions', num_solutions)
        if 'difficulty' in kwargs:
            self.difficulty = kwargs['difficulty']
        else:
            self.difficulty = random.choice([1, 1, 2])
        self.p = random_non_zero_integer(-9,9)
        self.q = random.randint(1, 5)
        self.r = Rational(self.p,self.q)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random.randint(1, 4)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')
        d_fact = random.choice([-1, 1])
        if num_solutions == oo:
            e_prime = 0
            self.d = self.a * d_fact
            if d_fact > 0:
                self.answer = Interval(self.r, oo)
                self.format_answer = f'\\( x \geq {self.r} \\)'
                self.ineq_answer = self.x >= self.r
            else:
                self.answer = Interval(-oo, self.r)
                self.format_answer = f'\\( x \leq {self.r} \\)'
                self.ineq_answer = self.x <= self.r
        elif num_solutions == 0:
            e_prime = random.randint(-9, -1)
            self.d = d_fact*random.randint(1, abs(self.a))
            self.format_answer = 'No Solution'
            self.answer = EmptySet
        elif num_solutions == 1:
            e_prime = random_non_zero_integer(-9, 9)
            if e_prime < 0:
                self.d = d_fact*random.randint(abs(self.a)+1, 6)
            else:
                self.d = d_fact*random.randint(abs(self.a), 6)
        else: # num_solutions == 2:
            e_prime = random.randint(1,9)
            self.d = d_fact * random.randint(1, abs(self.a))


        if num_solutions in [1,2]:
            things_to_check = []
            try:
                x0 = Rational(e_prime, self.a - self.d) + self.r
                things_to_check.append(x0)
            except ZeroDivisionError:
                pass
            try:
                x0 = Rational(-e_prime, self.a + self.d) + self.r
                things_to_check.append(x0)
            except ZeroDivisionError:
                pass
            solutions = EmptySet
            for x0 in things_to_check:
                lhs = self.a*abs(self.x - self.r)
                rhs = self.d*(self.x - self.r) + e_prime
                if lhs.subs(self.x, x0) == rhs.subs(self.x, x0):
                    solutions += FiniteSet(x0)
            self.answer = solutions
            if self.answer == EmptySet:
                self.num_solutions = 0
                self.format_answer = 'No Solution'
            else:
                fmt_answer = '\\('
                for x in self.answer:
                    fmt_answer += f'{latex(x)}, '
                fmt_answer = fmt_answer[:-2]
                fmt_answer += '\\)'
                self.format_answer = fmt_answer
                # self.format_answer = f'\({latex(self.answer)}\)'

        if 'c' in kwargs:
            self.c = kwargs['c']
        else:
            self.c = random.randint(-9,9)
        self.e = e_prime + self.c

        x = self.x
        a = self.a
        r = self.r
        c = self.c
        d = self.d
        e = self.e
        q = self.q
        split_d = random.randint(-9,9)
        terms = [abs(q*a*(x-r)),
                q*c,
                -q*(d+split_d)*(x-r),
                -q*e,
                q*(split_d)*(x-r)]
        # lhs = abs(self.q*a*(x - r)) + q*c
        # rhs = self.q*(d*(x - r) + e)
        eq = permute_equation(terms, seed=self.seed)

        self.given = eq
        self.format_given = f'\\[{latex(eq)}\\]'

        self.format_given_for_tex = f"""
        {self.prompt_single} \n
        {self.format_given}
        """



    name = 'Absolute Value Equation, Plus Linear'
    module_name = 'absolute_value_equation_plus_linear'

    prompt_single = 'Solve for \\(x\\).  (Find the solution set.) '
    prompt_multiple = 'For each of the following, solve for \\(x\\).  (Find the solution set.)'
    further_instruction = """If you have more than one number in the
    solution set, enter them separated by commas.  For instance, you might
    enter "-1, 3" as the answer to some problem (possibly but not likely this one!)

    <p>
    If you have an inequality answer, enter \\(\\leq\\) as "<=" and \\(\\geq\\)
    as ">=".  For instance, a possible answer might be "x <= -9/5".
    </p>

    <p>
    If your answer is "No Solution", just type that.
    </p>
    """

    # loom_link = "https://www.loom.com/share/4408bcd698d041e9917ba44ed17fbb2e"


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'




    def checkanswer(self, user_answer):
        if self.num_solutions == 0:
            return 'no' in user_answer.lower() or 'null' in user_answer.lower() or 'empty' in user_answer.lower() or user_answer.replace(' ', '') == '{}'
        else:
            # user_answer = user_answer.replace('x', ' ')
            # user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            # user_answer = user_answer.replace('or', ',')
            user_answers = user_answer.split(',')
            i = 0
            while i < len(user_answers):
                user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
                i += 1
            user_answers = set(user_answers)
            if self.num_solutions == oo:
                if len(user_answers) == 1:
                    user_answer = list(user_answers)[0]
                    cong = AbsoluteValueEquationPlusLinear.congruent
                    print(type(user_answer))
                    return cong(user_answer, self.ineq_answer)
                else:
                    return False
            return self.answer == user_answers

    @staticmethod
    def congruent(ineq1, ineq2):
        try:
            return ineq1.equals(ineq2)
        except TypeError:
            return False

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.lower()
        if self.num_solutions == 0:
            return user_answer
        elif 'no' in user_answer or 'null' in user_answer or 'empty' in user_answer or user_answer.replace(' ', '') == '{}':
            return user_answer
        else:
            # user_answer = user_answer.replace('x', ' ')
            # user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            # user_answer = user_answer.replace('or', ',')
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
            # user_answer = user_answer.replace('x', ' ')
            # user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            # user_answer = user_answer.replace('or', ',')
            if has_letters(user_answer):
                if '<' in user_answer or '>' in user_answer:
                    print('great!')
                elif 'no' not in user_answer and 'null' not in user_answer and 'empty' not in user_answer:
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


Question_Class = AbsoluteValueEquationPlusLinear
