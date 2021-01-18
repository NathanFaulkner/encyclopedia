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
                            fmt_slope_style_leading,
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

class ImaginaryElementLevel3(Question):
    """
        outer_sign(sign i)^p
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)

        i = sy.Symbol('i')
        a = random_non_zero_integer(-9,9)
        b = random_non_zero_integer(-9,9)
        inner_term = a + b*i
        if b > 0:
            if b == 1:
                disp_b = '+'
            else:
                disp_b = '+ ' + sy.latex(b)
        else:
            if b == -1:
                disp_b = '-'
            else:
                disp_b = sy.latex(b)
        disp_inner_term = sy.latex(a) + ' ' + disp_b + sy.latex(i)

        c = random_non_zero_integer(-9,9)
        outer_term = c*i


        self.prompt_single = f"""
        Simplify the following expression by using all the usual rules
        of arithmetic together with the added rule that \(i^2 = -1\).
        """
        self.format_given = f'\\[{fmt_slope_style_leading(outer_term)}\\left({disp_inner_term}\\right)\\]'

        # self.further_instruction = f"""Only give a numerical answer (no letter symbols)."""
        expr = outer_term*(inner_term)
        self.answer = sy.simplify(expr.subs(i, sy.I))
        # print(self.answer)
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

    name = 'Imaginary Element, Level 3'
    module_name = 'imaginary_element_level3'



    # loom_link = "https://www.loom.com/share/5028da702f8143568d2762e7a47d64db"


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'







    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        # user_answer = user_answer.subs(sy.Symbol('i'), sy.I)
        # print(self.answer, str(self.answer).replace('I', 'i'))
        answer = parse_expr(str(self.answer).replace('I', 'i'))
        return answer == user_answer

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('=', ' ')
        user_answer = user_answer.replace('^', '**')
        # user_answer = user_answer.replace('i', 'I')
        user_answer = parse_expr(user_answer, transformations=transformations)
        # user_answer = user_answer.subs(sy.Symbol('i'), sy.I)
        return f'\({sy.latex(user_answer)}\)'

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            # user_answer = user_answer.replace('i', 'I')
            user_answer = parse_expr(user_answer, transformations=transformations)
            # user_answer = user_answer.subs(sy.Symbol('i'), sy.I)
        except:
            raise SyntaxError



Question_Class = ImaginaryElementLevel3
