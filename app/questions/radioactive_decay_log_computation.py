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

class RadioactiveDecayLogComputation(Question):
    def __init__(self, **kwargs):
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
        radioisotope = random.choice(['c14', 'sr90', 'pol210', 'pol212', 'fr221', 'o22'])
        # radioisotope = 'pol212'
        if radioisotope == 'c14':
            halflife = 5730
            units = 'years'
            reg_time = ureg.year
            halflifewithunits = '5,730 years'
            symb = r'\(^{14}\,\)C'
            long_name = 'carbon-14'
            long_name_cap = 'Carbon-14'

        if radioisotope == 'sr90':
            halflife = 28.79
            units = 'years'
            reg_time = ureg.year
            halflifewithunits = '28.79 years'
            symb = r'\(^{90}\)Sr'
            long_name = 'strontium-90'
            long_name_cap = 'Strontium-90'

        if radioisotope == 'pol210':
            halflife = 138.376
            units = 'days'
            reg_time = ureg.day
            halflifewithunits = '138.376 days'
            symb = r'\(^{210}\)Po'
            long_name = 'polonium-210'
            long_name_cap = 'Polonium-210'

        if radioisotope == 'pol212':
            halflife = 299
            units = 'nanoseconds'
            reg_time = ureg.nanosecond
            halflifewithunits = '299 nanoseconds'
            symb = r'\(^{212}\)Po'
            long_name = 'polonium-212'
            long_name_cap = 'Polonium-212'

        if radioisotope == 'fr221':
            halflife = 4.8
            units = 'minutes'
            reg_time = ureg.minute
            halflifewithunits = '4.8 minutes'
            symb = r'\(^{221}\)Fr'
            long_name = 'francium-221'
            long_name_cap = 'Francium-221'

        if radioisotope == 'o22':
            halflife = 2.25
            units = 'seconds'
            reg_time = ureg.second
            halflifewithunits = '2.25 seconds'
            symb = r'\(^{22}\)O'
            long_name = 'oxygen-22'
            long_name_cap = 'Oxygen-22'
        howmuchstuff = random.randint(1,100)

        reduced = random.randint(1,int(0.75*howmuchstuff))
        self.time_unit = reg_time
        A = reduced
        A0 = howmuchstuff
        h = halflife
        # time_factor = random.randint(15,60)*0.1
        # how_long = round(time_factor*halflife, 2)
        t = sy.Symbol('t')
        self.format_given = ''
        self.answer = float((sy.log(A) - sy.log(A0))/sy.log(1/2)*halflife)
        self.format_answer = '\\({ans:.4f}\\) {time_unit}'.format(ans=self.answer, time_unit=inflector.plural(str(self.time_unit)))
        self.prompt_single = """{long_name_cap} ({symb}) is a radioisotope with a half life of {halflifewithunits}.
            Find out how many {units} it will take {howmuchstuff}
            grams of {symb} to decay leaving only {reduced} grams left.
            Use your calculator
            to obtain a numerical answer accurate to two decimal places.
            """.format(long_name_cap=long_name_cap,
                        symb=symb, reduced=reduced,
                        halflifewithunits=halflifewithunits,
                        units=units,howmuchstuff=howmuchstuff)
        self.format_given_for_tex = """{long_name_cap} ({symb}) is a radioisotope with a half life of {halflifewithunits}.
            The formula for radioactive decay is
            \\(A = A_0\\left(\\frac{{1}}{{2}}\\right)^{{\\frac{{t}}{{h}} }}\\).
            Find out how many {units} it will take {howmuchstuff}
            grams of {symb} to decay leaving only {reduced} grams left.
            {{\\color{{red}}(a)}} Write your answer
            in terms of a logarithm before {{\\color{{blue}}(b)}} also using your calculator
            to obtain a numerical answer accurate to two decimal places.
            Give the units of your answer.
            """.format(long_name_cap=long_name_cap,
                        symb=symb, reduced=reduced,
                        halflifewithunits=halflifewithunits,
                        units=units,howmuchstuff=howmuchstuff)

        self.prompt_multiple = f"""TBA"""

    prob_type = 'math_blank'

    name = 'Radioactive Decay: Log Computation Problem'
    module_name = 'radioactive_decay_log_computation'


    further_instruction = """Round your answer to at least 4 decimal places, and don't forget to include units.
    The answer checker will give a syntax error if you forget your units.  Also, don't write "y = " or
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
    """

    # loom_link = "https://www.loom.com/share/8ff321d4b7434dc5b42f2536a9129132"

    def checkunits(self, user_units):
        user_units = user_units.replace('.', ' ')
        user_units = user_units.lower()
        long_format = inflector.plural(str(self.time_unit))
        abbrev = '{:~}'.format(self.time_unit)
        peculiar = str(self.time_unit)
        abbrev_plural = abbrev + 's'
        allowed = [long_format, abbrev, peculiar, abbrev_plural]
        # print(allowed)
        return user_units in allowed

    def checkanswer(self, user_answer):
        # user_answer = user_answer.lower()
        # user_answer = user_answer.replace('y ', '')
        # user_answer = user_answer.replace('y=', '')
        # user_answer = user_answer.replace('a ', '')
        # user_answer = user_answer.replace('a=', '')
        # user_answer = user_answer.replace('=', '')
        user_answer = user_answer.strip()
        # print(user_answer)
        if not user_answer[-1].isalpha():
            # print('my fault!')
            user_units = ''
        else:
            i = -1
            while user_answer[i].isalpha():
                i += -1
            user_units = user_answer[i:].strip()
            user_answer = user_answer[:i]
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        # print(user_answer, user_units)
        # print(abs(user_answer - self.answer) < 0.0005)
        # print(self.checkunits(user_units))
        return abs(user_answer - self.answer) < 0.005 and self.checkunits(user_units)

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
            user_answer = user_answer.strip()
            # print(user_answer)
            if not user_answer[-1].isalpha():
                # print('my fault!')
                raise SyntaxError
            else:
                i = -1
                while user_answer[i].isalpha():
                    i += -1
                user_units = user_answer[i:]
                user_answer = user_answer[:i]
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            # print(user_answer, user_units)
            bool(abs(user_answer - 1) < 0.0005)
            abs(user_answer - 1) < 0.0005
        except:
            raise SyntaxError

Question_Class = RadioactiveDecayLogComputation
