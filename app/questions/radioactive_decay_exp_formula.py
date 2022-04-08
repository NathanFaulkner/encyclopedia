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

class RadioactiveDecayExpFormula(Question):
    def __init__(self, **kwargs):
        print('new decay formula problem')
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'type' in kwargs:
            self.type = kwargs['type']
        else:
            self.type = random.choice(['formula', 'value'])
        if 'mass_unit' in kwargs:
            self.mass_unit = kwargs['mass_unit']
        else:
            self.mass_unit = random.choice([ureg.gram, ureg.ounce, ureg.kg, ureg.pound])
        radioisotope = random.choice(['c14', 'sr90', 'pol210', 'fr221', 'o22'])
        #radioisotope = 'sr90'
        if radioisotope == 'c14':
        	halflife = 5730
        	units = 'years'
        	halflifewithunits = '5,730 years'
        	symb = r'\(^{14}\,\)C'
        	long_name = 'carbon-14'
        	long_name_cap = 'Carbon-14'

        if radioisotope == 'sr90':
        	halflife = 28.79
        	units = 'years'
        	halflifewithunits = '28.79 years'
        	symb = r'\(^{90}\)Sr'
        	long_name = 'strontium-90'
        	long_name_cap = 'Strontium-90'

        if radioisotope == 'pol210':
        	halflife = 138.376
        	units = 'days'
        	halflifewithunits = '138.376 days'
        	symb = r'\(^{210}\)Po'
        	long_name = 'polonium-210'
        	long_name_cap = 'Polonium-210'

        if radioisotope == 'pol212':
        	halflife = 299
        	units = 'nanoseconds'
        	halflifewithunits = '299 nanoseconds'
        	symb = r'\(^{212}\)Po'
        	long_name = 'polonium-212'
        	long_name_cap = 'Polonium-212'

        if radioisotope == 'fr221':
        	halflife = 4.8
        	units = 'minutes'
        	halflifewithunits = '4.8 minutes'
        	symb = r'\(^{221}\)Fr'
        	long_name = 'francium-221'
        	long_name_cap = 'Francium-221'

        if radioisotope == 'o22':
        	halflife = 2.25
        	units = 'seconds'
        	halflifewithunits = '2.25 seconds'
        	symb = r'\(^{22}\)O'
        	long_name = 'oxygen-22'
        	long_name_cap = 'Oxygen-22'
        howmuchstuff = random.randint(1,100)

        reduced = random.randint(1,int(0.75*howmuchstuff))

        A = reduced
        A0 = howmuchstuff
        h = halflife
        time_factor = random.randint(15,60)*0.1
        how_long = time_factor*halflife
        t = sy.Symbol('t')
        self.format_given = ''
        self.prompt_single = f"""
            {long_name_cap} ({symb}) is a radioisotope with a half life of {halflifewithunits}.
            Write down a formula for the
            (predicted) number \\(A\\) of {inflector.plural(str(self.mass_unit))}
            you'll have after \\(t\\) {units},
            if you start with {howmuchstuff} {inflector.plural(str(self.mass_unit))}.
            """#.format(long_name_cap=long_name_cap,
            # symb=symb, reduced=reduced,
            # halflifewithunits=halflifewithunits,
            # units=units,
            # howmuchstuff=howmuchstuff,
            # how_long=how_long)
        answer = f'{A0}(1/2)**(t/{h})'
        self.answer = parse_expr(answer, transformations=transformations)
        self.format_answer = f'\(A = {A0}\\left(\\frac{{1}}{{2}}\\right)^{{ \\frac{{ {t} }}{{ {h} }} }}\)'
        self.format_given_for_tex = f"""\\noindent
            {long_name_cap} ({symb}) is a radioisotope with a half life of {halflifewithunits}.
            The formula for radioactive decay is
            \\(A = A_0\\left(\\frac{{1}}{{2}}\\right)^{{\\frac{{t}}{{h}} }}\\).

            \\noindent
            {{\\color{{red}}(a)}} Write down a formula for the
            (predicted) number of {inflector.plural(str(self.mass_unit))}
            you'll have after \(t\) {units},
            if you start with {howmuchstuff} {inflector.plural(str(self.mass_unit))}.
            \\vspace{{5\\baselineskip}}

            \\noindent
            {{\\color{{blue}}(b)}}
            Find out how much {symb} will remain after {how_long} {units}.
            """#.format(long_name_cap=long_name_cap,
            # symb=symb, reduced=reduced,
            # halflifewithunits=halflifewithunits,
            # units=units,
            # howmuchstuff=howmuchstuff,
            # how_long=how_long)

        self.prompt_multiple = f"""TBA"""

    prob_type = 'math_blank'

    name = 'Radioactive Decay: Exponential Formula Problem'
    module_name = 'radioactive_decay_exp_formula'


    further_instruction = """Do not write "A(t)".  Just write your formula as "A = ...". """

    # loom_link = "https://www.loom.com/share/8ff321d4b7434dc5b42f2536a9129132"

    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace(' ', '')
        user_answer = user_answer.replace('y', 'a')
        user_answer = user_answer.replace('x', 't')
        if 'a' not in user_answer:
            return False
        if 't' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        user_answer = user_answer.replace('a=', '')
        user_answer = parse_expr(user_answer, transformations=transformations)
        # return sy.simplify(user_answer - self.answer) == 0
        print(user_answer, self.answer)
        return user_answer.equals(self.answer)
        # print('user traversal')
        # for arg in sy.preorder_traversal(user_answer):
        #     print(f'{arg}, {type(arg)}')
        # print('ans traversal')
        # for arg in sy.preorder_traversal(self.answer):
        #     print(f'{arg}, {type(arg)}')
        # return sy.simplify(user_answer - self.answer) == 0
        # user_answer = sy.lambdify(sy.Symbol('t'), user_answer)
        # answer = sy.lambdify(sy.Symbol('t'), self.answer)
        # print(answer, user_answer)
        # return tolerates(answer, user_answer, tolerance=0.000000000000005)

    @staticmethod
    def format_useranswer(user_answer, display=False):
        # user_answer = user_answer.lower()
        user_answer = user_answer.replace('y', 'a')
        user_answer = user_answer.replace('x', 't')
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations, evaluate=False)
        rhs = parse_expr(rhs, transformations=transformations, evaluate=False)
        # user_answer = sy.Eq(lhs, rhs)
        # A = sy.Symbol('a')
        # user_answer = sy.solve(user_answer, A)[0]
        return f'\\({sy.latex(lhs)} = {sy.latex(rhs)}\\)'

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace(' ', '')
            user_answer = user_answer.replace('y', 'a')
            if 'a' not in user_answer:
                raise SyntaxError
            user_answer = user_answer.replace('x', 't')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('a=', '')
            user_answer = parse_expr(user_answer, transformations=transformations)
            # return sy.simplify(user_answer - self.answer) == 0
            # print(user_answer, self.answer)
            user_answer.equals(sy.Symbol('t'))
        except:
            raise SyntaxError

Question_Class = RadioactiveDecayExpFormula
