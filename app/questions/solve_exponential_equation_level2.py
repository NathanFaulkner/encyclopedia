#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            get_integer_divisors,
                            fmt_abs_value,
                            has_numbers,
                            split_at_comma_not_in_parens,
                            )



class SolveExponentialLevel2(Question):
    """
    Format is
    \[
        e + c \cdot b^(Ax - B) = c \cdot d + e
    \]
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        if 'b' in kwargs:
            b = kwargs['b']
        else:
            b = random.randint(2,9)
        A = random_non_zero_integer(-9,9)
        B = random.randint(-5,5)
        C = random.randint(-9,9)
        while A == C:
            C = random.randint(-9,9)
        D = random.randint(-5,5)
        c = random_non_zero_integer(1,9)
        x = sy.Symbol('x')
        LHS = b**(A*x+B)
        RHS = c*b**(C*x+D)
        if random.choice([True, False]):
            LHS, RHS = RHS, LHS
        self.answer = sy.simplify(sy.Rational(1, (A-C))*(sy.log(c)/sy.log(b) + D - B))
        if (sy.log(c)/sy.log(b)).is_rational:
            self.format_answer = sy.latex(self.answer)
        else:
            if A - C == 1:
                if D - B == 0:
                    self.format_answer = f"\\log_{b}\\left({c}\\right)"
                elif D - B > 0:
                    self.format_answer = f"\\log_{b}\\left({c}\\right)+{sy.latex(D-B)}"
                else:
                    self.format_answer = f"\\log_{b}\\left({c}\\right)-{abs(D-B)}"
            else:
                if D - B == 0:
                    self.format_answer = f"\\frac{{\\log_{b}\\left({c}\\right)}}{{ {A - C} }}"
                elif D - B > 0:
                    self.format_answer = f"\\frac{{\\log_{b}\\left({c}\\right)+{sy.latex(D - B)}}}{{ {A - C} }}"
                else:
                    self.format_answer = f"\\frac{{\\log_{b}\\left({c}\\right)-{abs(D - B)}}}{{ {A - C} }}"
        self.format_answer = '\\(' + self.format_answer + '\\)'
        self.format_given = f"""
        \\[
            {sy.latex(LHS)} = {sy.latex(RHS)}
        \\]"""

        self.prompt_single = f"""Find all reals that solve the equation.
        (Find the solution set&mdash;the set of all real numbers that would make the equation
        true when substituted in.)  Give your answer in simplified form&mdash;either
        an integer or a fraction&mdash;or
        in terms of a logarithm.  (You won't receive credit for a decimal answer.)
        """

        self.format_given_for_tex = f"""
        Find all reals that solve the equation.
        (Find the solution set---the set of all real numbers that would make the equation
        true when substituted in.)  Give your answer in simplified form&mdash;either
        an integer or a fraction---or
        in terms of a logarithm.  (You won't receive credit for a decimal answer.)

        {self.format_given}
        """

    # def non_zero_integer(a,b):
    #     n = 0
    #     while n == 0:
    #         n = random.randint(a,b)
    #     return n



    name = 'Solve Exponential, Unknown in One Exponent'
    module_name = 'solve_exponential_equation_level2'


    prompt_multiple = """TBA"""

    further_instruction = """
        The answer checker (based on SymPy) understands both the symbols
        'log' and 'ln' to mean 'ln'.
        To use a base \(b\) other than base \(e\) (ln) you must use the notation
        "log(x, b)" to represent \\(\\log_b(x)\\).  For instance, if your answer involves the term
        \[
            \\log_{\\frac{1}{2}}\\left(1.2345\\right)
        \]
        then you should enter
        <div class="center" style="text-align:center">
            log(1.2345, 1/2)
        </div>

        Do NOT use commas in a decimal to represent the thousands place.  For instance,
        instead of writing "1,000" just write "1000".
    """


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        user_answer = user_answer.replace('x', '')
        user_answer = user_answer.replace('=', '')
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        print('user_ans:', user_answer, 'ans:', self.answer)
        print('simplified', sy.simplify(self.answer - user_answer))
        return sy.simplify(self.answer - user_answer) == 0

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.replace('x', '')
        user_answer = user_answer.replace('=', '')
        user_answer = user_answer.replace('^', '**')
        if 'log' in user_answer:
            i = user_answer.index('log')
            j = user_answer[i:].index(')')
            j = i + j
            log_string = user_answer[i:j+1]
            log_string = log_string.replace(' ', '')
            get_left = log_string.index('(')
            get_right = log_string.index(')')
            log_args = log_string[get_left+1:get_right].split(',')
            log_args = [parse_expr(arg, transformations=transformations) for arg in log_args]
            if len(log_args) == 2:
                restore_log = f'\\log_{{ {sy.latex(log_args[1])} }}\\left({sy.latex(log_args[0])}\\right)'
            else:
                restore_log = f'\\log\\left({sy.latex(log_args[0])}\\right)'
            user_answer = user_answer[:i] + 'L' + user_answer[j+1:]
        else:
            restore_log = 'L'
        user_answer = parse_expr(user_answer, transformations=transformations, evaluate=False)
        # print('user_answer', user_answer)
        out = sy.latex(user_answer).replace('L', restore_log)
        return f"\({out}\)"


    @staticmethod
    def validator(user_answer):
        try:
            tester = SolveExponentialLevel2()
            tester.checkanswer(user_answer)
            tester.format_useranswer(user_answer)
            # pass
        except:
            raise SyntaxError

Question_Class = SolveExponentialLevel2
prob_type = 'math_blank'
