from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

from app.interpolator import cart_x_to_svg, cart_y_to_svg

__all__ = ['quadratic_pattern',
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
            'graph_slope_intercept',
            'graph_to_slope_intercept_form',
            'graph_slope_intercept_from_english',
            'graph_point_slope',
            'graph_point_slope_from_english',
            'description_to_point_slope_form',
            'graph_to_point_slope_form',
            'two_points_to_equation',
            'altitude_temperature_problem',
            'altitude_temperature_problem_computation',
            'generic_table_hard',
            'generic_table_hard_computation',
            'graph_standard_form_line',
            'vertical_or_horizontal', 'vertical_or_horizontal_graph_to_equation',
            'parallel_perpendicular_to_point_slope_form',
            'vertical_or_horizontal_info_to_equation',
            'vertical_or_horizontal_graph_from_description',
            'how_many_solutions_to_system']

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



class GraphFromLambda():
    def __init__(self,
                    f,
                    color="blue",
                    res=0.001,
                    xwindow=[-10,10],
                    ywindow=[-10,10],
                    xmarker_delta=1,
                    ymarker_delta=1):
        self.f = f
        x_min = xwindow[0]
        x_max = xwindow[1]
        y_min = ywindow[0]
        y_max = ywindow[1]

        x = np.arange(x_min,x_max + xmarker_delta,res)

        y = self.f(x)

        if type(y) == int:
            x = np.array([x_min, x_max])
            y = np.array([f(x), f(x)])

        spacing = 1
        minorLocator = MultipleLocator(spacing)

        fig, ax = plt.subplots()

        ax.plot(x, y, color=color)

        fig.set_size_inches(6, 6)

        ax.axhline(y=0, color='k')
        ax.axvline(x=0, color='k')

        #ax.set_aspect('equal')
        ax.set_xticks(np.arange(x_min, x_max + xmarker_delta, xmarker_delta))
        ax.set_yticks(np.arange(y_min, y_max + ymarker_delta, ymarker_delta))

        # Turn on the minor TICKS, which are required for the minor GRID
        ax.minorticks_on()

        ax.yaxis.set_minor_locator(minorLocator)
        ax.xaxis.set_minor_locator(minorLocator)

        ax.grid(True, which='major')


        plt.axis([x_min,x_max,y_min, y_max])

        self.fig = fig
        # plt.show()

    def save_fig(self, file_name):
        self.fig.savefig(f'{file_name}.png', bbox_inches='tight')

class GraphVert():
    def __init__(self,
                    value,
                    color="blue",
                    res=0.001,
                    xwindow=[-10,10],
                    ywindow=[-10,10],
                    xmarker_delta=1,
                    ymarker_delta=1):
        self.value = value
        x_min = xwindow[0]
        x_max = xwindow[1]
        y_min = ywindow[0]
        y_max = ywindow[1]


        spacing = 1
        minorLocator = MultipleLocator(spacing)

        fig, ax = plt.subplots()

        ax.plot(x, y, color=color)

        fig.set_size_inches(6, 6)

        ax.axhline(y=0, color='k')
        ax.axvline(x=0, color='k')
        ax.axvline(x=value, color=color)

        #ax.set_aspect('equal')
        ax.set_xticks(np.arange(x_min, x_max + xmarker_delta, xmarker_delta))
        ax.set_yticks(np.arange(y_min, y_max + ymarker_delta, ymarker_delta))

        # Turn on the minor TICKS, which are required for the minor GRID
        ax.minorticks_on()

        ax.yaxis.set_minor_locator(minorLocator)
        ax.xaxis.set_minor_locator(minorLocator)

        ax.grid(True, which='major')


        plt.axis([x_min,x_max,y_min, y_max])

        self.fig = fig
        # plt.show()

    def save_fig(self, file_name):
        self.fig.savefig(f'{file_name}.png', bbox_inches='tight')

class GraphHoriz():
    def __init__(self,
                    value,
                    color="blue",
                    res=0.001,
                    xwindow=[-10,10],
                    ywindow=[-10,10],
                    xmarker_delta=1,
                    ymarker_delta=1):
        self.value = value
        x_min = xwindow[0]
        x_max = xwindow[1]
        y_min = ywindow[0]
        y_max = ywindow[1]


        spacing = 1
        minorLocator = MultipleLocator(spacing)

        fig, ax = plt.subplots()

        ax.plot(x, y, color=color)

        fig.set_size_inches(6, 6)

        ax.axhline(y=0, color='k')
        ax.axvline(x=0, color='k')
        ax.axhline(y=value, color=color)

        #ax.set_aspect('equal')
        ax.set_xticks(np.arange(x_min, x_max + xmarker_delta, xmarker_delta))
        ax.set_yticks(np.arange(y_min, y_max + ymarker_delta, ymarker_delta))

        # Turn on the minor TICKS, which are required for the minor GRID
        ax.minorticks_on()

        ax.yaxis.set_minor_locator(minorLocator)
        ax.xaxis.set_minor_locator(minorLocator)

        ax.grid(True, which='major')


        plt.axis([x_min,x_max,y_min, y_max])

        self.fig = fig
        # plt.show()

    def save_fig(self, file_name):
        self.fig.savefig(f'{file_name}.png', bbox_inches='tight')

def html_to_tex(html):
    out = fix_quotes_for_tex(html)
    return out

def fix_quotes_for_tex(string):
    count = 0
    i = 0
    while i < len(string):
        if string[i] == '"':
            if count % 2 == 0:
                string = string[:i] + '``' + string[i+1:]
            else:
                string = string[:i] + "''" + string[i+1:]
            count += 1
        i += 1
    return string

def has_letters(s):
    for char in s:
        if char.isalpha():
            return True
    return False

def fmt_slope_style_leading(term):
    try:
        if term.args[0] == 1:
            coeff = ''
        else:
            coeff = latex(term.args[0])
        terms = term.args[1:]
    except IndexError:
        coeff = latex(term)
        terms = []
    variable_part = ''
    for term in terms:
        variable_part += ' ' + latex(term)
    return f'{coeff} {variable_part} '

def fmt_slope_style_trailing(term):
    try:
        coeff = term.args[0]
        terms = term.args[1:]
    except IndexError:
        coeff = term
        terms = []
    if coeff > 0:
        if coeff == 1:
            coeff = ''
        else:
            coeff = latex(coeff)
        sign = '+'
    elif coeff == 0:
        coeff = ''
        sign = ''
    else:
        if coeff == -1:
            coeff = ''
        else:
            coeff = latex(abs(coeff))
        sign = '-'
    variable_part = ''
    for term in terms:
        variable_part += ' ' + latex(term)
    return f'{sign} {coeff} {variable_part} '

def fmt_slope_style(sum):
    x = Symbol('x')
    out = fmt_slope_style_leading(sum.args[0])
    i = 1
    while i < len(sum.args):
        out += fmt_slope_style_trailing(sum.args[i])
        i += 1
    return out
