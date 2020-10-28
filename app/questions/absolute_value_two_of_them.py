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

class AbsoluteValueTwoOfThem(Question):
    """
    The given is
    \\[
        |ax + b| + c = sign*|dx + e|
    \\]
    No solution is possible.  (Use kwarg 'force_no_solution=True').
    Infinite solutions is possible.  (Use kwarg 'force_infinite_solutions=True')
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'force_no_solution' in kwargs:
            self.force_no_solution = kwargs['force_no_solution']
        else:
            self.force_no_solution = random.choice([False, False, False, True])
        if 'force_infinite_solutions' in kwargs:
            self.force_infinite_solutions = kwargs['force_infinite_solutions']
        else:
            if not self.force_no_solution:
                self.force_infinite_solutions = random.choice([False, False, False, True])
            else:
                self.force_infinite_solutions = False
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-6, 6)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.randint(-6, 6)
        if 'c' in kwargs:
            self.c = kwargs['c']
        else:
            self.c = random.randint(-9, 9)
        if 'e' in kwargs:
            self.e = kwargs['e']
        else:
            self.e = random.randint(-9, 9)
        if 'sign' in kwargs:
            self.sign = kwargs['sign']
        else:
            self.sign = random.choice([-1,1])
        if self.force_no_solution:
            self.c = random_non_zero_integer(-9,9)
            self.d = self.a
            while self.e == self.b:
                self.e = random.randint(-9, 9)
            self.c = abs(self.e - self.b) + random.randint(1,9)
        elif self.force_infinite_solutions:
            self.c = random_non_zero_integer(-9,9)
            self.d = self.a
            while self.e == self.b:
                self.e = random.randint(-9, 9)
            self.c = self.a*(self.e - self.b)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')

        x = self.x
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e

        lhs = abs(a*x + b) + c
        rhs = abs(d*x + e)
        solutions = []

        if a != d:
            x0 = Rational((e - b - c),(a - d))
            if lhs.subs(x, x0) == rhs.subs(x, x0):
                solutions.append(x0)
            x0 = Rational((e + b - c),(a - d))
            if lhs.subs(x, x0) == rhs.subs(x, x0):
                solutions.append(x0)
        else:
            if -e + b + c == 0:
                if c < 0:
                    self.ineq_answer = x >= Rational(-e,d)
                elif c == 0:
                    self.answer = 'All real numbers'
                else:
                    self.ineq_answer = x >= Rational(-b,a)
        if a != -d:
            x0 = Rational((-e - b - c),(a + d))
            if lhs.subs(x, x0) == rhs.subs(x, x0):
                solutions.append(x0)
            x0 = Rational((e + b - c),(a + d))
            if lhs.subs(x, x0) == rhs.subs(x, x0):
                solutions.append(x0)


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



    name = 'Equation with Two Absolute Value Terms'
    module_name = 'absolute_value_two_of_them'

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
