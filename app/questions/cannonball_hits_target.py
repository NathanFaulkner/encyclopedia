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


class CannonballHitsTarget(Question):
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
        theta = random.randint(10,75)
        v0 = random.randint(328, 656)
        h0 = random.randint(4,30)
        c = h0

        voy = v0*sy.sin(theta*sy.pi/180)
        vox = v0*sy.cos(theta*sy.pi/180)
        b = float(str(round(voy/vox,3)))
        a = float(str(round(-16/vox**2,5)))
        self.a = a
        self.b = b
        # print(b)
        self.c = c

        def y(x):
            return h0 + b*x + a*x**2



        x = sy.Symbol('x')
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = sy.Symbol('x')
        expr = y(x)

        h = -b/2/a
        k = y(h)
        self.h = h
        self.k = k
        self.format_answer = f"""
        Max height of y = {k:.5f} feet at x = {h:.5f} feet
        """

        self.prompt_single = f"""
        After rounding the results of some intermediate calculations that are not displayed
        here, the vertical height \(y\) above the ground of a cannonball shot
        from an initial height of \({h0}\) feet with an initial velocity
        of \({v0}\) feet per second and initial launch angle
        (measured from the ground) of \({theta}^\circ\)
        can be given as a function of the horizontal distance
        \(x\) it has traveled from the launching point
        (if we neglect air resistance and the coriolis effect!) by
        \[
            y(x) = {a:.5f}x^2 + {b:.3f}x + {c}
        \]
        Find the horizontal distance \(x\) away from the launching point at
        which the cannonball crashes to Earth.
        """

        self.format_given_for_tex = f"""
        {self.prompt_single}
        """

        self.full_answer = f"""We need to solve the equation
        \\[
        {self.a:.5f}x^2 + {self.b:.3f}x + {self.c} = 0
        \\]
        Just use the quadratic formula:
        \\begin{{align*}}
        x & = \\frac{{-b\pm\sqrt{{b^2-4ac}}}}{{2a}} \\\\
        & = \\frac{{ -{self.b} \pm \\sqrt{{({self.b})^2 - 4({self.a})({self.c})}}}}{{2({self.a})}} \\\\
        x & \\approx {round(sy.solve(expr)[0], 3)} \\quad  \\textrm{{or}}
         \\quad x \\approx {round(sy.solve(expr)[1], 3)}
        \\end{{align*}}
        Now, since we are interested in the cannonball hitting the ground beyond our
        target (rather than behind it!) we select the positive answer.
        As a challenge, you should contemplate what the negative answer represents;
        it isn't meaningless!

        So, the final answer is \\(x \\approx {round(sy.solve(expr)[1], 3)}\\) ft."""

    name = 'Cannonball Hits Target'
    module_name = 'cannonball_hits_target'


    further_instruction = """
    Your answer should be of the following style (or close to it), with items highlighted in
    red replaced by your answer:

    <blockquote>
        Max height of y = <span style="color: red">200</span> feet above
        the ground at horizontal distance
        x = <span style="color: red">100</span> feet from the launching point
    </blockquote>

    Do NOT use commas to format numbers.  For instance, write '2220' not '2,220'.
    Your answer must be accurate to two decimal places.
    """

    loom_link = "https://www.loom.com/share/d6efec7f9ae0459e93344e76e4a3ec3b"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'




    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace(',', '')
        if 'min' in user_answer:
            return False
        if ' x' not in user_answer or ' y' not in user_answer:
            return False
        i = user_answer.find(' x')
        user_x = user_answer[i+2:]
        i = user_x.find('=')
        user_x = user_x[i+1:]
        user_x = user_x.strip()
        i = user_x.find(' ')
        if i != -1:
            user_x = user_x[:i]
        user_x = user_x.replace('^', '**')
        user_x = parse_expr(user_x, transformations=transformations)
        i = user_answer.find(' y')
        user_y = user_answer[i+2:]
        i = user_y.find('=')
        user_y = user_y[i+1:]
        user_y = user_y.strip()
        i = user_y.find(' ')
        if i != -1:
            user_y = user_y[:i]
        user_y = user_y.replace('^', '**')
        user_y = parse_expr(user_y, transformations=transformations)
        correct = abs(user_x - self.h) < 0.005 and abs(user_y -self.k) < max(-self.a*0.01*self.h + self.b*0.005, 0.005)
        return bool(correct)
        # return correct

    def format_useranswer(self, user_answer, display=False):
        user_answer = user_answer.split(' ')
        for i in range(len(user_answer)):
            word = user_answer[i]
            try:
                if has_numbers(word):
                    word = word.replace('^', '**')
                    word = parse_expr(word, transformations=transformations)
                    user_answer[i] = latex(word)
            except:
                pass
        formatted = ''
        for word in user_answer:
            formatted += str(word) + ' '
        return formatted

    @classmethod
    def validator(self, user_answer):
        try:
            user_answer = user_answer.lower()
            if ',' in user_answer:
                raise SyntaxError
            if ' x' not in user_answer or ' y' not in user_answer:
                raise SyntaxError
            if 'of x' in user_answer:
                raise SyntaxError
            if 'at y' in user_answer:
                raise SyntaxError
            i = user_answer.find(' x')
            user_x = user_answer[i+2:]
            i = user_x.find('=')
            user_x = user_x[i+1:]
            user_x = user_x.strip()
            i = user_x.find(' ')
            if i != -1:
                user_x = user_x[:i]
            user_x = user_x.replace('^', '**')
            user_x = parse_expr(user_x, transformations=transformations)
            i = user_answer.find(' y')
            user_y = user_answer[i+2:]
            i = user_y.find('=')
            user_y = user_y[i+1:]
            user_y = user_y.strip()
            i = user_y.find(' ')
            if i != -1:
                user_y = user_y[:i]
            user_y = user_y.replace('^', '**')
            user_y = parse_expr(user_y, transformations=transformations)
            if abs(user_x - 1.23) < 0.005 and abs(user_y - 1.23) < 0.01:
                pass
        except:
            raise SyntaxError


Question_Class = CannonballHitsTarget
prob_type = 'math_blank'
