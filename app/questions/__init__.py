from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import random

from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))

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
            'absolute_value_equation', 'absolute_value_equation_plus_linear',
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
            'how_many_solutions_to_system',
            'solve_by_elimination', 'solve_by_elimination_three',
            'solve_by_substitution',
            'we_lost_the_receipts', 'air_travel', 'gold_alloy',
            'graph_absolute_value',
            'graph_absolute_value_basic',
            'graph_absolute_value_basic_to_equation',
            'graph_absolute_value_to_equation',
            'vertex_form_to_standard_form',
            'vertex_form_from_three_points',
            'intercept_form_to_standard_form',
            'graph_vertex_form',
            'graph_vertex_form_to_equation',
            'graph_intercept_form',
            'graph_intercept_form_to_equation',
            'standard_form_to_vertex_form',
            'graph_standard_form',
            'generic_max_min',
            'cannonball_problem',
            'max_revenue_problem',
            'absolute_value_equation_multi',
            'absolute_value_equation_multi_one_or_two',
            'absolute_value_equation_multi_three',
            'factor_trinomials_level1',
            'factor_trinomials_level2',
            'factoring_warm_up',
            'solving_by_factoring_level1',
            'factor_special_patterns',
            'factoring_by_grouping',
            'mixed_practice_plus_gcf',
            'solving_by_factoring_level2',
            'quadratic_only_one_x',
            'solve_by_completing_the_square',
            'solve_by_quadratic_formula',
            'cannonball_hits_target',
            'celebratory_gunfire',
            'adding_or_subtracting_polynomials',
            'multiplying_polynomials',
            ]

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

def permute_equation(terms, as_list=False, **kwargs):
    if 'seed' in kwargs:
        random.seed(kwargs['seed'])
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

def has_numbers(s):
    for char in s:
        if char.isnumeric():
            return True
    return False

def find_numbers(string):
    """Finds numbers in a string and returns a list of them
    in the order in which they appear."""
    numbers = []
    for s in string.split():
        if ',' in s:
            try:
                s = s.replace(',', '')
                numbers.append(float(s))
            except:
                pass
        else:
            try:
                numbers.append(float(s))
            except:
                pass
    if len(numbers) == 1:
        return numbers[0]
    else:
        return numbers


def fmt_slope_style_leading(term):
    if len(term.args) > 1:
        if term.args[0] == 1:
            coeff = ''
        elif term.args[0] == -1:
            coeff = '-'
        else:
            coeff = latex(term.args[0])
        terms = term.args[1:]
        variable_part = ''
        x = Symbol('x')
        if type(term/term.args[0]) == type(x+1):
            variable_part = term/term.args[0]
            variable_part = f'\\left({latex(variable_part)}\\right)'
        else:
            for term in terms:
                variable_part += ' ' + latex(term)
        return f'{coeff} {variable_part} '
    else:
        return latex(term)

def signed_coeff(coeff):
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
    return sign + ' ' + coeff

def leading_coeff(coeff):
    if coeff > 0:
        if coeff == 1:
            coeff = ''
        else:
            coeff = latex(coeff)
    elif coeff == 0:
        coeff = ''
    else:
        if coeff == -1:
            coeff = '-'
        else:
            coeff = latex(coeff)
    return coeff

def fmt_slope_style_trailing(term):
    x = Symbol('x')
    if type(term) == type(5*x):
        coeff = term.args[0]
        terms = term.args[1:]
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
    elif sympify(term).is_number:
        if term > 0:
            return '+ ' + latex(term)
        elif term == 0:
            return ''
        else:
            return '- ' + latex(abs(term))
    else:
        coeff = term
        terms = []
        sign = '+'
    variable_part = ''
    if type(term/term.args[0]) == type(x+1):
        variable_part = term/term.args[0]
        variable_part = f'\\left({latex(variable_part)}\\right)'
    else:
        for term in terms:
            variable_part += ' ' + latex(term)
    return f'{sign} {coeff} {variable_part} '

def fmt_slope_style(sum):
    x = Symbol('x')
    if type(sum) == type(x + 1):
        out = fmt_slope_style_leading(sum.args[0])
        i = 1
        while i < len(sum.args):
            out += fmt_slope_style_trailing(sum.args[i])
            i += 1
    else:
        out = fmt_slope_style_leading(sum)
    return out

def commute_sum(sum):
    x = Symbol('x')
    if type(sum) == type(x + 1):
        first = sum.args[0]
        second = 0
        i = 1
        while i < len(sum.args):
            second += sum.args[i]
            i += 1
        return fmt_slope_style(second) + fmt_slope_style_trailing(first)
    else:
        return fmt_slope_style(sum)

def fmt_abs_value(string):
    count = 0
    i = 0
    while i < len(string):
        if string[i] == '|':
            if count % 2 == 0:
                string = string[:i] + 'Abs(' + string[i+1:]
            else:
                string = string[:i] + ")" + string[i+1:]
            count += 1
        i += 1
    return string

def sgn(x):
    if x > 0:
        return '+'
    elif x == 0:
        return ''
    else:
        return '-'

def tolerates(f1, f2, tolerance=0.0005, window=[-10,10], res=10):
    x_min = window[0]
    x_max = window[1]
    points = np.arange(x_min,x_max,res)
    close_enough = False
    for x in points:
        try:
            if abs(f1(x) - f2(x)) > tolerance:
                return False
        except ZeroDivisionError:
            pass
    return True


def sets_evaluate_equal(set1, set2):
    if len(set1) != len(set2):
        return False
    elif len(set1) == 0 and len(set2) == 0:
        return True
    else:
        element = list(set1)[0]
        for elem in set2:
            if element.equals(elem):
                new_set1 = set1.remove(element)
                new_set2 = set2.remove(elem)
                return sets_evaluate_equal(set1, set2)
        return False

def check_congruence_after_factoring_out_gcf(expr1, expr2):
    gcd1 = gcd(Poly(expr1).coeffs())
    gcd2 = gcd(Poly(expr2).coeffs())
    return gcd1 == gcd2 and simplify(expr1/gcd1) == simplify(expr2/gcd2)
