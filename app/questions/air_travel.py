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
                            permute_equation,
                            has_letters,
                            find_numbers)

ureg = UnitRegistry()

inflector = inflect.engine()
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

class AirTravelProblem(Question):
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)


        CHARtoSEA = {
          "origin" : "Charlotte",
          "destination" : "Seattle",
          "to": 5 * ureg.hours + 8 * ureg.minutes,
          "from": 4 * ureg.hours + 24 * ureg.minutes,
          "dist": 2286 * ureg.miles
        }

        CHARtoSF = {
          "origin" : "Charlotte",
          "destination" : "San Francisco",
          "to": 5 * ureg.hours + 3 * ureg.minutes,
          "from": 4 * ureg.hours + 25 * ureg.minutes,
          "dist": 2302 * ureg.miles
        }

        CHARtoLA = {
          "origin" : "Charlotte",
          "destination" : "Los Angeles",
          "to": 4 * ureg.hours + 38 * ureg.minutes,
          "from": 4 * ureg.hours + 10 * ureg.minutes,
          "dist": 2120 * ureg.miles
        }

        CHARtoSD = {
          "origin" : "Charlotte",
          "destination" : "San Diego",
          "to": 4 * ureg.hours + 34 * ureg.minutes,
          "from": 4 * ureg.hours + 2 * ureg.minutes,
          "dist": 2081 * ureg.miles
        }


        RDUtoSEA =	{
          "origin" : "Raleigh",
          "destination" : "Seattle",
          "to": 6 * ureg.hours + 10 * ureg.minutes,
          "from": 5 * ureg.hours + 14 * ureg.minutes,
          "dist": 2367 * ureg.miles
        }

        RDUtoSF = {
          "origin" : "Raleigh",
          "destination" : "San Francisco",
          "to": 5 * ureg.hours + 48.5 * ureg.minutes,
          "from": 4 * ureg.hours + 58 * ureg.minutes,
          "dist": 2410 * ureg.miles
        }

        RDUtoLA = {
          "origin" : "Raleigh",
          "destination" : "Los Angeles",
          "to" : 5 * ureg.hours + 15 * ureg.minutes,
          "from": 4 * ureg.hours + 56 * ureg.minutes,
          "dist": 2233 * ureg.miles
        }

        RDUtoSD = {
          "origin" : "Raleigh",
          "destination" : "San Diego",
          "to" : 5 * ureg.hours + 5 * ureg.minutes,
          "from": 4 * ureg.hours + 54 * ureg.minutes,
          "dist": 2188 * ureg.miles
        }


        scenario = random.choice([RDUtoSEA, RDUtoLA, RDUtoSD,
                                CHARtoSEA, CHARtoLA, CHARtoSD, CHARtoSF])

        class FlightTime():
            def __init__(self, time):
                self.time = time.magnitude
                self.hours = int(self.time)
                self.minutes = int((self.time - self.hours) * 60)

        to_flight_time = FlightTime(scenario["to"])
        error_factor = 1 + random.choice([1, -1]) * random.random()*0.05
        error_factor = 1
        to_time_random = FlightTime(to_flight_time.time * error_factor * ureg.hours)
        to_hrs = to_time_random.hours
        to_minutes = to_time_random.minutes
        to_time = to_hrs + to_minutes/60

        from_flight_time = FlightTime(scenario["from"])
        error_factor = 1 + random.choice([1, -1]) * random.random()*0.05
        error_factor = 1
        from_time_random = FlightTime(from_flight_time.time * error_factor * ureg.hours)
        from_hrs = from_time_random.hours
        from_minutes = from_time_random.minutes
        from_time = from_hrs + from_minutes/60

        A = [[to_time, -to_time],[from_time, from_time]]
        B = [scenario["dist"].magnitude, scenario["dist"].magnitude]

        v, w = np.linalg.solve(A,B)
        self.v = round(v, 2)
        self.w = round(w, 2)

        self.format_answer = f"""
The apparent speed of the airplane is {self.v} mph,
and the wind speed was {self.w} mph."""

        self.prompt_single = f"""
<p>
The average direct flight from
<span style="color:red">{scenario["origin"]}</span> to
<span style="color:red">{scenario["destination"]}</span> takes
<span style="color:red">{to_hrs}</span> hours and
<span style="color:red">{to_minutes}</span> minutes.
However, the return flight from
<span style="color:red">{scenario["destination"]}</span> to
<span style="color:red">{scenario["origin"]}</span> takes
an average of
<span style="color:red">{from_hrs}</span> hours and
<span style="color:red">{from_minutes}</span> minutes.
The difference between the two can be accounted
for by the wind blowing against the plane as it flies west
(the prevailing winds blow east) but actually adding to the plane's
speed as it travels back east!
The distance between these two cities is about
<span style="color:red">{scenario["dist"].magnitude}</span> miles.
</p>

<p>
Find the average wind speed and the average apparent speed
of the plane (relative to the air) across a two-way trip.
Give you answer in miles per hour.
The key here is to realize that you can add the wind
speed to the plane's speed for the return (west to east trip),
but you must subtract it on the trip from east to west.
You can round your answer to two decimal places, but you MUST
include four decimal places for intermediate steps.
</p>
"""

        self.format_given_for_tex = f"""
The average direct flight from {scenario["origin"]} to
{scenario["destination"]} takes {to_hrs} hours and
{to_minutes} minutes.  However, the return flight from
{scenario["destination"]} to {scenario["origin"]} takes
an average of
{from_hrs} hours and {from_minutes} minutes.
The difference between the two can be accounted
for by the wind blowing against the plane as it flies west
(the prevailing winds blow east) but actually adding to the plane's
speed as it travels back east!
The distance between these two cities is about
{scenario["dist"].magnitude} miles.

Find the average wind speed and the average apparent speed
of the plane (relative to the air) across a two-way trip.
The key here is to realize that you can add the wind
speed to the plane's speed for the return (west to east trip),
but you must subtract it on the trip from east to west.
You can round your answer to two decimal places, but you MUST
include four decimal places for intermediate steps.
"""

    prob_type = 'math_blank'

    name = 'Air Travel Problem'
    module_name = 'air_travel'


    prompt_multiple = """TBA
    """
    further_instruction = """Enter your answer as
"average apparent speed of planes, average wind speed".
For instance, you answer might be "405.31, 35.67"
The point is, you must separate the values by a comma and list
the airplanes' apparent speed first!  Also, do NOT use commas
to format your numbers.  For instance, if the plane
flew 1,000 mph, enter "1000" not "1,000".  Otherwise you'll either
get a syntax error or, possibly, the checker will misunderstand your intent.
"""

    # loom_link = ""






    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = user_answer.replace('(', '')
        user_answer = user_answer.replace(')', '')
        if ',' not in user_answer and ' and' not in user_answer:
            return False
        if len(user_answer.split(',')) > 1:
            user_x, user_y = user_answer.split(',')
        elif len(user_answer.split(' and')) > 1:
            user_x, user_y = user_answer.split(' and')
        if ' y ' in user_x:
            user_x, user_y = [user_y, user_x]
        elif 'wind' in user_x:
            user_x, user_y = [user_y, user_x]
        if ' x ' in user_x or 'x=' in user_x:
            i = user_x.find('x')
            user_x = user_x[i+1:]
            i = user_x.find('=')
            user_x = user_x[i+1:]
            user_x = user_x.replace(' ', '')
            user_x = parse_expr(user_x, transformations=transformations)
        elif 'plane' in user_x:
            user_x = find_numbers(user_x)
        else:
            user_x = user_x.replace(' ', '')
            user_x = parse_expr(user_x, transformations=transformations)
        if ' y ' in user_y or 'y=' in user_y:
            i = user_y.find('y')
            user_y = user_y[i+1:]
            i = user_y.find('=')
            user_y = user_y[i+1:]
            user_y = user_y.replace(' ', '')
            user_y = parse_expr(user_y, transformations=transformations)
        elif 'wind' in user_y:
            user_y = find_numbers(user_y)
        else:
            user_y = user_y.replace(' ', '')
            user_y = parse_expr(user_y, transformations=transformations)
        return abs(user_y - self.w) < 0.005 and abs(user_x - self.v) < 0.005

    def format_useranswer(self, user_answer, display=False):
        # user_answer = user_answer.lower()
        if has_letters(user_answer):
            return user_answer
        else:
            return f'\({user_answer}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('(', '')
            user_answer = user_answer.replace(')', '')
            if ',' not in user_answer and ' and' not in user_answer:
                raise SyntaxError
            if len(user_answer.split(',')) > 1:
                user_x, user_y = user_answer.split(',')
            elif len(user_answer.split(' and')) > 1:
                user_x, user_y = user_answer.split(' and')
            if ' y ' in user_x or 'y=' in user_x:
                user_x, user_y = [user_y, user_x]
            elif 'wind' in user_x:
                user_x, user_y = [user_y, user_x]
            if ' x ' in user_x or 'x=' in user_x:
                i = user_x.find('x')
                user_x = user_x[i+1:]
                i = user_x.find('=')
                user_x = user_x[i+1:]
                user_x = user_x.replace(' ', '')
                user_x = parse_expr(user_x, transformations=transformations)
            elif 'plane' in user_x:
                user_x = find_numbers(user_x)
            else:
                user_x = user_x.replace(' ', '')
                user_x = parse_expr(user_x, transformations=transformations)
            if ' y ' in user_y:
                i = user_y.find('y')
                user_y = user_y[i+1:]
                i = user_y.find('=')
                user_y = user_y[i+1:]
                user_y = user_y.replace(' ', '')
                user_y = parse_expr(user_y, transformations=transformations)
            elif ' wind' in user_y:
                user_y = find_numbers(user_y)
            else:
                user_y = user_y.replace(' ', '')
                user_y = parse_expr(user_y, transformations=transformations)
        except:
            raise SyntaxError






Question_Class = AirTravelProblem
