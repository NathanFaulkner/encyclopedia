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
import sympy as sy
import numpy as np
# import json

from app.questions import (Question,
                            # latex_print,
                            random_non_zero_integer,)
                            # permute_equation,
                            # RandomLinearFunction,
                            # RandomVertexFormQuadratic,
                            # RandomAbsValueFunction,
                            # compose)
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

class ImaginaryElementLevel2(Question):
    """
        outer_sign(sign i)^p
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'p' in kwargs:
            self.p = kwargs['p']
        else:
            # tens = int(random.triangular(0,10,2))
            # ones = random.randint(1, 10)
            # p = 10*tens + ones
            # while p < 2:
            #     ones = random.randint(1, 10)
            #     p = 10*tens + ones
            p = random.choice([2, 3])
            self.p = p
        if 'sign' in kwargs:
            self.sign = kwargs['sign']
        else:
            self.sign = random.choice([1, -1])
        if 'outer_sign' in kwargs:
            self.outer_sign = kwargs['outer_sign']
        else:
            self.outer_sign = random.choice([1, -1])
        if self.outer_sign == 1:
            self.outer_sign_symb = ''
        else:
            self.outer_sign_symb = '-'
        a = random.randint(2, 9)
        whether_sqrt = random.choice([True, False])
        # print('whether_sqrt', whether_sqrt)
        if a in [1, 4, 9]:
            whether_sqrt = False
        if whether_sqrt:
            a = sy.sqrt(a)
            fmt = f'i{sy.latex(a)}'
        else:
            fmt = f'{sy.latex(a)}i'

        self.prompt_single = f"""
        Simplify the following expression by using all the usual rules
        of arithmetic together with the added rule that \(i^2 = -1\).
        """
        if self.sign == -1:
            self.format_given = f'\\[{self.outer_sign_symb}\\left(-{fmt}\\right)^{{ {p} }}\\]'
        else:
            self.format_given = f'\\[{self.outer_sign_symb}\\left({fmt}\\right)^{{ {p} }}\\]'
        # self.further_instruction = f"""Only give a numerical answer (no letter symbols)."""

        self.answer = self.outer_sign*(self.sign*a*sy.I)**self.p
        self.format_answer = f'\({sy.latex(self.answer)}\)'

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

        # self.genproblem()

        # self.given_latex = latex_print(self.given)
        # self.answer_latex = latex_print(self.answer)
        # self.answer_latex_display = latex_print(self.answer, display=True)

        # self.format_answer = self.answer
    prob_type = 'math_blank'

    name = 'Imaginary Element, Level 2'
    module_name = 'imaginary_element_level2'



    loom_link = "https://www.loom.com/share/08b2f9ab974a42588693ce8ebc0f8604"


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'







    def checkanswer(self, user_answer):
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        # user_answer = user_answer.subs(sy.Symbol('i'), sy.I)
        # print(self.answer, str(self.answer).replace('I', 'i'))
        answer = parse_expr(str(self.answer).replace('I', 'i'))
        return answer == user_answer


    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        # user_answer = user_answer.replace('i', 'I')
        user_answer = parse_expr(user_answer, transformations=transformations)
        # user_answer = user_answer.subs(sy.Symbol('i'), sy.I)
        return f'\({sy.latex(user_answer)}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            # user_answer = user_answer.replace('i', 'I')
            user_answer = parse_expr(user_answer, transformations=transformations)
            # user_answer = user_answer.subs(sy.Symbol('i'), sy.I)
        except:
            raise SyntaxError



Question_Class = ImaginaryElementLevel2
