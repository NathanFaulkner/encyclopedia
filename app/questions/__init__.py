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
            'long_division_of_polynomials',
            'long_division_of_polynomials_harder',
            'synthetic_division_of_polynomials',
            'synthetic_division_of_polynomials_harder',
            'complete_factorization_level1',
            'complete_factorization_level1_nice_factors',
            'complete_factorization_level1_three_factors',
            'complete_factorization_level1_three_nice_factors',
            'imaginary_element_level1',
            'imaginary_element_level2',
            'imaginary_element_level3',
            'imaginary_element_level4',
            'quadratic_can_be_imaginary',
            'quadratic_force_imaginary',
            'quadratic_pattern_for_photomath',
            'polynomial_end_behavior',
            'polynomial_curve_sketching',
            'polynomial_curve_to_equation',
            'rationals_multiply_or_divide',
            'rationals_add_or_subtract',
            'rationals_add_or_subtract_type2',
            'rationals_messy',
            'solving_equation_with_rational_linear',
            'solving_equation_with_rational_quadratic',
            'solving_equation_with_rational_linear_type2',
            'graph_hyperbola', 'graph_hyperbola_to_equation',
            'simplify_integer_exponent',
            'simplify_rational_exponent_just_expo',
            'simplify_like_base_product_rational_expo',
            'simplify_like_base_quotient_rational_expo',
            'simplify_rational_expo_to_rational_expo',
            'simplify_by_combining_product_into_one_radical',
            'simplify_by_combining_quotient_into_one_radical',
            'simplify_rational_exponent_just_expo_of_quotient',
            'reduce_radical',
            'solve_power_equation_level1',
            'solve_power_equation_level2',
            'graph_sqrt', 'graph_sqrt_to_equation',
            'graph_cube_function', 'graph_cubic_to_equation',
            'graph_cbrt', 'graph_cbrt_to_equation',
            'graph_exp', 'graph_exp_to_equation',
            'graph_log',
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
    try:
        gcd1 = gcd(Poly(expr1).coeffs())
        gcd2 = gcd(Poly(expr2).coeffs())
        return gcd1 == gcd2 and simplify(expr1/gcd1) == simplify(expr2/gcd2)
    except polys.polyerrors.GeneratorsNeeded:
        return expr1 == expr2

def safe_gcf(expr):
    try:
        return gcd(Poly(expr).coeffs())
    except polys.polyerrors.GeneratorsNeeded:
        return expr

def get_coeff(expr):
    poly = Poly(expr)
    gcf = gcd(poly.coeffs())
    lc = LC(poly)
    # print('lc', lc)
    if lc < 0:
        gcf = -gcf
    if gcf.is_number:
        return gcf
    else:
        return 1

def factor_negative_out_from_denominator(quotient_expr):
    out = -1
    for term in quotient_expr.args:
        if term.func == (Symbol('x')**2).func and term.args[1] == -1:
            denom = term.args[0]
            new_denom = -denom
            out *= new_denom**(-1)
        else:
            out *= term
    return out

def get_numer_denom(quot_expr, evaluate=True):
    if quot_expr.args == ():
        # print('it was me!')
        return [quot_expr, 1]
    numer = 1
    denom = 1
    if quot_expr.func == (Symbol('x')**2).func and quot_expr.args[1] < 0:
        if quot_expr[args][0].is_number:
            denom *= quot_expr.args[0]**abs(quot_expr.args[1])
            # print('denom')
        else:
            denom *= Pow(quot_expr.args[0], abs(quot_expr.args[1]), evaluate=evaluate)
    else: #assumes that quot_expr is Mul
        # numer *= quot_expr
        for term in quot_expr.args:
            # print('get_stuff:', term, term.func)
            if term.func == (Symbol('x')**2).func and term.args[1] < 0:
                # print('it was me!')
                if term.args[0].is_number:
                    # print('it was me!')
                    denom *= term.args[0]**abs(term.args[1])
                    # print('denom', denom)
                else:
                    denom *= Pow(term.args[0], abs(term.args[1]), evaluate=evaluate)
            else:
                # print('it was me!')
                numer *= term
    return [numer, denom]

def congruence_of_quotient(quot1, quot2, evaluate=True):
    numer1, denom1 = get_numer_denom(quot1, evaluate=evaluate)
    print('QUOT1', numer1, denom1)
    numer2, denom2 = get_numer_denom(quot2, evaluate=evaluate)
    print('QUOT2', numer2, denom2)
    gcf_numer1, gcf_denom1 = [safe_gcf(numer1), safe_gcf(denom1)]
    gcf_numer2, gcf_denom2 = [safe_gcf(numer2), safe_gcf(denom2)]
    nec = gcf_numer1/gcf_denom1 == gcf_numer2/gcf_denom2
    nec1 = (numer1/gcf_numer1)/(denom1/gcf_denom1) == (numer2/gcf_numer2)/(denom2/gcf_denom2)
    nec2 = (numer1/gcf_numer1)/(denom1/gcf_denom1) == (-numer2/gcf_numer2)/(-denom2/gcf_denom2)
    nec3 = (factor(numer1/gcf_numer1)/factor(denom1/gcf_denom1)) == (factor(numer2/gcf_numer2)/factor(denom2/gcf_denom2))
    nec4 = (factor(numer1/gcf_numer1)/factor(denom1/gcf_denom1)) == (factor(-numer2/gcf_numer2)/factor(-denom2/gcf_denom2))
    # nec = Mul(gcf_numer1, Pow(gcf_denom1, -1)) == Mul(gcf_numer2, Pow(gcf_denom2, -1))
    # nec1 = Mul(numer1/gcf_numer1),Pow(denom1/gcf_denom1), -1)) == (numer2/gcf_numer2)/(denom2/gcf_denom2)
    # nec2 = (numer1/gcf_numer1)/(denom1/gcf_denom1) == (-numer2/gcf_numer2)/(-denom2/gcf_denom2)
    # nec3 = (factor(numer1/gcf_numer1)/factor(denom1/gcf_denom1)) == (factor(numer2/gcf_numer2)/factor(denom2/gcf_denom2))
    # nec4 = (factor(numer1/gcf_numer1)/factor(denom1/gcf_denom1)) == (factor(-numer2/gcf_numer2)/factor(-denom2/gcf_denom2))
    return nec and (nec1 or nec2 or nec3 or nec4)

def alt_congruence_of_quotient(quot1, quot2, evaluate=False):
    numer1, denom1 = get_numer_denom(quot1, evaluate=False)
    print('QUOT1', numer1, denom1)
    numer2, denom2 = get_numer_denom(quot2, evaluate=False)
    print('QUOT2', numer2, denom2)
    gcf_numer1, gcf_denom1 = [safe_gcf(numer1), safe_gcf(denom1)]
    gcf_numer2, gcf_denom2 = [safe_gcf(numer2), safe_gcf(denom2)]
    # nec = gcf_numer1/gcf_denom1 == gcf_numer2/gcf_denom2
    # nec1 = (numer1/gcf_numer1)/(denom1/gcf_denom1) == (numer2/gcf_numer2)/(denom2/gcf_denom2)
    # nec2 = (numer1/gcf_numer1)/(denom1/gcf_denom1) == (-numer2/gcf_numer2)/(-denom2/gcf_denom2)
    # nec3 = (factor(numer1/gcf_numer1)/factor(denom1/gcf_denom1)) == (factor(numer2/gcf_numer2)/factor(denom2/gcf_denom2))
    # nec4 = (factor(numer1/gcf_numer1)/factor(denom1/gcf_denom1)) == (factor(-numer2/gcf_numer2)/factor(-denom2/gcf_denom2))
    nec = gcf_numer1/gcf_denom1 == gcf_numer2/gcf_denom2
    rhs1 = Mul(Mul(numer1/gcf_numer1, evaluate=False), Pow(Mul(denom1/gcf_denom1, evaluate=False), -1, evaluate=False), evaluate=False)
    lhs1 = Mul(Mul(numer2/gcf_numer2, evaluate=False), Pow(Mul(denom2/gcf_denom2, evaluate=False), -1, evaluate=False), evaluate=False)
    lhs2 = Mul(Mul(-numer2/gcf_numer2, evaluate=False), Pow(Mul(-denom2/gcf_denom2, evaluate=False), -1, evaluate=False), evaluate=False)
    nec1 = rhs1 == lhs1
    nec2 = rhs1 == lhs2
    print(nec, nec1, nec2)
    print(rhs1, lhs1, lhs2)
    return nec and (nec1 or nec2)

def basic_parse_and_check(user_answer, answer):
    user_answer = user_answer.lower()
    user_answer = user_answer.replace('^', '**')
    user_answer = parse_expr(user_answer, transformations=transformations)
    return answer == user_answer


def list_integer_factors(n):
    factors = []
    i = 1
    while i <= abs(n):
        if n % i == 0:
            factors.append(i)
        i += 1
    return factors

def get_integer_divisors(n):
    divisors = []
    for i in range(1,n+1):
        if n/i % 1 == 0:
            divisors.append(i)
    return divisors

def apply_positive_integer_powers(expr):
    if isinstance(expr, Pow) and expr.args[1] > 0 and isinstance(expr.args[1], Integer):
        return simplify(expr)
    elif expr.args == ():
        return expr
    else:
        return expr.func(*(apply_positive_integer_powers(arg) for arg in expr.args), evaluate=False)

def drop_redundant_abs(expr, evaluate=True):
    # print(expr)
    if isinstance(expr, Pow) and expr.args[1] % 2 == 0:
        # print('even pow')
        pow = expr.args[1]
        arg = expr.args[0]
        if isinstance(arg, Abs):
            inner = arg.args[0]
            return Pow(inner, pow, evaluate=evaluate)
        else:
            return expr
    elif expr.args == ():
        # print('empty ?', expr)
        return expr
    else:
        # print('recurrence')
        return expr.func(*(drop_redundant_abs(arg) for arg in expr.args), evaluate=evaluate)

def is_rational_function(expr):
    out = True
    if isinstance(expr, Mul):
        for arg in expr.args:
            if isinstance(arg, Pow):
                if arg.args[1] % 1 != 0 or not arg.args[0].is_polynomial():
                    out = False
            elif not arg.is_polynomial():
                out = False
    else:
        out = sympify(expr).is_polynomial()
    return out


def simplify_for_long_division(expr):
    # print(expr, expr.args)
    if is_rational_function(expr):
        numer, denom = get_numer_denom(expr)
        if degree(numer) < degree(denom):
            return simplify(expr)
        else:
            return expr
    elif expr.args == ():
        return expr
    else:
        return expr.func(*(simplify_for_long_division(arg) for arg in expr.args))


def commute_AbsMul_to_MulAbs(expr, evaluate=True):
    if isinstance(expr, Abs):
        inner = expr.args[0]
        if isinstance(inner, Mul):
            factors = inner.args
            factors = (Abs(factor) for factor in factors)
            return Mul(*factors, evaluate=evaluate)
        elif isinstance(inner, Pow):
            return Pow(Abs(inner.args[0]), inner.args[1], evaluate=evaluate)
        else:
            return expr
    elif expr.args == ():
        return expr
    else:
        return expr.func(*(commute_AbsMul_to_MulAbs(arg) for arg in expr.args), evaluate=evaluate)

def has_rational_power(expr):
    if isinstance(expr, Pow) and expr.args[1].is_number:
        if expr.args[1] % 1 != 0:
            return True
    else:
        # print('recurrence')
        return any([has_rational_power(arg) for arg in expr.args])

def split_at_comma_not_in_parens(s):
    # print('hello!')
    paren_counter = 0
    i = 0
    while i < len(s):
        if s[i] == '(':
            paren_counter += 1
        elif s[i] == ')':
            paren_counter -= 1
        if s[i] == ',' and paren_counter == 0:
            s = s[:i] + ';' + s[i+1:]
        elif s[i] == ';':
            raise TypeError('A string containing a semi-colon is not allowed here.')
        i += 1
    return s.split(';')


class Monomial():
    def __init__(self, s):
        # print('input to Monomial', s)
        self.input = s.replace('**', '^')
        self.quick_check()
        self.variables = set([a for a in self.input if a.isalpha()])
        self.set_normal_form()

        # self.set_variables_and_constants()
    def quick_check(self):
        if self.input == '':
            raise TypeError('An empty string is not a monomial')
        if self.input[0] == '-':
            self.is_negative = True
        else:
            self.is_negative = False
        allowed = 'abcdefghijklmnopqrstuvwxyz'
        allowed = allowed + allowed.upper()
        allowed += '1234567890-*^()'
        if any([a not in allowed for a in self.input]):
            raise TypeError('You have used illegal characters.')

    def check_for_simplified(self):
        letters = sorted([a for a in self.input if a.isalpha()])
        if sorted(list(set(letters))) == letters:
            return True
        return False

    def set_normal_form(self):
        m = self.input
        coeff = 1
        # l = len(m)
        powers = {}
        for a in self.variables:
            powers[a] = 0
        # for i, a in enumerate(self.input):
        #     if a in self.variables:
        #         if i == len(self.input) - 1:
        #             powers[a] += 1
        #         elif self.input[i+1] == '^':
        #             if self.input[i+2].isalpha():
        #                 powers[a] += sy.Symbol(self.input[i+1])
        #             elif self.input[i+2].isnumeric():
        #                 start = i + 2
        #                 j = 1
        #                 while start + j < len(self.input) and self.input[start + j].isnumeric():
        #                     j += 1
        #                 stop = start + j
        #                 n = int(self.input[start:stop])
        #                 powers[a] += n
        #             else:
        #                 raise SyntaxError(f'{self.input} is not a well-formed monomial')
        #         else:
        #             powers[a] += 1
        i = 0
        while i < len(m):
            # print(i, m[i])
            if m[i] in self.variables:
                if i == len(m) - 1:
                    powers[m[i]] += 1
                    i += 1
                elif m[i+1] == '^':
                    if m[i+2].isalpha():
                        powers[m[i]] += Symbol(m[i+2])
                        i = i + 2
                    elif m[i+2].isnumeric():
                        start = i + 2
                        j = 1
                        while start + j < len(self.input) and self.input[start + j].isnumeric():
                            j += 1
                        stop = start + j
                        n = int(self.input[start:stop])
                        powers[m[i]] += n
                        i = stop
                    else:
                        raise SyntaxError(f'"{self.input}" is not a well-formed monomial')
                else:
                    powers[m[i]] += 1
                    i += 1
            elif m[i].isnumeric():
                start = i
                j = 1
                while start + j < len(m) and m[start + j].isnumeric():
                    j += 1
                stop = start + j
                n = int(m[start:stop])
                if stop == len(m) or m[stop] != '^':
                    coeff *= n
                else:
                    # print('My fault!')
                    start = stop + 1
                    j = 1
                    while start + j < len(m) and m[start + j].isnumeric():
                        j += 1
                    stop = start + j
                    p = int(m[start:stop])
                    coeff *= n**p
                i = stop
            elif m[i] == '*':
                if i == 0 or i == len(m)-1:
                    raise SyntaxError(f'"{self.input}" is not a well-formed monomial')
                elif m[i+1] == '*':
                    raise SyntaxError(f'"{self.input}" is not a well-formed monomial')
                else:
                    i += 1
            elif m[i] == '(':
                start = i+1
                j = 1
                while start + j < len(m) and m[start + j] != ')':
                    j += 1
                if start + j == len(m):
                    raise SyntaxError(f'"{self.input}" is not a well-formed monomial')
                stop = start + j
                submonomial = Monomial(m[start:stop])
                for key in submonomial.powers:
                    powers[key] += submonomial.powers[key]
                coeff *= submonomial.coeff
                i = stop + 2
            elif m[i] == '-':
                i += 1
            else:
                raise SyntaxError(f'"{self.input}" is not a well-formed monomial')
        self.coeff = coeff
        self.powers = powers
        if self.is_negative:
            normal_form = '-'
            normal_form_tex = '-'
        else:
            normal_form = ''
            normal_form_tex = ''
        normal_form += str(coeff)
        if coeff in [1, -1]:
            if self.variables == set():
                normal_form_tex += str(coeff)
        else:
            normal_form_tex += str(coeff)
        for x in sorted(list(self.variables)):
            normal_form += x + '^' + str(powers[x])
            if powers[x] == 0:
                pass
            elif powers[x] == 1:
                normal_form_tex += x
            else:
                normal_form_tex += x + '^{' + str(powers[x]) + '}'
        self.normal_form = normal_form
        self.normal_form_tex = normal_form_tex

    # def check_normal_form(self):
    #     i = 0
    #     while i < len(self.input):
    #         if self.input[0].is

#
#
#
#     def parse_monomial(s):
#         s = s.replace('**', '^')
#         # a recursive subroutine will need to be inserted here to handle parens
#         powers = {}
#         i = 0
#         number = 1
#         while i < len(s):
#             if not s[i].isalnum() and s[i] != '^' and s[i] != '*' and s[i] != '-':
#                 raise TypeError
#             if s[i] == '^':
#                 j = 1
#                 if not s[i-j].isalnum():
#                     raise SyntaxError
#                 elif s[i-j].isalpha():
#                     base = s[i-j]
#                 else:
#                     while s[i-j].isnumeric() and j < i:
#                         j += 1
#                     base = int(s[i-j:i])
#                 j = 1
#                 if i == len(s) - 1:
#                     raise SyntaxError
#                 if s[i+j] == '-':
#                     raise TypeError
#                 else:
#                     while  i + j < len(s) and s[i+j].isnumeric():
#                         j += 1
#                     expo = int(s[i+1:i+j])
#                 prev = powers.get(str(base)) or 0
#                 powers[str(base)] = expo + prev
#             i += 1
#         return powers


class Quotient():
    def __init__(self, s):
        self.input = s.replace('**', '^')
        self.quotient = Quotient.parse_quotient(self.input)
        self.numer, self.denom = self.quotient
        # print(f'Quotient is {self.numer.normal_form}/{self.denom.normal_form}')
        if self.denom.normal_form == '1':
            self.fmt_for_tex = self.numer.normal_form_tex
        else:
            self.fmt_for_tex = f'\\frac{{ {self.numer.normal_form_tex} }}{{ {self.denom.normal_form_tex} }}'

    @staticmethod
    def parse_quotient(s):
        counter = s.count('/')
        if counter > 1:
            raise TypeError(s + ' is not a single quotient.')
        elif counter == 1:
            i = s.find('/')
            if s[i+1] == '(':
                start = i+2
                j = 1
                while start + j < len(s) and s[start+j] != ')':
                    j += 1
                stop = start + j
                denom = Monomial(s[start:stop])
                stop += 1
            elif s[i+1].isalpha():
                start = i + 1
                if i + 2 < len(s) and s[i+2] == '^':
                    # print('My Fault!!!')
                    # print('character', s[i+3], s[i+3].isnumeric())
                    if s[i+3].isalpha():
                        stop = i + 4
                    elif s[i+3].isnumeric():
                        # print('My Fault!!!')
                        e_start = i+3
                        j = 1
                        while e_start + j < len(s) and s[e_start+j].isnumeric():
                            j += 1
                        stop = e_start + j
                    else:
                        raise SyntaxError(f'{s} is not a well-formed quotient.')
                else:
                    stop = i + 2
                denom = Monomial(s[start:stop])
            elif s[i+1].isnumeric():
                # print('My Fault!!! The denominator is numeric.')
                start = i + 1
                j = 1
                while start + j < len(s) and s[start+j].isnumeric():
                    j += 1
                stop = start + j
                if stop < len(s) and s[stop] == '^':
                    # print('My Fault!!! Expo on coeff in denominator was detected.')
                    # print('character', s[i+3], s[i+3].isnumeric())
                    e_start = stop + 1
                    if s[e_start].isalpha():
                        e_stop = e_start + 1
                    elif s[e_start].isnumeric():
                        # print('My Fault!!!')
                        j = 1
                        while e_start + j < len(s) and s[e_start+j].isnumeric():
                            j += 1
                        e_stop = e_start + j
                    else:
                        raise SyntaxError(f'{s} is not a well-formed quotient.')
                    stop = e_stop
                    denom = Monomial(s[start:stop])
                else:
                    denom = Monomial(s[start:stop])
            else:
                raise SyntaxError(f'{s} is not an admissiable quotient')
            numer = Monomial(s[:i] + s[stop:])
        else:
            numer = Monomial(s)
            denom = Monomial('1')
        return [numer, denom]


# class AtomicTerm:
#     """
#     A good option to add would be to express how this should be displayed.
#     """
#     def __init__(self, input):
#         if isinstance(input, BasicOperation) and input.arity == 0:
#             self.type = 'constant'
#             self.symbol = input.symbol
#         elif type(input) == str and input.isalpha():
#             self.type = 'variable'
#             self.symbol = input
#         else:
#             raise TypeError(f'{input} is not admissable as an atomic term.')

class Variable:
    def __init__(self, input):
        if type(input) != str:
            raise TypeError('Variable takes one argument, the symbol for the variable.')
        self.symbol = input

class BasicOperation:
    def __init__(self, symbol, arity):
        if type(symbol) != str:
            raise TypeError('The first argument for Basic Operation should be a string: the symbol for the operation.')
        self.symbol = symbol
        if type(arity) != int:
            raise TypeError('The second argument for Basic Operation should be a natural number, the arity of the operation.')
        self.arity = arity

class Term:
    def __init__(self, *args):
        if len(args) == 0:
            raise TypeError('A term cannot be empty.  Use PartialTerm instead.')
        if len(args) == 1:
            if isinstance(args[0], BasicOperation) and args[0].arity == 0:
                self.term = args[0]
            elif isinstance(args[0], Variable):
                self.term = args[0]
            else:
                raise SyntaxError('You did not provide a well-formed term.')
        else:
            if not isinstance(args[0], BasicOperation):
                raise SyntaxError('You did not provide a well-formed term.')
            else:
                self.basic_operation = args[0]
                for arg in args:
                    if isinstance(arg, Term):
                        pass
                    else:
                        arg = Term(arg)
