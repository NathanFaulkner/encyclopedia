#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, random_non_zero_integer, latex_print, has_numbers

from app.questions.quadratic_can_be_imaginary import QuadraticCanBeImaginary

class QuadraticForceImaginary(QuadraticCanBeImaginary):
    """
    """
    def __init__(self, **kwargs):
        kwargs['force_imaginary'] = True
        super().__init__(**kwargs)



Question_Class = QuadraticForceImaginary
prob_type = 'math_blank'
