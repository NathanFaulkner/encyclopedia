#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation,
                            has_numbers)


prob_type = 'math_blank'

class SolveByCompletingTheSquare(Question):
    """
    The given is
    \\[
        a(x-b)^2 + c = d,
    \\]
    but expanded and permuted with =... possibly recombine
    with extra quadratic terms added to both sides...
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'has_solutions' in kwargs:
            self.has_solutions = kwargs['has_solutions']
        else:
            self.has_solutions = random.choice([True,True,False])
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-3,3)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.randint(-9,9)
        if 'sqr' in kwargs:
            self.sqr = kwargs['sqr']
        else:
            if self.has_solutions:
                p = random.randint(0,9)
                q = random.choice([1, 1, 1, 2, 3])
                self.sqr = sy.Rational(p,q)
            else:
                p = random.randint(-9,-1)
                q = random.choice([1, 1, 1, 2, 3])
                self.sqr = sy.Rational(p,q)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('x')
        x = self.x
        a = self.a
        b = self.b
        sqr = self.sqr
        d = a*self.sqr
        self.d = d
        difficulty = random.choice([0,0,1,1,2])
        aux_a = 0
        aux_b = 0
        aux_c = int(random.triangular(-9,9,0))
        if difficulty > 0:
            aux_b = random_non_zero_integer(-9,9)
        if difficulty > 1:
            aux_a = random_non_zero_integer(-9,9)
        aux = aux_a*x + aux_b*x + aux_c
        LHS = q*sy.expand(a*(x-b)**2) + aux
        RHS = q*d + aux
        self.given = f'{sy.latex(LHS)} = {sy.latex(RHS)}'
        if self.has_solutions:
            self.answer = {-sy.sqrt(sqr)+b, sy.sqrt(sqr)+b}
            format_answer = ''
            for ans in self.answer:
                format_answer += sy.latex(ans) + ' ,'
            format_answer = format_answer[:-2]
            self.format_answer = '\(' + format_answer + '\)'
        else:
            self.answer = 'No solution'
            self.format_answer = self.answer

        self.given_latex = latex_print(self.given)
        self.given_latex_display = latex_print(self.given, display=True)
        self.format_given = self.given_latex_display
        self.answer_latex = latex_print(self.answer)
        self.answer_latex_display = latex_print(self.answer, display=True)


        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.given_latex_display}
        """

    name = 'Solve by Completing the Square'
    module_name = 'solve_by_completing_the_square'

    prompt_single = 'Solve for \\(x\\) by completing the square and taking square roots.  (Find the solution set.) '
    prompt_multiple = 'TBA'
    further_instruction = """If you get one or more solutions,
    enter symbols for your solutions separated by commas.
    Use 'sqrt()' (without the quotes) to enter square roots.  For instance,
    a possible solution might be
    \\[
        x = 5 - \\sqrt{\\frac{3}{2}} \\quad \\textrm{or} \\quad x = 5 + \\sqrt{\\frac{3}{2}}
    \\]
    You would enter, "5 - sqrt(3/2), 5 + sqrt(3/2)".
    """

    # loom_link = "https://www.loom.com/share/331e43b308a64cefbafdb1ac3211c9ac"


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
            return self.answer == user_answers

    def format_useranswer(self, user_answer, display=False):
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

    @classmethod
    def validator(self, user_answer):
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



Question_Class = SolveByCompletingTheSquare
