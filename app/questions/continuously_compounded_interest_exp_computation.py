#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy
# import numpy as np
# import json
from pint import UnitRegistry
import inflect

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation,
                            tolerates,
                            )
# from app.interpolator import cart_x_to_svg, cart_y_to_svg

ureg = UnitRegistry()
#
inflector = inflect.engine()

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




# class Plant():
#     def __init__(self, name, growth_rate, height_unit, time_unit):
#         self.name = name
#         self.growth_rate = growth_rate
#         self.height_unit = height_unit
#         self.time_unit = time_unit
#         self.growth_rate_with_units = growth_rate * height_unit / time_unit
#
#
#
#
# bamboo = Plant('bamboo', 2, ureg.foot, ureg.day)
# sunflower = Plant('sunflower', 9, ureg.inch, ureg.month)
# corn = Plant('corn', 1, ureg.inch, ureg.day)
# kudzu = Plant('kudzu', 1, ureg.foot, ureg.day)

class ContinuouslyCompoundedInterestExpComputation(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        P = random.randint(1,100)*1000
        r_pct = random.randint(50,700)*0.01
        scheme = 'continuously'
        self.scheme = scheme
        how_long = random.randint(1,20)
        self.format_given = ''
        self.prompt_single = """
                Say that you invest \\${P:,} at {r_pct}\\% annual interest, compounded
                {scheme}.  Find out how much
                you'll have in your account after {how_long} years.
                """.format(P=P, r_pct=r_pct, scheme=scheme, how_long=how_long)
        self.answer = P*sy.E**(round(r_pct/100,4)*how_long)
        # self.answer = parse_expr(answer, transformations=transformations)
        # if scheme == 'daily':
        #     self.alt_answer = P*(1+round(r_pct/100, 4)/365)**(365*how_long)
        # self.alt_answer = parse_expr(alt_answer, transformations=transformations)
        # self.answer = parse_expr(str(P*(1+r_pct/100/n)**(n*t)), transformations=transformations)
        # self.format_answer = f'\(A = {P}\\left(1+\\frac{{  {round(r_pct/100, 4)} }}{{ {n} }}\\right)^{{ {n}t }}\)'
        self.format_answer = '\\(\\${ans:.2f}\\)'.format(ans=self.answer)
        self.format_given_for_tex = '''\\noindent
                Say that you invest \\${P:,} at {r_pct}\\% annual interest, compounded
                {scheme}.  {{\\color{{red}}(a)}} Write a formula for \\(A(t)\\), the amount in your
                account after \\(t\\) years.  {{\\color{{blue}}(b)}} Find out how much
                you'll have in your account after {how_long} years.

        \\noindent
        Reminder: the formula for an investment value growing under continuously compounded interest is
        \\[
        A(t) = P e^{{rt}}
        \\]
                '''.format(P=P, r_pct=r_pct, scheme=scheme, how_long=how_long)

        self.prompt_multiple = f"""TBA"""

    prob_type = 'math_blank'

    name = 'Continuously Compounded Interest: Exponential Computation Problem'
    module_name = 'continuously_compounded_interest_exp_computation'


    further_instruction = """Just give the numerical value.  You may round to 2 decimal places. """

    # loom_link = "https://www.loom.com/share/8ff321d4b7434dc5b42f2536a9129132"

    # def checkunits(self, user_units):
    #     user_units = user_units.replace('.', ' ')
    #     user_units = user_units.lower()
    #     long_format = inflector.plural(str(self.mass_unit))
    #     abbrev = '{:~}'.format(self.mass_unit)
    #     peculiar = str(self.mass_unit)
    #     abbrev_plural = abbrev + 's'
    #     allowed = [long_format, abbrev, peculiar, abbrev_plural]
    #     # print(allowed)
    #     return user_units in allowed

    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('$', '')
        user_answer = user_answer.replace(',', '')
        user_answer = user_answer.replace('dollars', '')
        user_answer = user_answer.replace('dollar', '')
        # user_answer = user_answer.replace('y ', '')
        # user_answer = user_answer.replace('y=', '')
        # user_answer = user_answer.replace('a ', '')
        # user_answer = user_answer.replace('a=', '')
        # user_answer = user_answer.replace('=', '')
        # if len(user_answer.split(' ')) == 1:
        #     return false
        # else:
        #     user_answer, user_units = user_answer.split(' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        user_answer = user_answer.subs(sy.Symbol('e'), sy.E)
        return abs(user_answer - self.answer) < 0.005 #and self.checkunits(user_units)

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('$', '')
        user_answer = user_answer.replace(',', '')
        user_answer = user_answer.replace('dollars', '')
        user_answer = user_answer.replace('dollar', '')
        if len(user_answer.split(' ')) == 1:
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            user_answer = user_answer.subs(sy.Symbol('e'), sy.E)
            return f'\({user_answer}\)'
        else:
            user_answer, user_units = user_answer.split(' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            user_answer = user_answer.subs(sy.Symbol('e'), sy.E)
            return f'\({sy.latex(user_answer)}\) {user_units}'

    @staticmethod
    def validator(user_answer):
        try:
            # pass
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('$', '')
            user_answer = user_answer.replace(',', '')
            user_answer = user_answer.replace('dollars', '')
            user_answer = user_answer.replace('dollar', '')
            if len(user_answer.split(' ')) == 1:
                print('My fault!')
                user_answer = user_answer.replace('^', '**')
                user_answer = parse_expr(user_answer, transformations=transformations)
                user_answer = user_answer.subs(sy.Symbol('e'), sy.E)
                # return f'\({user_answer}\)'
            else:
                user_answer, user_units = user_answer.split(' ')
                user_answer = user_answer.replace('^', '**')
                user_answer = parse_expr(user_answer, transformations=transformations)
                user_answer = user_answer.subs(sy.Symbol('e'), sy.E)
            sy.latex(user_answer)
            # return f'\({sy.latex(user_answer)}\) {user_units}'
            abs(user_answer) < 0.005
        except:
            raise SyntaxError

Question_Class = ContinuouslyCompoundedInterestExpComputation
