#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import Question, random_non_zero_integer



class SimplifyIntegerExponent(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        def non_zero_integer(a,b):
            n = 0
            while n == 0:
                n = random.randint(a,b)
            return n

        def pow_neg_style(b,p):
            if p == 1:
                return str(b)
            else:
                return '{b}^{{{p}}}'.format(b=b,p=p)

        def basic_pow_term(**kwargs):
            if 'const_range' in kwargs:
                a, b = kwargs['const_range']
                A = non_zero_integer(a,b)
            else:
                A = non_zero_integer(-9,9)
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
            out = ''
            if A < 0:
                parens = random.choice([True, False])
                if parens:
                    out += pow_neg_style('({A})'.format(A=A), e_const)
                else:
                    out +=  pow_neg_style(A, e_const)
            elif A != 1:
                out = pow_neg_style(A, e_const)
            i = 0
            for var in variables:
                out += pow_neg_style(var, e[i])
                i += 1
            return out

        def make_term_depth_two(n, a, b, **kwargs):
            out = ''
            if kwargs == {}:
                oper = random.choice(['prod', 'quot', 'power'])
            elif kwargs['oper'] in ['quot', 'prod', 'power']:
                oper = kwargs['oper']
            else:
                oper = random.choice(['prod', 'quot', 'power'])
            #oper = 'power'
            if oper == 'prod':
                out += '\\left(' + basic_pow_term(n,a,b) + '\\right)'
                out += '\\left(' + basic_pow_term(n,a,b) + '\\right)'
            if oper == 'quot':
                expr1 = basic_pow_term(n,a,b)
                expr2 = basic_pow_term(n,a,b)
                out += '\\frac{{{expr1}}}{{{expr2}}}'.format(expr1=expr1,expr2=expr2)
            if oper == 'power':
                expr1 = basic_pow_term(n,a,b)
                power = random.randint(a,b)
                out += '\\left({expr}\\right)^{power}'.format(expr=expr1, power=power)
            return out
            second = random.choice(['prod', 'quot', 'power'])

        #a, b is range of integer powers, n is number of variables
        def make_term_depth_three(n, a, b, **kwargs):
            out = ''
            if kwargs == {}:
                oper3 = random.choice(['prod', 'quot', 'power'])
                term1 = make_term_depth_two(n,a,b)
                term2 = make_term_depth_two(n,a,b)
            elif 'oper3' in kwargs:
                oper3 = kwargs['oper3']
            else:
                oper3 = random.choice(['prod', 'quot', 'power'])
            if 'oper1' in kwargs:
                oper1 = kwargs['oper1']
                term1 = make_term_depth_two(n,a,b,oper=oper1)
            else:
                term1 = make_term_depth_two(n,a,b)
            if 'oper2' in kwargs:
                oper2 = kwargs['oper2']
                term2 = make_term_depth_two(n,a,b,oper=oper2)
            else:
                term2 = make_term_depth_two(n,a,b)
            if oper3 == 'prod':
                out += '\\left(' + term1 + '\\right)'
                out += '\\left(' + term2 + '\\right)'
            if oper3 == 'quot':
                out += '\\frac{{{expr1}}}{{{expr2}}}'.format(expr1=term1,expr2=term2)
            if oper3 == 'power':
                power = random.randint(a,b)
                out += '\\left({expr}\\right)^{power}'.format(expr=term1, power=power)
            return out
            second = random.choice(['prod', 'quot', 'power'])

        def prep_for_math_print(string):
            return '\\(\\displaystyle {string}\\)'.format(string=string)

        def compose_terms_for_latex_format(*args, **kwargs):
            terms = []
            for arg in args:
                terms.append(arg)
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
                out += '\\left(' + terms[0] + '\\right)'
                out += '\\left(' + terms[1] + '\\right)'
            if oper == 'quot' or oper == 'div':
                out += '\\frac{{{expr1}}}{{{expr2}}}'.format(expr1=terms[0],expr2=terms[1])
            if oper == 'power' or oper == 'pow':
                out += '\\left({expr}\\right)^{{{power}}}'.format(expr=terms[0], power=power)
            return out
        kwargs = {'const_range': [-10,10],
          'const_power_range':[-5,-1],
          'variables' : []
          }
        term = basic_pow_term(**kwargs)
        term  = sy.Pow(2, -3, evaluate=False)
        self.answer = term
        self.format_answer = f'\( {sy.latex(self.answer)}\)'
        self.format_given = f"""
        \\[
            {sy.latex(term)}
        \\]"""

        self.prompt_single = f"""Simplify."""

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

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
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        alt = sy.Add(user_answer, -sy.Symbol('x'), evaluate=False)
        print('alt', alt)
        print(alt == 0)
        print(user_answer)
        print(self.answer)
        return self.answer == user_answer

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return f'\({sy.latex(user_answer)}\)'

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError


Question_Class = SimplifyIntegerExponent
prob_type = 'math_blank'
