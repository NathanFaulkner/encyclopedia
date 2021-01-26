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

class QuadraticOnlyOneX(Question):
    """
    The given is
    \\[
        a(x-b)^2 + c = d,
    \\]
    but permuted with =.
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
            self.a = random_non_zero_integer(-9,9)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.randint(-9,9)
        if 'c' in kwargs:
            self.c = kwargs['c']
        else:
            self.c = random_non_zero_integer(-9,9)
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
        c = self.c
        sqr = self.sqr
        d = a*self.sqr + c
        self.d = d
        terms = [q*sy.factor(a*(x-b)**2), q*c, -d*q]
        if not self.has_solutions:
            LHS, RHS = permute_equation(terms, as_list=True)
            self.given = f'{sy.latex(LHS)} = {sy.latex(RHS)}'
        else:
            self.given = permute_equation(terms)
        #print('3rd step: So far its ', expr)
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

    name = 'Solving Quadratic: Only One x'
    module_name = 'quadratic_only_one_x'

    prompt_single = 'Solve for \\(x\\) by taking square roots.  (Find the solution set.) '
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

    prob_type = 'math_blank'

    loom_link = "https://www.loom.com/share/ee216854a9e34de887fe610a26ae69f6?sharedAppSource=personal_library"


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



Question_Class = QuadraticOnlyOneX
