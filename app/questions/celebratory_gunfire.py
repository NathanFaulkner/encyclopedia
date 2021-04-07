#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            sgn, leading_coeff, signed_coeff,
                            fmt_slope_style,
                            find_numbers,
                            has_numbers)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class CelebratoryGunfire(Question):
    """
    The given is an expanded form of

    \\[
        a(x - h)^2 + k
    \\]

    The directions are to find the max or min.  Answer example:
    "Max at x= h  of y = k"
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        starting_height = random.randint(75,95)
        c = round(starting_height/12.0,3)
        h0 = c
        veloc_factor = random.randint(15,32)
        velocity = veloc_factor*100
        b = velocity
        t = sy.Symbol('t')
        y = c + b*t - 16*t**2
        self.a = a = -16
        self.b = b
        # print(b)
        self.c = c

        def y(x):
            return h0 + b*x + a*x**2

        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('t')
        x = self.x
        expr = y(x)

        h = -b/2/a
        k = y(h)
        self.h = h
        self.k = k
        ans = h + sy.sqrt(-k/a)
        self.answer = ans
        self.format_answer = f"""{ans:.5f} seconds"""

        self.prompt_single = f"""
        In some cultures it is common to celebrate a holiday or special event
        by firing bullets into the air.

        Let's imagine that the bullet leaves the muzzle of a gun at a position
        of {starting_height} inches (let's call it {c} feet) from the ground.
        A typical bullet velocity is {velocity} feet per second
        (but it varies considerably).
        According to Newton's law of gravitation,
        the bullet falls to Earth (neglecting air resistance)
        with an acceleration of 32 feet per second per second.
        (FYI: Acceleration measures the rate of change of the velocity.)

        All that combines to give you the following model for the position
        \(y\) of the bullet relative to the ground after \(t\) seconds
            \[
                y(t) = {c:.3f} + {b}t - 16t^2
            \]
        (FYI: Where did the '32' go?  It became a 16.)

        Your task: Figure how quickly (in seconds) the party-goers need to leave the area!!
        Your answer must be accurately rounded to at least
        two decimal places (more is fine).
        """

        self.format_given_for_tex = f"""
                In some cultures it is common to celebrate a holiday or special event
                by firing bullets into the air.

                Let's imagine that the bullet leaves the muzzle of a gun at a position
                of {starting_height} inches (let's call it {c} feet) from the ground.
                A typical bullet velocity is {velocity} feet per second
                (but it varies considerably).
                According to Newton's law of gravitation,
                the bullet falls to Earth (neglecting air resistance)
                with an acceleration of 32 feet per second per second.
                (FYI: Acceleration measures the rate of change of the velocity.)

                All that combines to give you the following model for the position
                \(y\) of the bullet relative to the ground after \(t\) seconds
                    \[
                        y(t) = {c:.3f} + {b}t - 16t^2
                    \]
                (FYI: Where did the `32' go?  It became a 16.)

                Your task: Figure how quickly (in seconds) the party-goers need to leave the area!!
                Your answer must be accurately rounded to at least
                two decimal places (more is fine).
        """

    name = 'Celebratory Gunfire'
    module_name = 'celebratory_gunfire'


    further_instruction = """
    Your answer should just include the numerical answer followed by correct units.
    Do not include "t=".
    """

    # loom_link = "https://www.loom.com/share/d6efec7f9ae0459e93344e76e4a3ec3b"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'




    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.strip()
        # user_answer = user_answer.replace(' ', '')
        user_answer = user_answer.replace('t', '')
        user_answer = user_answer.replace('=', '')
        user_answer = user_answer.replace(',', '')
        user_answer = user_answer.replace('seconds', 's')
        user_answer = user_answer.replace('secs', 's ')
        user_answer = user_answer.replace('sec', 's')
        if user_answer[-1] != 's':
            return False
        user_x = user_answer[:-1]
        user_x = user_x.replace('^', '**')
        user_x = parse_expr(user_x, transformations=transformations)
        correct = abs(user_x - self.answer) < 0.005
        return bool(correct)
        # return correct

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.strip()
        # user_answer = user_answer.replace(' ', '')
        user_answer = user_answer.replace('t', '')
        user_answer = user_answer.replace('=', '')
        user_answer = user_answer.replace(',', '')
        user_answer = user_answer.replace('seconds', 's')
        user_answer = user_answer.replace('secs', 's ')
        user_answer = user_answer.replace('sec', 's')
        if user_answer[-1] != 's':
            return user_answer
        user_x = user_answer[:-1]
        user_x = user_x.replace('^', '**')
        user_x = parse_expr(user_x, transformations=transformations)
        formatted = f'\({sy.latex(user_x)}\) ' + ' seconds'
        return formatted

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.strip()
            # user_answer = user_answer.replace(' ', '')
            user_answer = user_answer.replace('t', '')
            user_answer = user_answer.replace('=', '')
            user_answer = user_answer.replace(',', '')
            user_answer = user_answer.replace('seconds', 's')
            user_answer = user_answer.replace('secs', 's ')
            user_answer = user_answer.replace('sec', 's')
            if user_answer[-1] != 's':
                pass
            user_x = user_answer[:-1]
            user_x = user_x.replace('^', '**')
            user_x = parse_expr(user_x, transformations=transformations)
            correct = abs(user_x - 0.01) < 0.005
            correct = bool(correct)
            formatted = f'\({sy.latex(user_x)}\) ' + ' seconds'
        except:
            raise SyntaxError


Question_Class = CelebratoryGunfire
prob_type = 'math_blank'
