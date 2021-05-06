#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
# from sympy.parsing.sympy_parser import parse_expr
# from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
# transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy
import numpy as np
import json
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            GraphFromLambda,
                            fmt_slope_style,
                            commute_sum,
                            tolerates)
from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general



prob_type = 'graph'

class GraphHyperbola(Question):
    """
    The given is of the form

    \\[
        y = a/(x - x0) + y0
    \\]

    The student is expected to graph by plotting points including two anchors.
    """
    def __init__(self, **kwargs):
        if 'basic' in kwargs:
            self.basic = kwargs['basic']
        else:
            self.basic = False
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['a']
            a = self.a
        else:
            a = 1
        if 'x0' in kwargs:
            self.x0 = kwargs['x0']
            h = self.x0
        else:
            h = 0
        if 'y0' in kwargs:
            self.y0 = kwargs['y0']
            k = self.y0
        else:
            k = 0
        if not self.basic:
            while a == 1 and h == 0 and k == 0:
            	a = random.choice([-2,-1,-1,1,1,2,2])
            	h = random.randint(-5,5)
            	k = random.randint(-5,5)
        self.x0 = h
        self.y0 = k
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('x')
        x = self.x

        expr = a/(x-h) + k

        self.as_lambda = lambda x: a/(x - h) + k
        f = self.as_lambda
        self.given = a/(x-h) + k
        #print('3rd step: So far its ', expr)
        self.answer = f(x)


        # term = factor(self.m*(self.x - self.x0)**2)
        # if self.y0 > 0:
        #     fmt_y0 = latex(self.y0)
        #     sign = '+'
        # elif self.y0 == 0:
        #     fmt_y0 = ''
        #     sign = ''
        # else:
        #     fmt_y0 = latex(abs(self.y0))
        #     sign = '-'
        # # print(term)
        # if self.m == 1:
        #     fmt_m = ''
        # elif self.m == -1:
        #     fmt_m = '-'
        # else:
        #     fmt_m = latex(self.m)
        # try:
        self.format_given = f"""
        \\[
         y = {sy.latex(a/(x-h) + k)}
        \\]
        """
        # except IndexError:
        #     self.format_given = f"""
        #     \\[
        #      y = {latex(term)} {sign} {fmt_y0}
        #     \\]
        #     """




        self.format_answer = '\\quad\n'
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        self.format_given_for_tex = f"""
Sketch a graph of the given equation.  Make sure your graph is accurate throughout
the window.  It must also have two ``anchors'' and multiple points besides.
{self.format_given}

\\begin{{flushright}}
\\includegraphics[scale=0.6]{{../common_imgs/blank}}
\\end{{flushright}}
\\vspace{{-12\\baselineskip}}

"""

    name = 'Graph of Hyperbola'
    module_name = 'graph_hyperbola'

    prompt_single = """Graph the given equation by plotting the "anchors" of the
    graph plus multiple points besides."""
    prompt_multiple = """TBA."""

    loom_link = "https://www.loom.com/share/7e04eda1c32d4dad85cf099aceeed38a"


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    has_img_in_key = True

    def save_img(self, filename):
        # graph = GraphFromLambda(self.as_lambda)
        f = self.as_lambda
        color="blue"
        res=1001
        xwindow=[-10,10]
        ywindow=[-10,10]
        xmarker_delta=1
        ymarker_delta=1
        x_min = xwindow[0]
        x_max = xwindow[1]
        y_min = ywindow[0]
        y_max = ywindow[1]

        # x = np.arange(x_min,x_max + xmarker_delta,res)
        x_left = np.linspace(x_min, self.x0-(x_max-x_min)/res, res)
        y_left = self.as_lambda(x_left)
        x_right = np.linspace(self.x0+(x_max-x_min)/res, x_max, res)
        y_right = self.as_lambda(x_right)
        x = np.concatenate((x_left, x_right))
        y = np.concatenate((y_left, y_right))

        spacing = 1
        minorLocator = MultipleLocator(spacing)

        fig, ax = plt.subplots()

        ax.plot(x, y, color=color)

        fig.set_size_inches(6, 6)

        ax.axhline(y=0, color='k')
        ax.axvline(x=0, color='k')

        #ax.set_aspect('equal')
        ax.set_xticks(np.arange(x_min, x_max + xmarker_delta, xmarker_delta))
        ax.set_yticks(np.arange(y_min, y_max + ymarker_delta, ymarker_delta))

        # Turn on the minor TICKS, which are required for the minor GRID
        ax.minorticks_on()

        ax.yaxis.set_minor_locator(minorLocator)
        ax.xaxis.set_minor_locator(minorLocator)

        ax.grid(True, which='major')


        plt.axis([x_min,x_max,y_min, y_max])
        fig.savefig(f'{filename}.png', bbox_inches='tight')
        # graph.save_fig(filename)

    def get_svg_data(self, window=[-10,10], res=1001):
        x_min = window[0]
        x_max = window[1]
        x_left = np.linspace(x_min, self.x0-(x_max-x_min)/res, res)
        y_left = self.as_lambda(x_left)
        x_left = cart_x_to_svg(x_left)
        y_left = cart_y_to_svg(y_left)
        x_right = np.linspace(self.x0+(x_max-x_min)/res, x_max, res)
        y_right = self.as_lambda(x_right)
        x_right = cart_x_to_svg(x_right)
        y_right = cart_y_to_svg(y_right)
        poly_points = []
        current = ''
        l = len(x_left)
        i = 0
        while i < l:
            current += f"{x_left[i]},{y_left[i]} "
            i += 1
        poly_points.append(current)
        current = ''
        l = len(x_right)
        i = 0
        while i < l:
            current += f"{x_right[i]},{y_right[i]} "
            i += 1
        poly_points.append(current)
        # print('poly', poly_points[1])
        return {'piecewise': True, 'poly_points': poly_points}


    def checkanswer(self, user_answer):
        if type(user_answer) == type(5):
            return False
        # user_answer = user_answer(self.x)
        # return self.answer.equals(user_answer)
        return tolerates(sy.lambdify(self.x, self.answer), user_answer)
        # return tolerates(sy.lambdify(self.x, self.answer), lambdify(self.x, user_answer))

    # def useranswer_latex(self, user_answer, display=False):
    #     user_answer = user_answer.replace('^', '**')
    #     user_answer = parse_expr(user_answer, transformations=transformations)
    #     return latex_print(user_answer, display)

    # @classmethod
    # def validator(self, user_answer):
    #     try:
    #         user_answer = user_answer.replace('^', '**')
    #         user_answer = parse_expr(user_answer, transformations=transformations)
    #     except:
    #         raise SyntaxError



Question_Class = GraphHyperbola
