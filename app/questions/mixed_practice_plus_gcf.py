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
                            check_congruence_after_factoring_out_gcf)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class MixedPracticePlusGCF(Question):
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

        self.type_of_problem = random.choice(['easyFactorExpr',
                                                'factorByGroupingExpr',
                                                'specialPatternExpr',
                                                'fancyFactorExpr',
                                                'quadraticPatternExpr'])

        # self.type_of_problem = 'easyFactorExpr'

        if self.type_of_problem == 'quadraticPatternExpr':
            p = 0
            while p == 0:
            	p = random.randint(-7,7)
            q = 0
            while q ==0:
            	q = random.randint(-5,5)
            e = random.randint(2,6)
            expr = (x-p)*(x-q)
            expr = expr.subs(x, x**e)
        if self.type_of_problem == 'fancyFactorExpr':
            m = random.randint(2, 5)
            p = random.choice([-5,-3,-2,-1,1,2, 3, 5])
            n = random.choice([-5,-3,-2,-1,1,2, 3, 5])
            q = random.choice([-5,-3,-2,-1,1,2, 3, 5])
            expr = (m*x+p)*(n*x+q)
        if self.type_of_problem == 'specialPatternExpr':
            a = random.randint(1,9)
            b = random.randint(1,9)
            sign1 = random.choice([-1,1])
            sign2 = random.choice([-1,1])
            x, t, r, y = sy.symbols('x t r y')
            vars = random.choice([(x,1),(x,y),(r,t),(1,y)])
            vars = (r,t)
            A = a*vars[0]
            B1 = sign1*b*vars[1]
            B2 = sign2*b*vars[1]
            expr = (A+B1)*(A+B2)
        if self.type_of_problem == 'factorByGroupingExpr':
            a = 0
            while a==0:
                a = random.randint(-5,5)
            b = 0
            while b==0:
                b = random.randint(-5,5)
            c = 0
            while c==0:
                c = random.randint(-5,5)
            d = 0
            while d==0:
                d = random.randint(-5,5)
            x, t, r, y = sy.symbols('x t r y')
            vars = random.choice([(x,1),(x,y),(r,t)])
            vars = [x,1]
            A = a*vars[0]**2
            C = c*vars[1]
            B = b*vars[0]
            D = d*vars[1]
            expr = (A+C)*(B+D)
        if self.type_of_problem == 'easyFactorExpr':
            p=0
            while p ==0:
            	p = random.randint(-9,9)
            q = 0
            while q == 0:
            	q = random.randint(-9,9)
            b = p+q
            c = p*q
            expr = x**2+b*x+c
        random.seed(self.seed) #Why do I have to put this here??? ... meaning, I put it here to get consistent behavior from the random generator, but why do I need to do that?
        A = 0
        while A == 0:
        	A = random.randint(-7,7)
        e=random.randint(0,5)

        GCF = A*x**e

        expr = GCF*expr

        self.answer = sy.factor(expr)
        # expr1 = sy.factor(A+B1)*(A+B2)
        # expr2 = (A+B1)*sy.factor(A+B2)
        # expr3 = sy.factor((A+B1)*(A+B2))
        # self.answers = [expr, expr1, expr2, expr3]
        self.format_answer = f'\( {sy.latex(self.answer)}\)'

        self.format_given = f"\\[{sy.latex(sy.expand(self.answer))} \\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Mixed Factoring, Plus GCF'
    module_name = 'mixed_practice_plus_gcf'

    prompt_single = """Completely factor."""
    prompt_multiple = """TBA"""

    further_instruction = """
    """

    loom_link = "https://www.loom.com/share/d438c1117f6947dba59cb1023a6a9bae?sharedAppSource=personal_library"

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
        # return answer ==  user_answer
        return check_congruence_after_factoring_out_gcf(answer, user_answer)

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        return f'\\({user_answer}\\)'

    @staticmethod
    def validator(user_answer):
        try:
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('^', '**')
            user_answer = parse_expr(user_answer, transformations=transformations)
        except:
            raise SyntaxError


Question_Class = MixedPracticePlusGCF
prob_type = 'math_blank'
