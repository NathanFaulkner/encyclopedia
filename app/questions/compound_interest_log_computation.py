#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from math import log10, floor
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
def round_to_n(x, n):
    return round(x, -int(floor(log10(abs(x))))+n-1)

class CompoundInterestLogFormula(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        compounding_info = {'quarterly': 4, 'monthly': 12, 'yearly': 1, 'biannually': 2, 'daily': 360, 'continuously': 1000000}
        schemes = compounding_info.keys()
        scheme = random.choice(list(schemes))
        self.scheme = scheme
        n = compounding_info[scheme]
        P = random.randint(1,100)*1000
        r_pct = round(random.randint(50,700)*0.01,2)
        r = round(r_pct/100, 4)
        t = random.randint(1,20) + random.random()
        n = compounding_info[scheme]
        how_much = int(round_to_n(P*(1+r_pct*0.01/n)**(n*t), 2))
        # t = sy.Symbol('t')
        self.format_given = ''
        self.prompt_single = '''Say that you invest \\${P:,} at {r_pct}% annual interest, compounded
                {scheme}.  How long will it take to earn \\${how_much:,}, assuming
                you don't make any withdrawals?
                '''.format(P=P, r_pct=r_pct, scheme=scheme, how_much=how_much)
        if scheme == 'continuously':
            self.answer = sy.log(how_much/P)/r
        else:
            self.answer = sy.log(how_much/P)/sy.log(1+r/n)/n
        # self.answer = parse_expr(answer, transformations=transformations)
        if scheme == 'daily':
            self.alt_answer = sy.log(how_much/P)/sy.log(1+r/365)/365
        # self.alt_answer = parse_expr(alt_answer, transformations=transformations)
        # self.answer = parse_expr(str(P*(1+r_pct/100/n)**(n*t)), transformations=transformations)
        # self.format_answer = f'\(A = {P}\\left(1+\\frac{{  {round(r_pct/100, 4)} }}{{ {n} }}\\right)^{{ {n}t }}\)'
        self.format_answer = '\\({ans:.2f}\\) years'.format(ans=self.answer)
        self.format_given_for_tex = '''Say that you invest \\${P:,} at {r_pct}\\% annual interest, compounded
                {scheme}.  How long will it take to earn \\${how_much:,}, assuming
                you don't make any withdrawals?  {{\\color{{red}}(a)}} Write your answer
                in terms of a logarithm before {{\\color{{blue}}(b)}} also using your calculator
                to obtain a numerical answer accurate to two decimal places.
                Give the units of your answer.
                '''.format(P=P, r_pct=r_pct, scheme=scheme, how_much=how_much)

        self.prompt_multiple = f"""TBA"""

    prob_type = 'math_blank'

    name = 'Compound Interest: Log Computation Problem'
    module_name = 'compound_interest_log_computation'


    further_instruction = """Just give the numerical value.  You may round to 2 decimal places.
        Also, don't write "y = " or
        "A = "; just enter the numerical part of your answer followed by a space and then the units.

        <p>
        The answer checker (based on SymPy) understands both the symbols
        'log' and 'ln' to mean 'ln'.
        To use a base \(b\) other than base \(e\) (ln) you must use the notation
        "log(x, b)" to represent \\(\\log_b(x)\\).  For instance, if your answer involves the term
        \[
            \\log_{\\frac{1}{2}}\\left(1.2345\\right)
        \]
        then you should enter
        <div class="center" style="text-align:center">
            log(1.2345, 1/2)
        </div>

        Do NOT use commas in a decimal to represent the thousands place.  For instance,
        instead of writing "1,000" just write "1000".
    """

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
        if '$' in user_answer or 'dollar' in user_answer:
            return False
        # user_answer = user_answer.replace(',', '')
        user_answer = user_answer.replace('years', '')
        user_answer = user_answer.replace('year', '')
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
        if self.scheme == 'daily':
            return abs(user_answer - self.answer) < 0.005  or abs(user_answer - self.alt_answer) < 0.005 #and self.checkunits(user_units)
        else:
            return abs(user_answer - self.answer) < 0.005 #and self.checkunits(user_units)

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.strip()
        # print(user_answer)
        if not user_answer[-1].isalpha():
            # print('my fault!')
            user_units = ''
        else:
            i = -1
            while user_answer[i].isalpha():
                i += -1
            user_units = user_answer[i:]
            user_answer = user_answer[:i]
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        print(user_answer, user_units)
        return f'\({float(user_answer)}\) {user_units}'

    @staticmethod
    def validator(user_answer):
        try:
            # pass
            # user_answer = user_answer.lower()
            # # user_answer = user_answer.replace(',', '')
            # user_answer = user_answer.replace('dollars', '')
            # user_answer = user_answer.replace('dollar', '')
            # if len(user_answer.split(' ')) == 1:
            #     print('My fault!')
            #     user_answer = user_answer.replace('^', '**')
            #     user_answer = parse_expr(user_answer, transformations=transformations)
            #     # return f'\({user_answer}\)'
            # else:
            #     user_answer, user_units = user_answer.split(' ')
            #     user_answer = user_answer.replace('^', '**')
            #     user_answer = parse_expr(user_answer, transformations=transformations)
            # sy.latex(user_answer)
            # # return f'\({sy.latex(user_answer)}\) {user_units}'
            user_answer = user_answer.strip()
            # print(user_answer)
            if not user_answer[-1].isalpha():
                # print('my fault!')
                user_units = ''
            else:
                i = -1
                while user_answer[i].isalpha():
                    i += -1
                user_units = user_answer[i:]
                user_answer = user_answer[:i]
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            print(user_answer, user_units)
            return f'\({float(user_answer)}\) {user_units}'
            abs(user_answer) < 0.005
        except:
            raise SyntaxError

Question_Class = CompoundInterestLogFormula
