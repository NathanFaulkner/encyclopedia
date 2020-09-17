#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *
import numpy as np
import json

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer)
from app.interpolator import cart_x_to_svg, cart_y_to_svg, get_parameters

from flask import render_template

# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general



prob_type = 'math_blank'

class SolveBySubstitution(Question):
    """
    The given is a graph of an equation of the form

    \\[
        y  = value
    \\]
    or
    \\[
        x = value
    \\]

    kwarg orientation is either vert or horiz

    The answer is the equation.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'how_many' in kwargs:
            self.how_many = kwargs['how_many']
        else:
            self.how_many = random.choice([0, 1, 1, 1, 1, oo])
        self.how_many = 1
        self.x_soln = random.randint(-10,10)
        self.y_soln = random.randint(-10,10)

        a = random_non_zero_integer(-10,10)
        b = random_non_zero_integer(-10,10)
        c = random_non_zero_integer(-10,10)
        d = random_non_zero_integer(-10,10)
        factor = random.choice([-5, -4, -3, -2, -1, 2, 3, 4, 5])

        solve_for_which = random.choice(['x', 'y'])
        top = random.choice([True, False])

        if self.how_many == 1:
            if solve_for_which == 'x':
            	if top:
            		a = random.choice([-1,1])
            	else:
            		c = random.choice([-1,1])
            	while a*d - b*c == 0:
            		d = random_non_zero_integer(-10,10)
            if solve_for_which == 'y':
            	if top:
            		b = random.choice([-1,1])
            	else:
            		d = random.choice([-1,1])
            	while a*d - b*c == 0:
            		c = random_non_zero_integer(-10,10)
            e0 = a*self.x_soln + b*self.y_soln
            e1 = c*self.x_soln + d*self.y_soln

        if self.how_many == 0:
            e0 = random.randint(-10,10)
            e1 = random.randint(-10,10)
            if solve_for_which == 'x':
            	if top:
            		a = random.choice([-1,1])
            		c = a*factor
            		d = b*factor
            		while e1 == e0*factor:
            			e1 = random.randint(-10,10)
            	else:
            		c = random.choice([-1,1])
            		a = c*factor
            		b = d*factor
            		while e0 == e1*factor:
            			e0 = random.randint(-10,10)
            if solve_for_which == 'y':
            	if top:
            		b = random.choice([-1,1])
            		d = b*factor
            		c = a*factor
            		while e1 == e0*factor:
            			e1 = random.randint(-10,10)
            	else:
            		d = random.choice([-1,1])
            		b = d*factor
            		a = c*factor
            		while e0 == e1*factor:
            			e0 = random.randint(-10,10)

        if self.how_many == oo:
            e0 = random.randint(-10,10)
            e1 = random.randint(-10,10)
            if solve_for_which == 'x':
            	if top:
            		a = random.choice([-1,1])
            		c = a*factor
            		d = b*factor
            		e1 = e0*factor
            	else:
            		c = random.choice([-1,1])
            		a = c*factor
            		b = d*factor
            		e0 = e1*factor
            if solve_for_which == 'y':
            	if top:
            		b = random.choice([-1,1])
            		d = b*factor
            		c = a*factor
            		e1 = e0*factor
            	else:
            		d = random.choice([-1,1])
            		b = d*factor
            		a = c*factor
            		e0 = e1*factor

        x, y = symbols('x y')

        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e0 = e0
        self.e1 = e1

        self.eq1 = Eq(self.a*x + self.b*y,self.e0)
        self.eq2 = Eq(self.c*x + self.d*y,self.e1)

        self.format_given = f"""
        \\[
            \\begin{{cases}}
                {latex(self.eq1)}\\\\
                {latex(self.eq2)}
            \\end{{cases}}
        \\]
        """
        if self.how_many == 0:
            self.format_answer = 'No solution'
        elif self.how_many == 1:
            self.format_answer = f'\(x = {self.x_soln}, y = {self.y_soln}\)'
        else:
            self.answer = solve(self.eq1, y)[0]
            self.format_answer = f'\({latex(self.eq1)}\)'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
{self.prompt_single}
{self.format_given}
"""

    name = 'Solve By Elimination'
    module_name = 'solve_by_elimination'

    prompt_single = """Give a simple description of the set of all pairs
    that satisfy this system."""
    prompt_multiple = """TBA"""

    further_instruction = """
If the solution is a
single pair&mdash;such as \((2, -3)\)
either enter it as an ordered pair or enter
"x = 2, y = -3".  If the solution is an infinite set lying along
a line, give an equation for that line.  If there is no solution,
type "no solution".
"""


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'



    # has_img = True
    #
    # def save_img(self, filename):
    #     if self.orientation == 'vert':
    #         graph = GraphVert(self.value)
    #     else:
    #         graph = GraphHoriz(self.value)
    #     graph.save_fig(filename)

    # def get_svg_data(self, xwindow=[-10,10], ywindow=[-10,10]):
    #     x_min, x_max = xwindow
    #     y_min, y_max = ywindow
    #     if self.orientation == 'vert':
    #         x_points = np.array([self.value, self.value])
    #         y_points = np.array([y_min, y_max])
    #     else:
    #         x_points = np.array([x_min, x_max])
    #         y_points = np.array([self.value, self.value])
    #     x_points = cart_x_to_svg(x_points)
    #     y_points = cart_y_to_svg(y_points)
    #     poly_points = ""
    #     l = len(x_points)
    #     i = 0
    #     while i < l:
    #         poly_points += f"{x_points[i]},{y_points[i]} "
    #         i += 1
    #     return poly_points


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        if self.how_many == 0:
            if not user_answer.replace(' ', '').isalpha():
                return False
            else:
                if 'no ' in user_answer or 'null' in user_answer or 'empty' in user_answer:
                    return True
        else:
            if user_answer.replace(' ', '').isalpha():
                return False
        user_answer = user_answer.replace('^', '**')
        user_answer = user_answer.replace(' ', '')
        if self.how_many == 1:
            user_answer = user_answer.replace('(', '')
            user_answer = user_answer.replace(')', '')
            if ',' not in user_answer:
                return False
            user_answer = user_answer.replace(' ', '')
            user_x, user_y = user_answer.split(',')
            if 'y' in user_x:
                user_x, user_y = [user_y, user_x]
            if 'x' in user_x:
                i = user_x.find('x')
                user_x = user_x[i+1:]
                i = user_x.find('=')
                user_x = user_x[i+1:]
                user_x = user_x.replace(' ', '')
                user_x = parse_expr(user_x, transformations=transformations)
            else:
                user_x = user_x.replace(' ', '')
                user_x = parse_expr(user_x, transformations=transformations)
            if 'y' in user_y:
                i = user_y.find('y')
                user_y = user_y[i+1:]
                i = user_y.find('=')
                user_y = user_y[i+1:]
                user_y = user_y.replace(' ', '')
                user_y = parse_expr(user_y, transformations=transformations)
            else:
                user_y = user_y.replace(' ', '')
                user_y = parse_expr(user_y, transformations=transformations)
            return user_y == self.y_soln and user_x == self.x_soln
        if self.how_many == oo:
            if '=' not in user_answer:
                return False
            if user_answer.count('=') > 1:
                return False
            y = Symbol('y')
            answer = solve(self.eq1, y)[0]
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
            user_answer = solve(user_answer, y)[0]
            return self.answer.equals(user_answer)


    def format_useranswer(self, user_answer, display=False):
        # user_answer = user_answer.lower()
        if user_answer.replace(' ', '').isalpha():
            return user_answer
        else:
            return f'\({user_answer}\)'
        # user_answer = user_answer.lower()
        # if self.how_many == 0:
        #     return user_answer
        # user_answer = user_answer.replace('^', '**')
        # if self.how_many == 1:
        #     user_answer = user_answer.replace('(', '')
        #     user_answer = user_answer.replace(')', '')
        #     if ',' not in user_answer:
        #         return user_answer
        #     user_answer = user_answer.replace(' ', '')
        #     user_x, user_y = user_answer.split(',')
        #     if 'y' in user_x:
        #         user_x, user_y = [user_y, user_x]
        #     if 'x' in user_x:
        #         i = user_x.find('x')
        #         user_x = user_x[i+1:]
        #         i = user_x.find('=')
        #         user_x = user_x[i+1:]
        #         user_x = user_x.replace(' ', '')
        #         user_x = parse_expr(user_x, transformations=transformations)
        #     else:
        #         user_x = user_x.replace(' ', '')
        #         user_x = parse_expr(user_x, transformations=transformations)
        #     if 'y' in user_y:
        #         i = user_y.find('y')
        #         user_y = user_y[i+1:]
        #         i = user_y.find('=')
        #         user_y = user_y[i+1:]
        #         user_y = user_y.replace(' ', '')
        #         user_y = parse_expr(user_y, transformations=transformations)
        #     else:
        #         user_y = user_y.replace(' ', '')
        #         user_y = parse_expr(user_y, transformations=transformations)
        #     return f'\(({latex(user_x)}, {latex(user_y)})\)'
        # if self.how_many == oo:
        #     if '=' not in user_answer:
        #         return user_answer
        #     if user_answer.count('=') > 1:
        #         return user_answer
        #     y = Symbol('y')
        #     answer = solve(self.eq1, y)[0]
        #     lhs, rhs = user_answer.split('=')
        #     lhs = parse_expr(lhs, transformations=transformations)
        #     rhs = parse_expr(rhs, transformations=transformations)
        #     user_answer = Eq(lhs, rhs)
        #     user_answer = solve(user_answer, y)[0]
        #     return f'\({latex(lhs)} = {latex(rhs)}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            if not user_answer.replace(' ', '').isalpha():
                user_answer = user_answer.replace(' ', '')
                if ',' not in user_answer:
                    if '=' not in user_answer:
                        raise SyntaxError
                    y = Symbol('y')
                    user_answer = user_answer.replace('^', '**')
                    lhs, rhs = user_answer.split('=')
                    lhs = parse_expr(lhs, transformations=transformations)
                    rhs = parse_expr(rhs, transformations=transformations)
                    user_answer = Eq(lhs, rhs)
                    user_answer = solve(user_answer, y)[0]
                else:
                    user_answer = user_answer.replace('(', '')
                    user_answer = user_answer.replace(')', '')
                    user_x, user_y = user_answer.split(',')
                    if 'y' in user_x:
                        user_x, user_y = [user_y, user_x]
                    if 'x' in user_x:
                        i = user_x.find('x')
                        user_x = user_x[i+1:]
                        i = user_x.find('=')
                        user_x = user_x[i+1:]
                        user_x = user_x.replace(' ', '')
                        user_x = parse_expr(user_x, transformations=transformations)
                    else:
                        user_x = user_x.replace(' ', '')
                        user_x = parse_expr(user_x, transformations=transformations)
                    if 'y' in user_y:
                        i = user_y.find('y')
                        user_y = user_y[i+1:]
                        i = user_y.find('=')
                        user_y = user_y[i+1:]
                        user_y = user_y.replace(' ', '')
                        user_y = parse_expr(user_y, transformations=transformations)
                    else:
                        user_y = user_y.replace(' ', '')
                        user_y = parse_expr(user_y, transformations=transformations)
        except:
            raise SyntaxError



Question_Class = SolveBySubstitution
