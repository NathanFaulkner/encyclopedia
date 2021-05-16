#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            sets_evaluate_equal,
                            check_congruence_after_factoring_out_gcf,
                            get_numer_denom,
                            congruence_of_quotient)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class RationalsMultiplyOrDivide(Question):
    """
    The given is an expanded form of

    \\[

    \\]

    The directions are to factor.
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        x = sy.Symbol('x')

        zs_for_cancellation = []
        for i in range(3):
            zs_for_cancellation.append(random.randint(-9,9))

        #print(zs_for_cancellation)

        extra_zs = [random.randint(-9,9) for i in range(2)]

        #print('extra zs', extra_zs)


        extra_as = [0,0]
        for i in range(2):
            a = 0
            while a == 0:
                a = random.randint(-6,6)
            extra_as[i] = a
        extra_as += [1,1]

        random.shuffle(extra_as)
        #print(extra_as)

        numerator_zs = extra_zs[:1] + zs_for_cancellation

        #print(numerator_zs)

        random.shuffle(numerator_zs)

        #print(numerator_zs)

        denominator_zs = extra_zs[-1:] + zs_for_cancellation
        #print(denominator_zs)
        random.shuffle(denominator_zs)


        numerator1 = extra_as[0]
        denominator1 = extra_as[1]
        numerator2 = extra_as[2]
        denominator2 = extra_as[3]
        for i in range(2):
            numerator1 *= (x-numerator_zs[i])
            denominator1 *= (x-denominator_zs[i])
            numerator2 *= (x-numerator_zs[3-i])
            denominator2 *= (x-denominator_zs[3-i])

        #print(numerator1, numerator2, denominator1, denominator2)

        operator_symb = random.choice(['\\cdot', '\\div'])

        if operator_symb == '\\cdot':
        	prob = '\\frac{{{n}}}{{{d}}}'.format(n=sy.latex(sy.expand(numerator1)), d=sy.latex(sy.expand(denominator1)))
        	prob += operator_symb
        	prob +='\\frac{{{n}}}{{{d}}}'.format(n=sy.latex(sy.expand(numerator2)), d=sy.latex(sy.expand(denominator2)))
        else:
        	prob = '\\frac{{{n}}}{{{d}}}'.format(n=sy.latex(sy.expand(numerator1)), d=sy.latex(sy.expand(denominator1)))
        	prob += operator_symb
        	prob +='\\frac{{{d}}}{{{n}}}'.format(n=sy.latex(sy.expand(numerator2)), d=sy.latex(sy.expand(denominator2)))

        self.answer = sy.simplify(numerator1*numerator2/denominator1/denominator2)
        # print(self.answer)
        # expr1 = sy.factor(A+B1)*(A+B2)
        # expr2 = (A+B1)*sy.factor(A+B2)
        # expr3 = sy.factor((A+B1)*(A+B2))
        # self.answers = [expr, expr1, expr2, expr3]
        self.format_answer = f'\( {sy.latex(self.answer)}\)'

        self.format_given = f"\\[{prob}\\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Rationals: Multiply or Divide'
    module_name = 'rationals_multiply_or_divide'

    prompt_single = """Carry out the indicated operation and simplify (reduce to lowest terms)."""
    prompt_multiple = """TBA"""

    # further_instruction = """
    # """

    loom_link = "https://www.loom.com/share/80802f0dbd4a455eac003e5d20be1508?sharedAppSource=personal_library"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        if 'simplify' in user_answer:
            return False
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        user_numer, user_denom = get_numer_denom(user_answer)
        print(user_numer, user_denom)
        if '+' not in str(user_denom) and '-' not in str(user_denom):
            if isinstance(user_numer, sy.Add):
                new = 0
                for arg in user_numer.args:
                    new += arg/user_denom
                user_answer = new
        # if not (isinstance(user_answer, sy.core.power.Pow) or isinstance(user_answer, sy.core.mul.Mul)):
        #     return False
        # if isinstance(user_answer, sy.core.mul.Mul):
        #     user_factors = user_answer.args
        #     user_factors = [sy.factor(factor) for factor in user_factors]
        #     check_factors = sets_evaluate_equal(set(self.answer.args), set(user_factors))
        # constraints = [check_factors,
        #                 type(self.answer) == type(user_answer)]
        # print([type(elem) for elem in self.answer.args], [type(elem) for elem in user_answer.args])
        # print(type(self.answer), type(user_answer))
        # print(constraints)
        # print([answer for answer in self.answers])
        # return any([sets_evaluate_equal(set(answer.args), set(user_answer.args)) for answer in self.answers])
        # print(type(user_answer), type(self.answer))
        # return (isinstance(user_answer, sy.core.power.Pow) or isinstance(user_answer, sy.core.mul.Mul)) and sy.expand(user_answer) == sy.expand(self.answer)
        # return user_answer == self.answer
        answer = parse_expr(str(self.answer), transformations=transformations)
        # ans_numer, ans_denom = get_numer_denom(answer)
        # user_numer, user_denom = get_numer_denom(user_answer)
        # sufficient_conditions = [check_congruence_after_factoring_out_gcf(ans_numer, user_numer) and check_congruence_after_factoring_out_gcf(ans_denom, user_denom)]
        # sufficient_conditions += [check_congruence_after_factoring_out_gcf(-ans_numer, user_numer) and check_congruence_after_factoring_out_gcf(-ans_denom, user_denom)]
        # check_congruence_after_factoring_out_gcf(sy.Symbol('x'), user_answer)
        # return answer ==  user_answer or answer == factor_negative_out_from_denominator(user_answer)
        # return any(sufficient_conditions)
        return congruence_of_quotient(answer, user_answer)

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        return f'\\({sy.latex(user_answer)}\\)'

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
            answer = parse_expr('x', transformations=transformations)
            congruence_of_quotient(answer, user_answer)
            # ans_numer, ans_denom = get_numer_denom(answer)
            # user_numer, user_denom = get_numer_denom(user_answer)
            # sufficient_conditions = [check_congruence_after_factoring_out_gcf(ans_numer, user_numer) and check_congruence_after_factoring_out_gcf(ans_denom, user_denom)]
            # sufficient_conditions += [check_congruence_after_factoring_out_gcf(-ans_numer, user_numer) and check_congruence_after_factoring_out_gcf(-ans_denom, user_denom)]
            # factor_negative_out_from_denominator(user_answer)
            # type(user_answer) == type(parse_expr('5', transformations=transformations))
            # if 'x' in str(user_answer):
            #     check_congruence_after_factoring_out_gcf(sy.Symbol('x'), user_answer)
        except:
            raise SyntaxError


Question_Class = RationalsMultiplyOrDivide
prob_type = 'math_blank'
