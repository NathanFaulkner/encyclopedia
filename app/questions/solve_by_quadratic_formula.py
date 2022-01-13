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

class SolveByQuadraticFormula(Question):
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
        # if 'has_solutions' in kwargs:
        #     self.has_solutions = kwargs['has_solutions']
        # else:
        #     self.has_solutions = random.choice([True,True,False])
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-9,9)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.randint(-9,9)
        if 'c' in kwargs:
            self.c = kwargs['c']
        else:
            self.c = random.randint(-9,9)
            # if self.has_solutions:
            #     while (self.b**2 - 4*self.a*self.c < 0):
            #         print('doin stuff')
            #         self.c = random.randint(-9,9)
            # else:
            #     while (self.b**2 - 4*self.a*self.c >= 0):
            #         print('doin other stuff')
            #         self.c = random.randint(-9,9)
        if (self.b**2 - 4*self.a*self.c < 0):
            self.has_solutions = False
        else:
            self.has_solutions = True
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('x')
        x = self.x
        a = self.a
        b = self.b
        c = self.c
        difficulty = random.choice([0,0,0,1,1,2])
        # difficulty = 2
        aux_a = 0
        aux_b = 0
        aux_c = int(random.triangular(-9,9,0))
        if difficulty > 0:
            aux_b = random_non_zero_integer(-9,9)
        if difficulty > 1:
            aux_a = random_non_zero_integer(-9,9)
        aux = aux_a*x**2 + aux_b*x + aux_c
        LHS = sy.expand(a*x**2 + b*x + c + aux)
        RHS = aux
        self.given = f'{sy.latex(LHS)} = {sy.latex(RHS)}'
        if self.has_solutions:
            self.answer = {(-b-sy.sqrt(b**2-4*a*c))/(2*a), (-b+sy.sqrt(b**2-4*a*c))/(2*a)}
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

    name = 'Solve by the Quadratic Formula'
    module_name = 'solve_by_quadratic_formula'

    prompt_single = """Solve for \\(x\\) using the quadratic formula.
    If you get a negative under the radical (the square root sign), you should
    enter your answer as "No Solution," as the square root of a negative
    cannot be any real number."""
    prompt_multiple = 'TBA'
    further_instruction = """If you get one or more solutions,
    enter symbols for your solutions separated by commas.
    Use 'sqrt()' (without the quotes) to enter square roots.  For instance,
    a possible solution might be
    \\[
        x = \\frac{7 - \\sqrt{157}}{18} \\quad \\textrm{or} \\quad x = \\frac{7 + \\sqrt{157}}{18}
    \\]
    You would enter, "(7 - sqrt(157))/18, (7 + sqrt(157))/18".
    """

    prob_type = prob_type

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



Question_Class = SolveByQuadraticFormula
