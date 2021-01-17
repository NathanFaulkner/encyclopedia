#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, random_non_zero_integer, latex_print, has_numbers



class CompleteFactorizationLevel1(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)

        x = sy.Symbol('x', real=True)
        z = 0
        while z == 0:
        	z = random.randint(-10,10)
        self.z = z
        a = 0
        while a == 0:
        	a = random.randint(-9,9)
        b = random.randint(-9,9)
        c = random.randint(-10,10)
        # a = 1
        # b = 1
        # c = 1

        if 'nice' in kwargs:
            self.nice = kwargs['nice']
        else:
            self.nice = False

        if self.nice:
            z1 = 0
            while z1 == 0:
            	z1=random.randint(-10,10)
            z2=random.randint(-10,10)
            expr = (x-z)*(x-z1)*(x-z2)
        else:
            expr = (x-z)*(a*x**2+b*x+c)
        #symb_z = Symbol(str(z))

        self.answer = set(sy.solve(expr))
        self.format_given = f"""\\(x= {z}\\) is a solution of
        \[
            {sy.latex(sy.expand(expr))} = 0
        \]"""

        fmt_ans = ''
        for item in self.answer:
            fmt_ans += f'{sy.latex(item)}, '
        fmt_ans = fmt_ans[:-2]
        self.format_answer = f"""\\({fmt_ans}\\)"""

        self.prompt_single = f"""
            For the following, you will be given one solution.  Use that to find all solutions.
        """

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = "Complete Factorization, Level 1"
    module_name = 'complete_factorization_level1'


    prompt_multiple = """For each of the following, you will be given one solution.  Use that to find all solutions."""

    further_instruction = """If you get one or more solutions,
    enter symbols for your solutions separated by commas.
    Use 'sqrt()' (without the quotes) to enter square roots.  For instance,
    a possible solution might be
    \\[
        x = \\frac{7 - \\sqrt{157}}{18} \\quad \\textrm{or} \\quad x = \\frac{7 + \\sqrt{157}}{18}
    \\]
    You would enter, "(7 - sqrt(157))/18, (7 + sqrt(157))/18".
    """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        if 'no' in user_answer.lower() or 'null' in user_answer.lower() or 'empty' in user_answer.lower():
            print(self.answer - {self.z})
            if self.answer - {self.z} == set():
                # print('true')
                if 'other' in user_answer.lower():
                    return True
            return False
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
            return self.answer == user_answers or user_answers == self.answer - {self.z}

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


Question_Class = CompleteFactorizationLevel1
prob_type = 'math_blank'
