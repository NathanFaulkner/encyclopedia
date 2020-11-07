#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import collections
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

def two_zeros_in_(row):
    return collections.Counter(row)[0] > 1

def two_zeros_in_some_row(A):
    rows = [A.row(i) for i in range(A.rows)]
    for row in rows:
        if two_zeros_in_(row):
            return True
    return False

class SolveByEliminationThree(Question):
    """
    System of 3 equations in 3 unknowns with a single solution.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        # if 'how_many' in kwargs:
        #     self.how_many = kwargs['how_many']
        # else:
        #     self.how_many = random.choice([0, 1, 1, 1, 1, oo])
        self.x_soln = random.randint(-5,5)
        self.y_soln = random.randint(-5,5)
        self.z_soln = random.randint(-5,5)
        A = zeros(3,3)
        rows = []
        for i in range(3):
            row = [random.randint(-5,5) for i in range(3)]
            rows.append(row)
        A = Matrix(rows)
        while A.det() == 0 or two_zeros_in_some_row(A):
            rows = []
            for i in range(3):
                row = [random.randint(-5,5) for i in range(3)]
                rows.append(row)
            A = Matrix(rows)
        self.A = A

        # if self.how_many == 1:
        #     while self.a*d - self.b*c == 0:
        #     	d = random_non_zero_integer(-10,10)
        #     self.c = c
        #     self.d = d
        #     self.e0 = self.a*self.x_soln + self.b*self.y_soln
        #     self.e1 = self.c*self.x_soln + self.d*self.y_soln
        # else:
        #     factor = random.choice([-5, -4, -3, -2, -1, 2, 3, 4, 5])
        #     self.c = factor*self.a
        #     self.d = factor*self.b
        #     self.e0 = self.a*self.x_soln + self.b*self.y_soln
        #     e1 = random.randint(-10,10)
        #     if self.how_many == 0:
        #         while e1 == factor*self.e0:
        #             e1 = random.randint(-10,10)
        #     else:
        #         e1 = factor*self.e0
        #     self.e1 = e1

        x, y, z = symbols('x y z')

        eqs = []
        es = []
        for i in range(3):
            a, b, c = self.A.row(i)
            e = a*self.x_soln + b*self.y_soln + c*self.z_soln
            es.append(e)
            eqs.append(Eq(a*x + b*y + c*z, e))


        self.format_given = f"""
        \\[
            \\begin{{cases}}
                {latex(eqs[0])}\\\\
                {latex(eqs[1])}\\\\
                {latex(eqs[2])}\\\\
            \\end{{cases}}
        \\]
        """
        # if self.how_many == 0:
        #     self.format_answer = 'No solution'
        # elif self.how_many == 1:
        self.format_answer = f'\(x = {self.x_soln}, y = {self.y_soln}, z={self.z_soln}\)'
        # else:
        #     self.answer = solve(self.eq1, y)[0]
        #     self.format_answer = f'\({latex(self.eq1)}\)'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)
        print(self.format_answer)

        self.format_given_for_tex = f"""
{self.prompt_single}
{self.format_given}
Use any method you like as you solve the entire system \\textbf{{by hand}}!
(Show all your work.)
"""

    name = 'Solve By Elimination: Three Equations, One Solution'
    module_name = 'solve_by_elimination_three'

    prompt_single = """Give a simple description of the set of all triples, \((x, y, z)\)
    that satisfy this system."""
    prompt_multiple = """TBA"""

    further_instruction = """
If the solution is a
single triple&mdash;such as \((2, -3, 1)\)
either enter it as an ordered triple or enter
"x = 2, y = -3, z = 1".
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
        user_answer = user_answer.replace('^', '**')
        user_answer = user_answer.replace(' ', '')
        user_answer = user_answer.replace('(', '')
        user_answer = user_answer.replace(')', '')
        if ',' not in user_answer:
            return False
        user_answer = user_answer.replace(' ', '')
        answers = user_answer.split(',')
        i = 0
        user_answers = [None, None, None]
        for answer in answers:
            if 'x' in answer:
                i = answer.find('x')
                user_x = answer[i+2:]
                user_x = parse_expr(user_x, transformations=transformations)
                user_answers[0] = user_x
            elif 'y' in answer:
                i = answer.find('y')
                user_y = answer[i+2:]
                user_y = parse_expr(user_y, transformations=transformations)
                user_answers[1] = user_y
            elif 'z' in answer:
                i = answer.find('z')
                user_z = answer[i+2:]
                user_z = parse_expr(user_z, transformations=transformations)
                user_answers[2] = user_z
            else:
                user_answers[i] = parse_expr(answer, transformations=transformations)
            i += 1

            # for x in ['x', 'y', 'z']:
            #     exec(f'user_{x} = parse_expr(user_{x}, transformations=transformations)')

            # print(user_x, user_y, user_z)
            # print(type(user_x), type(self.x_soln))
        return user_answers == [self.x_soln, self.y_soln, self.z_soln]


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
            pass
            # user_answer = user_answer.lower()
            # user_answer = user_answer.replace('^', '**')
            # user_answer = user_answer.replace(' ', '')
            # user_answer = user_answer.replace('(', '')
            # user_answer = user_answer.replace(')', '')
            # if ',' not in user_answer:
            #     raise SyntaxError
            # user_answer = user_answer.replace(' ', '')
            # if 'x' in user_answer:
            #     i = user_x.find('x')
            #     user_x = user_x[i+1:]
            #     i = user_x.find(',')
            #     user_x = user_x[1:i]
            #     user_x = parse_expr(user_x, transformations=transformations)
            # if 'y' in user_answer:
            #     i = user_y.find('y')
            #     user_y = user_y[i+1:]
            #     i = user_y.find(',')
            #     user_y = user_y[1:i]
            #     user_y = parse_expr(user_y, transformations=transformations)
            # if 'z' in user_answer:
            #     i = user_z.find('z')
            #     user_z = user_z[i+1:]
            #     i = user_z.find(',')
            #     user_z = user_z[1:i]
            #     user_z = parse_expr(user_z, transformations=transformations)
            # else:
            #     user_x, user_y, user_z = user_answer.split(',')
            #     user_x = parse_expr(user_x, transformations=transformations)
            #     user_y = parse_expr(user_y, transformations=transformations)
            #     user_z = parse_expr(user_z, transformations=transformations)
        except:
            raise SyntaxError



Question_Class = SolveByEliminationThree
