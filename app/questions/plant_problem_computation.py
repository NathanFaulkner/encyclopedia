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
# import numpy as np
# import json
from pint import UnitRegistry
import inflect

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation)
# from app.interpolator import cart_x_to_svg, cart_y_to_svg

ureg = UnitRegistry()

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

class PlantProblemComputation(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'plant' in kwargs:
            self.plant = kwargs['plant']
        else:
            plants = [bamboo, corn, sunflower, kudzu]
            self.plant = random.choice(plants)
        if 'height_unit' in kwargs:
            self.height_unit = kwargs['height_unit']
        else:
            self.height_unit = random.choice([ureg.meter, ureg.foot, ureg.inch, ureg.yard])
        daily_growth = self.plant.growth_rate_with_units
        self.time_unit = self.plant.time_unit
        self.growth_rate = daily_growth.to(self.height_unit / self.time_unit).magnitude
        if 'b' in 'kwargs':
            self.b = kwargs['b']
        else:
            b = self.growth_rate * random.randint(1,5)
            self.b = round(b, 1)
        if 'm' in 'kwargs':
            self.m = kwargs['m']
        else:
            error = round(self.growth_rate * 0.2, 1)
            # print(error)
            error = random.randint(0, error*10)/10
            # print(error)
            m = self.growth_rate + error
            self.m = round(m, 1)
            # print(self.m)
        x = Symbol('x')
        self.formula = self.m * x + self.b
        self.input = random.randint(6,20)
        self.answer = self.formula.subs(x, self.input)
        self.format_answer = f'\({latex(self.answer)}\)' + ' {:~}'.format(self.height_unit)

        self.prompt_single = f"""
        The following table depicts the height of a {self.plant.name} plant
        depending on the number of {inflector.plural(str(self.time_unit))} that it has
        grown.
        Compute the height of the plant after
        <span style="color: red">
        {self.input} {inflector.plural(str(self.time_unit))}.
        </span>
        You must include units in your answer!
        """

        prompt_multiple = f"""For each of the following tables,
        compute the height of the plant after {self.input} {inflector.plural(str(self.time_unit))}.
        You must include units in your answer!
        """

        self.genproblem()

    prob_type = 'math_blank'

    name = 'Plant Growth Computation'
    module_name = 'plant_problem_computation'


    further_instruction = """You must include units in your answer AND the
    units must be separated from
    your answer by a space.
    """

    # loom_link = ""

    def genproblem(self):
        table_html = f"""
        <table border="1">
            <tr>
                <th>{str(self.time_unit).title()} Number</th>
        """
        for i in range(5):
            table_html += f"""<td style="text-align: center;">{i}</td>"""
        table_html += f"""
            </tr>
            <tr>
                <th>Height of {self.plant.name} (in {inflector.plural(str(self.height_unit))})</th>
        """
        for i in range(5):
            table_html += f"<td>{round(self.m * i + self.b, 1)}</td>"
        table_html += """
            </tr>
        </table>
        """
        self.table_html = table_html
        self.format_given = self.table_html

        tabular = "\\begin{tabular}{|l||"
        for i in range(5):
            tabular += 'c|'
        tabular += '}\n\\hline\n'
        tabular += f' {str(self.time_unit).title()} Number & '
        for i in range(5):
            tabular += f'{i} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n'
        tabular += f'Height of {self.plant.name} (in {inflector.plural(str(self.height_unit))}) & '
        for i in range(5):
            tabular += f'{round(self.m * i + self.b, 1)} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n\\end{tabular}'


        self.format_given_for_tex = f"""
The following table depicts the height of a {self.plant.name} plant
depending on the number of {inflector.plural(str(self.time_unit))} that it has
grown.
Compute the height of the plant after
{{\\color{{red}}
{self.input} {inflector.plural(str(self.time_unit))}.
}}
You must include units in your answer!
\\smallskip

\\begin{{center}}
{tabular}
\\end{{center}}
\\smallskip

"""

    def checkunits(self, user_units):
        user_units = user_units.replace('.', ' ')
        user_units = user_units.lower()
        long_format = inflector.plural(str(self.height_unit))
        abbrev = '{:~}'.format(self.height_unit)
        peculiar = str(self.height_unit)
        return user_units in [long_format, abbrev, peculiar]

    def checkanswer(self, user_answer):
        if len(user_answer.split(' ')) == 1:
            return false
        else:
            user_answer, user_units = user_answer.split(' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return abs(user_answer - self.answer) < 0.0005 and self.checkunits(user_units)


    def format_useranswer(self, user_answer, display=False):
        if len(user_answer.split(' ')) == 1:
            return user_answer
        else:
            user_answer, user_units = user_answer.split(' ')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return f'\({latex(user_answer)}\) {user_units}'

    @classmethod
    def validator(self, user_answer):
        try:
            if len(user_answer.split(' ')) == 1:
                user_answer = user_answer.replace('^', '**')
                user_answer = parse_expr(user_answer, transformations=transformations)
                float(user_answer)
            else:
                user_answer, user_units = user_answer.split(' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError






Question_Class = PlantProblemComputation
