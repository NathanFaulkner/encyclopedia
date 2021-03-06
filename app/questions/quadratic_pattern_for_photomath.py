#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, random_non_zero_integer, latex_print, has_numbers

from app.questions.quadratic_pattern import QuadraticPattern

class QuadraticPatternForPhotoMath(QuadraticPattern):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            seed = kwargs['seed']
        else:
            seed = random.random()
        kwargs['seed'] = seed
        random.seed(seed)
        kwargs['p'] = 1
        kwargs['r'] = random.choice([3, 6, 9])
        super().__init__(**kwargs)



Question_Class = QuadraticPatternForPhotoMath
prob_type = 'math_blank'
