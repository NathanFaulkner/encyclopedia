#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, random_non_zero_integer, latex_print, has_numbers

from app.questions.complete_factorization_level1 import CompleteFactorizationLevel1

class CompleteFactorizationLevel1NiceFactors(CompleteFactorizationLevel1):
    """
    """
    def __init__(self, **kwargs):
        kwargs['nice'] = True
        super().__init__(**kwargs)

    module_name = 'complete_factorization_level1_nice_factors'



Question_Class = CompleteFactorizationLevel1NiceFactors
prob_type = 'math_blank'
