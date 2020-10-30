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
from app.questions.absolute_value_equation_multi import AbsoluteValueEquationMulti


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general
prob_type = 'math_blank'




class AbsoluteValueEquationMultiThree(AbsoluteValueEquationMulti):
    """
    The given is
    \\[
        |ax + b| +... + similar +  c = 0
    \\]
    but permuted...

    Use kwarg num_terms to control number of extra terms
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            seed = kwargs['seed']
        else:
            seed = random.random()
        kwargs['seed'] = seed
        random.seed(seed)
        if 'num_abs_val_terms' in kwargs:
            num_abs_val_terms = kwargs['num_abs_val_terms']
        else:
            num_abs_val_terms = 3
        kwargs['num_abs_val_terms'] = num_abs_val_terms
        super().__init__(**kwargs)

    module_name = 'absolute_value_equation_multi_three'
    name = 'Equation with Three Absolute Value Terms'



Question_Class = AbsoluteValueEquationMultiThree
