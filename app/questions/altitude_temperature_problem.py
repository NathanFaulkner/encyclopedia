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
ureg = UnitRegistry()
import inflect
inflector = inflect.engine()

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation)
# from app.interpolator import cart_x_to_svg, cart_y_to_svg

from sqlalchemy import (MetaData,
                        Table,
                        Column,
                        create_engine,
                        select)

engine = create_engine('sqlite:///app/questions/climate.db', echo = None, connect_args={'check_same_thread': False})
conn = engine.connect()
# print('table_names', engine.table_names())
metadata = MetaData()
ws_climate = Table('climate_of_winston_salem', metadata, autoload=True,
                   autoload_with=engine)
boone_climate = Table('climate_of_boone', metadata, autoload=True,
                   autoload_with=engine)

class Locale():
    def __init__(self, name, table):
        self.name = name
        self.table = table
        stmt = select([table])
        self.rows = conn.execute(stmt).fetchall()
        for row in self.rows:
            if 'average high' in row[0].lower():
                self.monthly_avg_highs = [float(data.split('\n')[0]) for data in row[1:13]]
                self.yearly_avg_high = float(row[13].split('\n')[0])
            elif 'average low' in row[0].lower():
                self.monthly_avg_lows = [float(data.split('\n')[0]) for data in row[1:13]]
                self.yearly_avg_low = float(row[13].split('\n')[0])
            elif 'daily mean' in row[0].lower():
                self.monthly_daily_means = [float(data.split('\n')[0]) for data in row[1:13]]
                self.yearly_daily_mean = float(row[13].split('\n')[0])
        self.temps = {'avg_highs': [self.yearly_avg_high] + self.monthly_avg_highs,
            'avg_lows': [self.yearly_avg_low] + self.monthly_avg_lows,
            'daily_means': [self.yearly_daily_mean] + self.monthly_daily_means}

    def set_altitude(self, altitude):
        self.altitude = altitude


ws = Locale('Winston-Salem', ws_climate)
ws.set_altitude(960 * ureg.foot)
boone = Locale('Boone', boone_climate)
boone.set_altitude(3000 * ureg.foot)

months = {1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'}

temp_abbrev = {ureg.degC: '\\(^\\circ\\textrm{C}\\)',
                ureg.degF: '\\(^\\circ\\textrm{F}\\)'}

prob_type = 'math_blank'


class AltitudeTemperatureProblem(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'temp_unit' in kwargs:
            self.temp_unit = kwargs['temp_unit']
        else:
            self.temp_unit = random.choice([ureg.degF, ureg.degC])
        if 'alt_unit' in kwargs:
            self.alt_unit = kwargs['alt_unit']
        else:
            self.alt_unit = random.choice([ureg.meter, ureg.foot])
        if 'lower_locale' in kwargs:
            self.lower_locale = kwargs['lower_locale']
        else:
            self.lower_locale = ws
        if 'upper_locale' in kwargs:
            self.upper_locale = kwargs['upper_locale']
        else:
            self.upper_locale = boone
        lower_altitude = self.lower_locale.altitude + random.randint(-3,3) * 20 * ureg.foot
        lower_altitude = lower_altitude.to(self.alt_unit)
        lower = round(lower_altitude.magnitude,-1)
        self.lower_alt = lower
        upper = round(self.upper_locale.altitude.to(self.alt_unit).magnitude, -1)
        self.upper_alt = upper
        diff = upper - lower
        self.l = random.randint(6,8)
        alt_delta = int(diff/(self.l-1)/10)*10
        self.alt_delta = alt_delta
        upper_latitude = lower + self.l * alt_delta
        self.moment = random.randint(0,12)
        if self.moment == 0:
            calendar_descriptor = 'year'
        else:
            calendar_descriptor = f'month of {months[self.moment]}'
        which_temps = random.choice(['avg_highs', 'avg_lows', 'daily_means'])
        temp_descriptors = {'avg_highs': 'average daily high',
                        'avg_lows': 'average daily low',
                        'daily_means': 'average daily temperature'}
        temp_descriptor = temp_descriptors[which_temps]
        lower_temps = self.lower_locale.temps[which_temps]
        lower_temp = ureg.Quantity(lower_temps[self.moment], ureg.degF)
        lower_temp = round(lower_temp.to(self.temp_unit),1)
        self.lower_temp = lower_temp
        upper_temps = self.upper_locale.temps[which_temps]
        upper_temp = ureg.Quantity(upper_temps[self.moment], ureg.degF)
        upper_temp = upper_temp.to(self.temp_unit)
        temp_delta = round((lower_temp.magnitude - upper_temp.magnitude)/(self.l - 1), 1)
        self.temp_delta = temp_delta
        upper_temp = lower_temp.magnitude - self.l * temp_delta
        self.upper_temp = upper_temp

        x = Symbol('x')
        self.answer = lower_temp.magnitude - temp_delta/alt_delta*(x - self.lower_alt)
        self.m = -temp_delta/alt_delta
        self.b = self.answer.coeff(x, 0)
        self.format_answer = """
        \(T =
            {ltemp} - \\frac{{{tdelta}}}{{{adelta}}}(A - {lalt})\)
        """.format(ltemp=lower_temp.magnitude,
                    tdelta=temp_delta,
                    adelta=alt_delta,
                    lalt=lower)
        # self.format_answer = f'\\( {latex(self.answer)} \\)'


        self.prompt_single = f"""
        The following table depicts the approximate {temp_descriptor}
        for the {calendar_descriptor}, as you
        move up in altitude from a locale in {self.lower_locale.name}
        to a locale in {self.upper_locale.name}."""

        prompt_multiple = f"""To be coded."""

        table_html = f"""
        <table border="1">
            <tr>
                <th>Altitude (in {inflector.plural(str(self.alt_unit))})</th>
        """
        for i in range(self.l + 1):
            table_html += f"""<td style="text-align: center;">{lower + i*alt_delta}</td>"""
        table_html += f"""
            </tr>
            <tr>
                <th>Temperature (in {temp_abbrev[self.temp_unit]})</th>
        """
        for i in range(self.l + 1):
            table_html += f"<td>{round(self.m * (alt_delta *i) + self.lower_temp.magnitude, 1)}</td>"
        table_html += """
            </tr>
        </table>
        """
        self.table_html = table_html
        self.format_given = self.table_html

        tabular = "\\begin{tabular}{|l||"
        for i in range(self.l):
            tabular += 'c|'
        tabular += '}\n\\hline\n'
        tabular += f'Altitude (in {inflector.plural(str(self.alt_unit))}) & '
        for i in range(self.l):
            tabular += f'{lower + i*alt_delta} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n'
        tabular += f'Temperature (in {temp_abbrev[self.temp_unit]}) & '
        for i in range(self.l):
            tabular += f'{round(self.m * (alt_delta *i) + self.lower_temp.magnitude, 1)} & '
        tabular = tabular[:-2]
        tabular += '\\\\\n\\hline\n\\end{tabular}'


        self.format_given_for_tex = f"""
{self.prompt_single}
\\smallskip

{tabular}
\\smallskip

Develop an equation that models the data
in the table, using
\(T\) for the temperature and
\(A\) for the altitude.
"""
        self.format_fragment_for_tex = self.format_given_for_tex

    prob_type = 'math_blank'

    name = 'Altitude vs. Temperature Growth Problem'
    module_name = 'altitude_temperature_problem'


    further_instruction = """Enter an equation that models the data
    in the table, using
    \(T\) for the temperature and
    \(A\) for the altitude.  Also, the coefficients (numbers) in your equation
    have to be accurate to 4 decimal places.  Use exact figures
    wherever possible just in case.  But, as a helpful hint,
    you can enter things like, "-0.6/70" and the checking algorithm
    will be perfectly happy to do reduce this to a decimal for you.
    You DO NOT have to simplify your answer.
    """

    # loom_link = ""



    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('y', 't')
        user_answer = user_answer.replace('x', 'a')
        if 't' not in user_answer:
            return False
        if 'a' not in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        t, a  = symbols('t a')
        user_answer = solve(user_answer, t)[0]
        user_answer_m = user_answer.coeff(a)
        user_answer_b = user_answer.coeff(a, 0)
        # print('m:', user_answer_m, self.m)
        return abs(user_answer_m - self.m) < 0.00005 and abs(user_answer_b - self.b) < 0.00005



    def format_useranswer(self, user_answer, display=False):
        if 't' in user_answer:
            user_y = 't'
        elif 'T' in user_answer:
            user_y = 'T'
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
        elif 'a' in user_answer:
            user_x = 'a'
        elif 'A' in user_answer:
            user_x = 'A'
        else:
            user_x = ''
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('y', 't')
        user_answer = user_answer.replace('x', 'a')
        user_answer = user_answer.replace('^', '**')
        lhs, rhs = user_answer.split('=')
        lhs = parse_expr(lhs, transformations=transformations)
        rhs = parse_expr(rhs, transformations=transformations)
        user_answer = Eq(lhs, rhs)
        t, a  = symbols('t a')
        user_answer = solve(user_answer, t)[0]
        user_m = float(user_answer.coeff(a))
        user_b = float(user_answer.coeff(a, 0))
        if user_m > 0:
            sign = '+'
        elif user_m < 0:
            sign = '-'
        else:
            sign = '+'
        return f'\({user_y} = {user_b:.4f} {sign} {abs(user_m):.4f} {user_x}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            if 't' in user_answer:
                user_y = 't'
            elif 'T' in user_answer:
                user_y = 'T'
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
            elif 'a' in user_answer:
                user_x = 'a'
            elif 'A' in user_answer:
                user_x = 'A'
            else:
                user_x = ''
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('y', 't')
            user_answer = user_answer.replace('x', 'a')
            user_answer = user_answer.replace('^', '**')
            lhs, rhs = user_answer.split('=')
            lhs = parse_expr(lhs, transformations=transformations)
            rhs = parse_expr(rhs, transformations=transformations)
            user_answer = Eq(lhs, rhs)
            t, a = symbols('t a')
            user_answer = solve(user_answer, t)[0]
            user_m = float(user_answer.coeff(a))
            user_b = float(user_answer.coeff(a, 0))
            f'\({user_y} = {user_b:.4f} - {abs(user_m):.4f} {user_x}\)'
        except:
            raise SyntaxError






Question_Class = AltitudeTemperatureProblem

conn.close()
