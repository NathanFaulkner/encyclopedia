#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, random_non_zero_integer, latex_print, has_numbers

from app.questions.complete_factorization_level1 import CompleteFactorizationLevel1

class CompleteFactorizationLevel1ThreeNiceFactors(CompleteFactorizationLevel1):
    """
    """
    def __init__(self, **kwargs):
        kwargs['nice'] = True
        kwargs['num_factors'] = 3
        super().__init__(**kwargs)


    loom_link = "https://www.loom.com/share/3bbf5a9cf5e74f038d9d0f52fcf60587"
    module_name = 'complete_factorization_level1_three_nice_factors'


Question_Class = CompleteFactorizationLevel1ThreeNiceFactors
prob_type = 'math_blank'
