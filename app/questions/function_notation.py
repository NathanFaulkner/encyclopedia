#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from flask_wtf import FlaskForm
# from wtforms import SubmitField, StringField, HiddenField
# from wtforms.validators import DataRequired, ValidationError, Email, \
#                 EqualTo, Length, InputRequired

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *
import numpy as np
import json

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation,
                            RandomLinearFunction,
                            RandomVertexFormQuadratic,
                            RandomAbsValueFunction,
                            compose)
# from app.interpolator import cart_x_to_svg, cart_y_to_svg


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general

# class RealLineForm(FlaskForm):
#     points = HiddenField(id="points_field")
#     intervals = HiddenField(id="intervals_field")
#     submit = SubmitField('Submit')

# form = RealLineForm

prob_type = 'math_blank'




class FunctionNotation(Question):
    """
    The given is
    \\[
        f(x) = ...
    \\]
    and an input for a computation.
    f could be linear or simple transformation of x^2 or of |x|
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'symbol' in kwargs:
            self.symbol = kwargs['symbol']
        else:
            self.symbol = random.choice(['f', 'g', 'h'])
        if 'f' in kwargs:
            self.f = kwargs['f']
        else:
            self.function_type = random.choice(['linear', 'quadratic', 'abs_val'])
            if self.function_type == 'linear':
                self.f = RandomLinearFunction(seed=self.seed).f
            elif self.function_type == 'quadratic':
                a = random.choice([1, 1, -1])
                h = random.randint(-3,3)
                if h == 0:
                    k = random.randint(-5,5)
                else:
                    k = 0
                self.f = RandomVertexFormQuadratic(seed=self.seed, a=a, h=h, k=k).f
            else:
                self.f = RandomAbsValueFunction(seed=self.seed).f

        self.input = random.randint(-5,5)
        x = Symbol('x')
        self.prompt_single = f"""
        Let \({self.symbol}\) be the function given by the rule
        \[
            {self.symbol}(x) = {latex(self.f(x))}
        \]
        Compute the value of \({self.symbol}({self.input})\).
        """
        self.further_instruction = f"""Do NOT include "{self.symbol}({self.input})"
        in the statement of your answer."""
        self.answer = self.f(self.input)
        self.format_answer = f'\({self.answer}\)'

        self.format_given_for_tex = self.prompt_single

        # self.genproblem()

        # self.given_latex = latex_print(self.given)
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        # self.format_answer = self.answer
    prob_type = 'math_blank'

    name = 'Function Notation'
    module_name = 'function_notation'



    # loom_link = "https://www.loom.com/share/5028da702f8143568d2762e7a47d64db"


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'







    def checkanswer(self, user_answer):
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return float(self.answer) == float(user_answer)


    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return user_answer

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            float(user_answer)
        except:
            raise SyntaxError



Question_Class = FunctionNotation
