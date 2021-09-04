#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation,
                            has_letters,
                            )
from app.questions.compound_linear_inequality import CompoundLinearInequality


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general
prob_type = 'math_blank'




class CompoundLinearInequalityOr(CompoundLinearInequality):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            seed = kwargs['seed']
        else:
            seed = random.random()
        kwargs['seed'] = seed
        random.seed(seed)
        kwargs['logical_connector'] = 'or'
        super().__init__(**kwargs)

    module_name = 'compound_linear_inequality_or'
    name = 'Compound Linear "Or" Inequality'



Question_Class = CompoundLinearInequalityOr
