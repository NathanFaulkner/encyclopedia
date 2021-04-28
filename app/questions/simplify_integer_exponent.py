#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            alt_congruence_of_quotient,
                            congruence_of_quotient,
                            Monomial,
                            Quotient,
                            )



class SimplifyIntegerExponent(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        # print('seed', self.seed)
        self.difficulty = random.choice([0, 0, 1, 1, 2])
        # self.difficulty = 2
        def pow_neg_style(b, p):
            if p == 1:
                return str(b)
            else:
                return '{b}^{{{p}}}'.format(b=b,p=p)

        def basic_pow_term(**kwargs):
            if 'seed' in kwargs:
                seed = kwargs['seed']
            else:
                seed = random.random()
            # print('basic pow term seed', seed)
            random.seed(seed)
            if 'const_range' in kwargs:
                a, b = kwargs['const_range']
                A = random_non_zero_integer(a,b)
            else:
                A = random_non_zero_integer(-9,9)
            if 'const_power_range' in kwargs:
                a, b = kwargs['const_power_range']
                e_const = random.randint(a,b)
            else:
                e_const = random.randint(-9,9)
            if 'variables' in kwargs:
                variables = []
                for variable in kwargs['variables']:
                    variables.append(variable)
            else:
                n = random.randint(0,3)
                variables = []
                if n > 0:
                    variables.append('x')
                if n > 1:
                    variables.append('y')
                if n > 2:
                    variables.append('z')
            e = []
            if 'var_power_ranges' in kwargs:
                for r in kwargs['var_power_ranges']:
                    a, b = r
                    e.append(random.randint(a,b))
            else:
                for var in variables:
                    e.append(random.randint(-5,5))
            fmt_out = ''
            term = 1
            if A < 0:
                parens = random.choice([True, False])
                if parens and e_const != 1:
                    # print('parens:', A, e_const)
                    fmt_out += pow_neg_style('\\left({A}\\right)'.format(A=A), e_const)
                    term *= sy.Pow(A, e_const)
                    # print('term:', term)
                else:
                    fmt_out +=  pow_neg_style(A, e_const)
                    term *= -sy.Pow(abs(A), e_const)
            elif A != 1:
                fmt_out = pow_neg_style(A, e_const)
                term *= sy.Pow(A, e_const)
            elif A == -1:
                fmt_out += '-'
                term *= -1
            i = 0
            for var in variables:
                fmt_out += pow_neg_style(var, e[i])
                term *= sy.Pow(sy.Symbol(var), e[i])
                i += 1
            return {'fmt': fmt_out, 'sym': term}

        def make_term_depth_two(**kwargs):
            # print('depth_two kwargs:', kwargs)
            if 'seed' in kwargs:
                seed = kwargs['seed']
            else:
                seed = random.random()
            random.seed(seed)
            out = ''
            if kwargs.get('oper') in ['quot', 'prod', 'power', 'pow']:
                oper = kwargs['oper']
            else:
                oper = random.choice(['prod', 'quot', 'power'])
            #oper = 'power'
            if oper == 'prod':
                term1 = basic_pow_term(**kwargs)
                kwargs['seed'] = 1 - kwargs['seed']
                term2 = basic_pow_term(**kwargs)
                out += '\\left(' + term1['fmt'] + '\\right)'
                out += '\\left(' + term2['fmt'] + '\\right)'
                term = term1['sym']*term2['sym']
            if oper == 'quot':
                term1 = basic_pow_term(**kwargs)
                kwargs['seed'] = 1 - kwargs['seed']
                term2 = basic_pow_term(**kwargs)
                out += '\\frac{{{expr1}}}{{{expr2}}}'.format(expr1=term1['fmt'],expr2=term2['fmt'])
                term = term1['sym']/term2['sym']
            if oper == 'power' or oper == 'pow':
                term1 = basic_pow_term(**kwargs)
                random.seed(seed)
                power = random.randint(-5,5)
                out += '\\left({expr}\\right)^{{{power}}}'.format(expr=term1['fmt'], power=power)
                term = sy.Pow(term1['sym'], power)
            return {'fmt': out, 'sym': term}
            # second = random.choice(['prod', 'quot', 'power'])

        #a, b is range of integer powers, n is number of variables
        def make_term_depth_three(**kwargs):
            if 'seed' in kwargs:
                seed = kwargs['seed']
            else:
                seed = random.random()
            random.seed(seed)
            out = ''
            if kwargs == {}:
                oper3 = random.choice(['prod', 'quot', 'power'])
                term1 = make_term_depth_two()
                term2 = make_term_depth_two()
            elif 'oper3' in kwargs:
                oper3 = kwargs['oper3']
            else:
                oper3 = random.choice(['prod', 'quot', 'power'])
            if 'oper1' in kwargs:
                kwargs['oper'] = kwargs['oper1']
                term1 = make_term_depth_two(**kwargs)
            else:
                term1 = make_term_depth_two(**kwargs)
            if 'oper2' in kwargs:
                kwargs['oper'] = kwargs['oper2']
                kwargs['seed'] = 1 - kwargs['seed']
                term2 = make_term_depth_two(**kwargs)
            else:
                kwargs['seed'] = 1 - kwargs['seed']
                term2 = make_term_depth_two(**kwargs)
            if oper3 == 'prod':
                out += '\\left(' + term1['fmt'] + '\\right)'
                out += '\\left(' + term2['fmt'] + '\\right)'
                term = term1['sym'] * term2['sym']
            if oper3 == 'quot':
                out += '\\frac{{{expr1}}}{{{expr2}}}'.format(expr1=term1['fmt'],expr2=term2['fmt'])
                term = term1['sym'] / term2['sym']
            if oper3 == 'power':
                random.seed(seed)
                power = random.randint(-5,5)
                out += '\\left({expr}\\right)^{{{power}}}'.format(expr=term1['fmt'], power=power)
                term = sy.Pow(term1['sym'], power)
            return {'fmt': out, 'sym': term}
            # second = random.choice(['prod', 'quot', 'power'])

        def prep_for_math_print(string):
            return '\\(\\displaystyle {string}\\)'.format(string=string)

        def compose_terms_for_latex_format(*args, **kwargs):
            # print(kwargs)
            if 'seed' in kwargs:
                seed = kwargs['seed']
            else:
                seed = random.random()
            random.seed(seed)
            terms = args
            out = ''
            if kwargs == {}:
                oper = random.choice(['quot', 'prod', 'power'])
            elif 'oper' in kwargs:
                oper = kwargs['oper']
                if 'power' in kwargs:
                    power = kwargs['power']
                else:
                    power = random.randint(-6,6)
            if oper == 'prod':
                if kwargs['parens']:
                    out += '\\left(' + terms[0]['fmt'] + '\\right)'
                    out += '\\left(' + terms[1]['fmt'] + '\\right)'
                else:
                    out += terms[0]['fmt'] + terms[1]['fmt']
                term = terms[0]['sym'] * terms[1]['sym']
            if oper == 'quot' or oper == 'div':
                out += '\\frac{{{expr1}}}{{{expr2}}}'.format(expr1=terms[0]['fmt'], expr2=terms[1]['fmt'])
                term = terms[0]['sym'] / terms[1]['sym']
            if oper == 'power' or oper == 'pow':
                out += '\\left({expr}\\right)^{{{power}}}'.format(expr=terms[0]['fmt'], power=power)
                term = sy.Pow(terms[0]['sym'], power)
            return {'fmt': out, 'sym': term}

        if self.difficulty == 0:
            kwargs = {'const_range': [-10,10],
                    'const_power_range':[-5,-1],
                    'variables' : ['x'],
                    'seed': self.seed}
            term = basic_pow_term(**kwargs)
        if self.difficulty == 1:
            kwargs = {'const_range': [-10,10],
                    'const_power_range':[1, 1],
                    'variables': random.choice([['x','y'], ['y', 'z'], ['x', 'y', 'z']]),
                    'seed': self.seed}
            term = make_term_depth_two(**kwargs)
        if self.difficulty == 2:
            kwargs = {'const_range': [-10,10],
                    'const_power_range':[1, 1],
                    'variables': random.choice([['x','y'], ['y', 'z']]),
                    'seed': self.seed,
                    }
            oper1, oper2, oper3 = random.choice([['prod', None, 'quot'],
                                                [None, 'prod', 'quot'],
                                                [None, 'pow', 'prod'],
                                                [None, 'pow', 'quot'],
                                                ['pow', None, 'quot'],
                                                [None, 'prod', 'prod'],
                                                ['prod', None, 'pow'],
                                                ['quot', None, 'pow']])
            if oper1 is None:
                term1 = basic_pow_term(**kwargs)
            else:
                kwargs['oper'] = oper1
                term1 = make_term_depth_two(**kwargs)
            if oper2 is None:
                kwargs['seed'] = kwargs['seed']*7 % 1
                term2 = basic_pow_term(**kwargs)
            else:
                kwargs['oper'] = oper2
                kwargs['seed'] = kwargs['seed']*7 % 1
                term2 = make_term_depth_two(**kwargs)
            kwargs['oper'] = oper3
            terms = [term1, term2]
            kwargs['parens'] = False
            term = compose_terms_for_latex_format(*terms, **kwargs)
        # term  = sy.Pow(2, -3, evaluate=False)
        self.answer = term['sym']
        # print('self.answer:', self.answer)
        self.format_answer = f'\( {sy.latex(self.answer)}\)'
        self.format_given = f"""
        \\[
            {term['fmt']}
        \\]"""

        self.prompt_single = f"""Simplify.  In particular, rewrite the term without
        the use of any negative exponents and cancel common factors wherever possible."""

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    # def non_zero_integer(a,b):
    #     n = 0
    #     while n == 0:
    #         n = random.randint(a,b)
    #     return n



    name = 'Simplify Integer Exponents'
    module_name = 'simplify_integer_exponent'


    prompt_multiple = """TBA"""

    # further_instruction = """
    # Just enter the final expression.  You shouldn't enter
    # "y =" or "f(x) = ".
    # """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('**', '^')
        user_quotient = Quotient(user_answer)
        user_numer, user_denom = [user_quotient.numer.normal_form, user_quotient.denom.normal_form]
        # print('user', user_numer, user_denom)
        if isinstance(self.answer, sy.Pow):
            ans_numer = '1'
            ans_denom = '1' + str(self.answer.args[0]) + '^' + str(abs(self.answer.args[1]))
            # print('My fault!')
        else:
            ans_quotient = Quotient(str(self.answer))
            ans_numer, ans_denom = [ans_quotient.numer.normal_form, ans_quotient.denom.normal_form]
        # print('ans', ans_numer, ans_denom)
        return user_numer == ans_numer and user_denom == ans_denom
        # user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        # if self.non_positive_power(user_answer):
        #     return False
        # answer = parse_expr(str(self.answer), transformations=transformations, evaluate=False)
        # # alt = sy.Add(user_answer, -answer)
        # # print('alt', alt)
        # # print(alt == 0)
        # print(user_answer, type(user_answer))
        # print(answer, type(answer))
        # return alt_congruence_of_quotient(user_answer, answer, evaluate=False)
        # return user_answer == answer

    # @staticmethod
    # def non_positive_power(expr):
    #     if expr.args == ():
    #         return False
    #     elif isinstance(expr, sy.Pow):
    #         # print('expr', expr, 'power', expr.args[1])
    #         if expr.args[1] <= 0:
    #             return True
    #     else:
    #         return any([SimplifyIntegerExponent.non_positive_power(arg) for arg in expr.args])

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('**', '^')
        user_quotient = Quotient(user_answer)
        fmt = user_quotient.fmt_for_tex
        # print(repr(user_answer))
        # if SimplifyIntegerExponent.non_positive_power(user_answer):
        #     return unchanged
        return f'\({fmt}\)'

    @staticmethod
    def validator(user_answer):
        try:
            pass
            # user_answer = user_answer.lower()
            # user_answer = user_answer.replace('**', '^')
            # user_quotient = Quotient(user_answer)
            # user_numer, user_denom = [user_quotient.numer.normal_form, user_quotient.denom.normal_form]
            # fmt = user_quotient.fmt_for_tex
        except:
            raise SyntaxError


Question_Class = SimplifyIntegerExponent
prob_type = 'math_blank'
