from sympy import *
import random

__all__ = ['quadratic_pattern', 'graph_point_slope']

class Question():
    pass

def latex_print(expr, display=False):
    if display:
        return '\[' + latex(expr) + '\]'
    else:
        return '\(' + latex(expr) + '\)'

def random_non_zero_integer(a,b):
    out = 0
    while out == 0:
        out = random.randint(a,b)
    return out
