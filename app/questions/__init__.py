from sympy import *
import random

__all__ = ['quadratic_pattern',
            'graph_point_slope',
            'solve_for_x',
            'linear_inequality',
            'graph_of_linear_inequality',
            'compound_linear_inequality',
            'graph_of_compound_linear_inequality',
            'inequality_to_interval_notation',
            'interval_to_inequality_notation',
            'interval_notation_to_graph',
            'absolute_value_equation',
            'absolute_value_inequality',
            'absolute_value_inequality_to_interval_notation',
            'absolute_value_inequality_to_graph',
            'pizza_problem', 'pizza_problem_computation',
            'plant_problem', 'plant_problem_computation',
            'generic_table', 'generic_table_computation']

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

def permute_equation(terms, as_list=False):
    random.shuffle(terms)
    l = len(terms)
    divider = random.randint(0, l)
    i = 0
    LHS = 0
    RHS = 0
    while i < divider:
        LHS += terms[i]
        i += 1
    while i < l:
        RHS -= terms[i]
        i += 1
    if as_list:
        return [LHS, RHS]
    return Eq(LHS, RHS)
