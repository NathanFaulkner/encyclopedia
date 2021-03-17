#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            get_integer_divisors,
                            fmt_abs_value,
                            has_numbers,
                            split_at_comma_not_in_parens,
                            )



class SolvePowerEquationLevel2(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        n,m = random.choice([[1,2],[1,2], [1,3],[1,4],[2,3],[3,4], [3,2], [4,3]])
        base = random.randint(-7,7)
        root_answer = random.choice([True, True, False])
        if root_answer:
            if n % 2 == 0:
                T = abs(base)**n
            else:
                T = base**n
        else:
            T = base
        whether_b = random.choice([True, True, True, False])
        whether_A = random.choice([True, True, True, False])
        whether_C = random.choice([True, True, True, False])
        if whether_b:
            b = random_non_zero_integer(-10,10)
        else:
            b = 0
        if whether_A:
            A = random_non_zero_integer(-10,10)
        else:
            A = 1
        if whether_C:
            C = random_non_zero_integer(-10,10)
        else:
            C = 0
        x = sy.Symbol('x', real=True)
        LHS = sy.Add(sy.Mul(A,(x-b)**sy.Rational(n,m), evaluate=False),C, evaluate=False)
        RHS = A*T + C
        prob = sy.Eq(LHS, RHS)
        answer = sy.solve(prob, x)
        if n % 2 == 1:
            self.answer = set(answer)
        elif len(answer) == 1:
            print('hello')
            ans = answer[0]
            other_ans = -ans + 2*b
            self.answer = set([ans, other_ans])
        print('self.answer', self.answer)
        self.has_solutions = self.answer != set()
        if self.has_solutions:
            format_answer = ''
            for ans in self.answer:
                format_answer += sy.latex(ans) + ' ,'
            format_answer = format_answer[:-2]
            self.format_answer = '\(' + format_answer + '\)'
        else:
            # self.answer = 'No solution'
            self.format_answer = self.answer
            self.format_answer = 'No solution'
        self.format_given = f"""
        \\[
            {sy.latex(prob)}
        \\]"""

        self.prompt_single = f"""Find all reals that solve the equation.
        (Find the solution set&mdash;the set of all real numbers that would make the equation
        true when substituted in.)
        """

        self.format_given_for_tex = f"""
        Find all reals that solve the equation.  (Find the solution set---the set of all real numbers that would make the equation
        true when substituted in.)

        {self.format_given}
        """

    # def non_zero_integer(a,b):
    #     n = 0
    #     while n == 0:
    #         n = random.randint(a,b)
    #     return n



    name = 'Solve Power Equation with Fraction Power'
    module_name = 'solve_power_equation_level2'


    prompt_multiple = """TBA"""

    further_instruction = """
    <p>
    Enter multiple answers separated by commas.

    <p>
    To enter a radical, you will use the symbol "root".  For example,
    to enter
    \\[
        \sqrt[3]{2x^2}
    \\]
    you will need to enter
    <div style="margin-left: auto; margin-right: auto; text-align:center; padding:10px;">
        root(2x^2, 3)
    </div>
    In case you are curious, this is the syntax for a Python (Sympy)
    function 'root', whose first "argument" (input) is what goes
    under the radical sign and whose second argument is the type
    of root&mdash;e.g.: 3 for cube root, 4 for 4th root, etc.
    """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        if not self.has_solutions:
            return 'no' in user_answer.lower() or 'null' in user_answer.lower() or 'empty' in user_answer.lower()
        else:
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('or', ',')
            # print('user_answer', user_answer)
            user_answers = split_at_comma_not_in_parens(user_answer)
            # print('USER', user_answers)
            i = 0
            while i < len(user_answers):
                print(i, user_answers[i])
                user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
                i += 1
            user_answers = set(user_answers)
            # print('user', user_answers)
            # print('ans', self.answer)
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
            user_answers = split_at_comma_not_in_parens(user_answer)
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

Question_Class = SolvePowerEquationLevel2
prob_type = 'math_blank'
