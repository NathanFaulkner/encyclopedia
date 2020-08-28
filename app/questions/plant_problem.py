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

class PlantProblem(Question):
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
        self.answer = self.m * x + self.b
        self.format_answer = f'\(h = {latex(self.answer)}\)'

        self.prompt_single = f"""
        The following table depicts the height of a {self.plant.name} plant
        depending on the number of {inflector.plural(str(self.time_unit))} that it has
        grown.
        Develop an equation that relates the height of the plant
        to the time that it has grown.  Use the letter \(h\) for
        the height of the plant.  Use the letter \(x\) for the number
        of {inflector.plural(str(self.time_unit))} that have gone by
        since "{str(self.time_unit).title()} 0"."""

        prompt_multiple = f"""For each of the following tables,
        develop an equation that relates the height of the plant
        to the time that it has grown.  Use the letter \(P\) for
        the price of the pizza.  Use the letter \(x\) for the number
        of {inflector.plural(str(self.time_unit))} that have gone by
        since "{str(self.time_unit).title()} 0"."""

        self.genproblem()

    prob_type = 'math_blank'

    name = 'Plant Growth Problem'
    module_name = 'plant_problem'


    further_instruction = """Just enter the equation in a natural way.
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
            user_y = None
        if 'x' in user_answer:
            user_x = 'x'
        elif 'X' in user_answer:
            user_x = 'X'
        elif 't' in user_answer:
            user_x = 't'
        elif 'T' in user_answer:
            user_x = 'T'
        else:
            user_n = None
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
