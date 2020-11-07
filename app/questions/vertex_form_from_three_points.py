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
                            signed_coeff, leading_coeff, sgn,
                            fmt_slope_style)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class VertexFormFromThreePoints(Question):
    """
    Interpolation of three points
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-5,5)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.randint(-10,10)
        if 'c' in kwargs:
            self.c = kwargs['c']
        else:
            self.c = random.randint(-10,10)
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')



        a = self.a
        b = self.b
        c = self.c
        h = Rational(-b, 2*a)
        x = self.x
        self.answer = a*x**2 + b*x + c
        self.format_answer = f'\\(y = {latex(self.answer)}\\)'

        expr = self.answer

        x_points = []
        for i in range(3):
            x_point = random.randint(-5,5)
            while x_point in x_points:
                x_point = random.randint(-5,5)
            x_points.append(x_point)

        self.points = [(x_point, expr.subs(x, x_point)) for x_point in x_points]
        print_points = ''
        for point in self.points:
            print_points += f'{latex(point)}, '
        print_points = print_points[:-2]

        self.format_given = f"""
        \\[
            {print_points}
        \\]
        """

        self.format_given_for_tex = f"""
        Previously, you have learned that any two
        distinct points determine a line.
        It turns out that any three points determine a
        quadratic---as long as they don't instead all
        happen to lie on a line (also two points
        can't share the same \(x\) if you intend to solve for \(y\).)

        Find a formula for a quadratic function whose graph
        passes through the given points.  Clearly indicate
        each step in the process you used to solve this problem!

        {self.format_given}

        \\textit{{Hint: A quadratic function is one that can be given in the form
        \\[
            y = ax^2 + bx + c
        \\]
        for some numbers \\(a\\), \\(b\\), and \\(c\\), where \\(a \\neq 0\\).
        Furthermore, for each of these given points, this equation
        must be true when \(x\) and \(y\) are subbed in.  See what you
        can figure out from there.}}
        """

    name = 'Vertex Form from Three Points'
    module_name = 'vertex_form_from_three_points'

    prompt_single = """Previously, you have learned that any two
    distinct points determine a line.
    It turns out that any three points determine a
    quadratic&mdash;as long as they don't instead all
    happen to lie on a line (also two points
    can't share the same \(x\) if you intend to solve for \(y\).)

    <br>
    <br>
    Find a formula for a quadratic function whose graph
    passes through the given points."""
    prompt_multiple = """TBA"""

    further_instruction = """
    Enter your answer as "y = [your formula]".
    """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = user_answer.replace(' ', '')
        user_answer = user_answer.replace('f(x)', 'y')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        y = Symbol('y')
        user_answer = solve(user_answer, y)[0]
        return self.answer == expand(user_answer)

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.lower()
        # user_answer = user_answer.replace('^', '**')
        return f'\\({user_answer}\\)'

    @classmethod
    def validator(self, user_answer):
        try:
            pass
            # user_answer = user_answer.lower()
            # user_answer = user_answer.replace('^', '**')
            # user_answer = user_answer.replace(' ', '')
            # user_answer = user_answer.replace('f(x)', 'y')
            # lhs, rhs = user_answer.split('=')
            # lhs = parse_expr(lhs, transformations=transformations)
            # rhs = parse_expr(rhs, transformations=transformations)
            # user_answer = Eq(lhs, rhs)
            # y = Symbol('y')
            # user_answer = solve(user_answer, y)[0]
        except:
            raise SyntaxError


Question_Class = VertexFormFromThreePoints
prob_type = 'math_blank'
