#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy
# import numpy as np
# import json
# from pint import UnitRegistry
# import inflect

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation)
# from app.interpolator import cart_x_to_svg, cart_y_to_svg

# ureg = UnitRegistry()
#
# inflector = inflect.engine()

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




class Plant():
    def __init__(self, name, growth_rate, height_unit, time_unit):
        self.name = name
        self.growth_rate = growth_rate
        self.height_unit = height_unit
        self.time_unit = time_unit
        self.growth_rate_with_units = growth_rate * height_unit / time_unit




bamboo = Plant('bamboo', 2, ureg.foot, ureg.day)
sunflower = Plant('sunflower', 9, ureg.inch, ureg.month)
corn = Plant('corn', 1, ureg.inch, ureg.day)
kudzu = Plant('kudzu', 1, ureg.foot, ureg.day)

class RadioactiveDecayExpProblem(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        radioisotope = random.choice(['c14', 'sr90', 'pol210', 'fr221', 'o22'])
        #radioisotope = 'sr90'
        if radioisotope == 'c14':
        	halflife = 5730
        	units = 'years'
        	halflifewithunits = '5,370 years'
        	symb = r'$^{14}\,$C'
        	long_name = 'carbon-14'
        	long_name_cap = 'Carbon-14'

        if radioisotope == 'sr90':
        	halflife = 28.79
        	units = 'years'
        	halflifewithunits = '28.79 years'
        	symb = r'$^{90}$Sr'
        	long_name = 'strontium-90'
        	long_name_cap = 'Strontium-90'

        if radioisotope == 'pol210':
        	halflife = 138.376
        	units = 'days'
        	halflifewithunits = '138.376 days'
        	symb = r'$^{210}$Po'
        	long_name = 'polonium-210'
        	long_name_cap = 'Polonium-210'

        if radioisotope == 'pol212':
        	halflife = 299
        	units = 'nanoseconds'
        	halflifewithunits = '299 nanoseconds'
        	symb = r'$^{212}$Po'
        	long_name = 'polonium-212'
        	long_name_cap = 'Polonium-212'

        if radioisotope == 'fr221':
        	halflife = 4.8
        	units = 'minutes'
        	halflifewithunits = '4.8 minutes'
        	symb = r'$^{221}$Fr'
        	long_name = 'francium-221'
        	long_name_cap = 'Francium-221'

        if radioisotope == 'o22':
        	halflife = 2.25
        	units = 'seconds'
        	halflifewithunits = '2.25 seconds'
        	symb = r'$^{22}$O'
        	long_name = 'oxygen-22'
        	long_name_cap = 'Oxygen-22'
        howmuchstuff = random.randint(1,100)

        reduced = random.randint(1,int(0.75*howmuchstuff))

        A = reduced
        A0 = howmuchstuff
        h = halflife
        time_factor = random.randint(15,60)*0.1
        how_long = time_factor*halflife
        if kwargs.get('check'):
            out = """\\noindent
                {long_name_cap} ({symb}) is a radioisotope with a half life of {halflifewithunits}.
                The formula for radioactive decay is
                \\(A = A_0\\left(\\frac{{1}}{{2}}\\right)^{{\\sfrac{{t}}{{h}} }}\\).

                \\noindent
                {{\\color{{red}}(a)}} Write down a formula for the
                (predicted) number of grams
                you'll have after $t$ {units},
                if you start with {howmuchstuff} grams.
                \\vspace{{5\\baselineskip}}

                \\noindent
                {{\\color{{blue}}(b)}}
                Find out how much {symb} will remain after {how_long} {units}.
                """.format(long_name_cap=long_name_cap,
                symb=symb, reduced=reduced,
                halflifewithunits=halflifewithunits,
                units=units,
                howmuchstuff=howmuchstuff,
                how_long=how_long)
        else:
            out = """{long_name_cap} ({symb}) is a radioisotope with a half life of {halflifewithunits}.
                        {{\\color{{red}}(a)}} Write down a formula for the
                (predicted) number of grams
                you'll have after $t$ {units},
                if you start with {howmuchstuff} grams.
                {{\\color{{blue}}(b)}}
                Find out how much {symb} will remain after {how_long} {units}.
                """.format(long_name_cap=long_name_cap,
                symb=symb, reduced=reduced,
                halflifewithunits=halflifewithunits,
                units=units,
                howmuchstuff=howmuchstuff,
                how_long=how_long)
        x = Symbol('x')
        self.answer = self.m * x + self.b
        self.format_answer = f'\(h = {latex(self.answer)}\)'
        self.format_given = ''

        self.prompt_single = """\\noindent
            {long_name_cap} ({symb}) is a radioisotope with a half life of {halflifewithunits}.
            The formula for radioactive decay is
            \\(A = A_0\\left(\\frac{{1}}{{2}}\\right)^{{\\sfrac{{t}}{{h}} }}\\).

            \\noindent
            {{\\color{{red}}(a)}} Write down a formula for the
            (predicted) number of grams
            you'll have after $t$ {units},
            if you start with {howmuchstuff} grams.
            \\vspace{{5\\baselineskip}}

            \\noindent
            {{\\color{{blue}}(b)}}
            Find out how much {symb} will remain after {how_long} {units}.
            """.format(long_name_cap=long_name_cap,
            symb=symb, reduced=reduced,
            halflifewithunits=halflifewithunits,
            units=units,
            howmuchstuff=howmuchstuff,
            how_long=how_long)

        self.prompt_multiple = f"""TBA"""

    prob_type = 'math_blank'

    name = 'Plant Growth Problem'
    module_name = 'plant_problem'


    further_instruction = """Just enter the equation in a natural way.
    """

    loom_link = "https://www.loom.com/share/8ff321d4b7434dc5b42f2536a9129132"



        self.format_given_for_tex = f"""
The following table depicts the height of a {self.plant.name} plant
depending on the number of {inflector.plural(str(self.time_unit))} that it has
grown.
Develop an equation that relates the height of the plant
to the time that it has grown.  Use the letter \(h\) for
the height of the plant.  Use the letter \(x\) for the number
of {inflector.plural(str(self.time_unit))} that have gone by
since ``{str(self.time_unit).title()} 0''.
\\smallskip

\\begin{{center}}
{tabular}
\\end{{center}}
\\smallskip

"""

    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('y', 'h')
        user_answer = user_answer.replace('t', 'x')
        if 'h' not in user_answer:
            return False
        if 'x' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        h = Symbol('h')
        user_answer = solve(user_answer, h)[0]
        return self.answer.equals(user_answer)


    def format_useranswer(self, user_answer, display=False):
        if 'h' in user_answer:
            user_y = 'h'
        elif 'H' in user_answer:
            user_y = 'H'
        elif 'y' in user_answer:
            user_y = 'y'
        elif 'Y' in user_answer:
            user_y = 'Y'
        else:
            user_y = ''
        if 'x' in user_answer:
            user_x = 'x'
        elif 'X' in user_answer:
            user_x = 'X'
        elif 't' in user_answer:
            user_x = 't'
        elif 'T' in user_answer:
            user_x = 'T'
        else:
            user_x = ''
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('y', 'h')
        user_answer = user_answer.replace('t', 'x')
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        h = Symbol('h')
        user_answer = solve(user_answer, h)[0]
        return f'\({user_y} = {latex(user_answer)}\)'.replace('x', user_x)

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('y', 'h')
            user_answer = user_answer.replace('t', 'x')
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
            h = Symbol('h')
            user_answer = solve(user_answer, h)[0]
        except:
            raise SyntaxError






Question_Class = PlantProblem
