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


class RationalsMessy(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        x = sy.Symbol('x')
        left = -7
        right = 7
        common_factor = x - random.choice([0,0,0,0,0,0,0,0,1,2,-1,-2])
        e = random.choice([[0,1], [1,1],[1,0]])
        f = random.choice([[0,1], [1,1],[1,0]])
        numa = []
        numb = []
        for i in range(2):
            numa.append(random_non_zero_integer(-5,5))
            numb.append(random.randint(1,3))
        numterms = []
        for i in range(2):
            term = sy.expand(numa[i]/(numb[i]*common_factor**e[i]))
            numterms.append(term)
        numerator = sy.expand(numterms[0] + numterms[1])
        denominator = 0
        while type(denominator) != type(x+1):
            dena = []
            denb = []
            denterms = []
            denominator = 0
            for i in range(2):
                dena.append(random_non_zero_integer(-5,5))
                denb.append(random.randint(1,3))
            for i in range(2):
                term = sy.expand(dena[i]/(denb[i]*common_factor**f[i]))
                denterms.append(term)
            denominator = sy.expand(denterms[0] + denterms[1])
        #print(numterms, denterms)
        #print(numerator, denominator)
        prob = '\\frac{{{n}}}{{{d}}}'.format(n=sy.latex(numerator), d=sy.latex(denominator))

        self.answer = sy.simplify(numerator/denominator)
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

    name = 'Rationals: Getting Messy'
    module_name = 'rationals_messy'

    prompt_single = """Simplify the following.
    (Your goal should be to write it plainly as a polynomial over another
    polynomial, as well as to look to factor these polynomials and cancel
    like factors, wherever possible.)"""
    prompt_multiple = """TBA"""

    further_instruction = """
    """

    # loom_link = "https://www.loom.com/share/6cbdb245ddf94247985dc59deac4cbf2?sharedAppSource=personal_library"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.lower()
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
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


Question_Class = RationalsMessy
prob_type = 'math_blank'
