#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, latex_print, random_non_zero_integer, sgn, has_letters


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class SolvingByFactoringLevel2(Question):
    """
    The given is an expanded form of

    \\[
        (mx + p)(nx + q) = 0
    \\]

    The directions are to solve.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        m = random.choice([1, 2, 3, 5])
        p = random.choice([-5,-3,-2,-1,1,2,3,5])
        n = random.choice([-5,-3,-2,-1,1,2,3,5])
        q = random.choice([-5,-3,-2,-1,1,2,3,5])
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('x')
        x = self.x
        expr = (m*x+p)*(n*x+q)
        self.answer = set([sy.Rational(-p,m), sy.Rational(-q,n)])
        ans = ''
        for answer in self.answer:
            ans += sy.latex(answer) + ', '
        ans = ans[:-2]
        self.format_answer = f'\( {ans}\)'

        expr = sy.expand(expr)
        random.seed(self.seed) # Why does reseeding seem to be necessary??
        two_sides = random.choice([True, False])
        if two_sides:
            a = random.randint(-6,6)
            b = random.randint(-6,6)
            c = random.randint(-10,10)
            RHS = a*x**2 + b*x +c
            LHS = (m*x+p)*(n*x+q) + RHS
            eqn = sy.Eq(sy.expand(LHS), sy.expand(RHS))
        else:
            eqn = sy.Eq(expr, 0)
        self.format_given = f"\\[{sy.latex(eqn)} \\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Solve by Factoring, Level 2'
    module_name = 'solving_by_factoring_level2'

    prompt_single = """Solve by factoring."""
    prompt_multiple = """TBA"""

    further_instruction = """If you get more than one solution,
    enter your answers separated by commas.  For instance, if you
    get \(\\frac{1}{2}, -1\) as your solutions, then would just enter "1/2, -1".
    """

    loom_link = "https://www.loom.com/share/f2a293dacfbf42369e52d8c1f450941f?sharedAppSource=personal_library"


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
                    out += sy.latex(ans) + ', '
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


Question_Class = SolvingByFactoringLevel2
prob_type = 'math_blank'
