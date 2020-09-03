from sympy import *
import random

from app.interpolator import cart_x_to_svg, cart_y_to_svg

__all__ = ['quadratic_pattern',
            'graph_slope_intercept',
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
            'generic_table', 'generic_table_computation',
            'function_from_set_notation',
            'function_notation',
            'function_composition',
            'graph_to_slope_intercept_form']

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

def compose(f, g):
    return lambda x: f(g(x))

class RandomLinearFunction():
    """
    self.f is lambda x: a*x + b
    where a and b can be specified
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-5,5)
        if 'b' in kwargs:
            self.b = kwargs['b']
        else:
            self.b = random.randint(-5,5)

        self.f = lambda x: self.a*x + self.b

class RandomVertexFormQuadratic():
    """
    self.f is lambda x: a*(x - h)**2 + k
    where a, h, and k can be specified
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random.choice([-Rational(1,2), Rational(1,2), 1, -1, 2, -2])
        if 'h' in kwargs:
            self.h = kwargs['h']
        else:
            self.h = random.randint(-5,5)
        if 'k' in kwargs:
            self.k = kwargs['k']
        else:
            self.k = random.randint(-5,5)

        self.f = lambda x: self.a*(x - self.h)**2 + self.k

class RandomAbsValueFunction():
    """
    self.f is lambda x: a(x - h)**2 + k
    where a, h, and k can be specified
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'a' in kwargs:
            self.a = kwargs['a']
        else:
            self.a = random_non_zero_integer(-5,5)
        if 'h' in kwargs:
            self.h = kwargs['h']
        else:
            self.h = random.randint(-5,5)
        if 'k' in kwargs:
            self.k = kwargs['k']
        else:
            self.k = random.randint(-5,5)

        self.f = lambda x: self.a*abs(x - self.h) + self.k

def poly_points_from_nparrays(x, y):
    x_points = cart_x_to_svg(x)
    y_points = cart_y_to_svg(y)
    i = 0
    out = ""
    while i < len(x_points):
        out += f"{x_points[i]}, {y_points[i]} "
        i += 1
    return out
