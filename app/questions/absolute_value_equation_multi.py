#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
from sympy import *

from app.questions import (Question,
                            latex_print,
                            random_non_zero_integer,
                            permute_equation,
                            has_letters)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general
prob_type = 'math_blank'

class LinearOrAbs():
    def __init__(self, sign, a, b, x, whether_abs):
        self.sign = sign
        self.a = a
        self.b = b
        self.x = x
        self.whether_abs = whether_abs
        self.zero = Rational(-b, a)
        if whether_abs:
            self.term = sign*abs(a*x + b)
        else:
            self.term = sign*(a*x + b)
        self.kern = a*x + b


class AbsoluteValueEquationMulti(Question):
    """
    The given is
    \\[
        |ax + b| +... + similar +  c = 0
    \\]
    but permuted...

    Use kwarg num_terms to control number of extra terms
    """
    def __init__(self, **kwargs):
        # seq = [{'a': 1}, {'a': 2}, {'a': 3}]
        # get_the_bugs_out = sorted(seq, key=lambda d: d['a'])
        # get_the_bugs_out = LinearOrAbs(1, 1, 1, Symbol('x'), True) #Does Python make a call to random.random() when loading classes???
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        print('seed:', self.seed)
        random.seed(self.seed)
        if 'd' in kwargs:
            self.d = kwargs['d']
        else:
            self.d = random.randint(-6, 6)
        # self.d = 2
        if 'num_abs_val_terms' in kwargs:
            self.num_abs_val_terms = kwargs['num_abs_val_terms']
        else:
            self.num_abs_val_terms = random.choice([1, 2, 3])
        # self.num_abs_val_terms = 3
        if 'force_infinite_solutions' in kwargs:
            self.force_infinite_solutions = kwargs['force_infinite_solutions']
        else:
            self.force_infinite_solutions = random.choice([False, False, True])
        self.force_infinite_solutions = True
        if 'guarantee_solution' in kwargs:
            self.guarantee_solution = kwargs['guarantee_solution']
        else:
            self.guarantee_solution = random.choice([False, True])
        self.guarantee_solution = True
        if 'x' in kwargs:
            self.x = kwargs['x']
        else:
            self.x = Symbol('x')
        x = self.x
        if self.force_infinite_solutions:
            a1 = random.randint(1,9)
            s1 = random.choice([-1,1])
            b1 = random.randint(-9,9)
            # print(s1, a1, b1)
            if self.num_abs_val_terms == 1:
                a2 = a1
                s2 = random.choice([-1,1])
                b2 = random.randint(-9,9)
                while b2 == b1:
                    b2 = random.randint(-9,9)
                abs_val_terms = [LinearOrAbs(s1, a1, b1, self.x, True)]
                random.seed(self.seed)
                # print(s1, a2, b1, s2, a2, b2)
                if s1*a1 + s2*a2 == 0:
                    self.d = -s1*b1-s2*b2
                elif -s1*a1 + s2*a1 == 0:
                    self.d = s1*b1-s2*b2
                linear_term = s2*(a2*self.x + b2) + self.d
            elif self.num_abs_val_terms == 2:
                linear_x = random.choice([True, False])
                linear_x = True
                if linear_x:
                    a2 = random.randint(1,9)
                    s2 = random.choice([-1,1])
                    b2 = random.randint(-9,9)
                    print(s2, a2, b2)
                    # i = 0
                    while a1 == a2 and b2 == b1:
                        # print(i)
                        # i += 1
                        b2 = random.randint(-9,9)
                    # random.seed(self.seed)
                    abs_val_terms = [LinearOrAbs(s1, a1, b1, self.x, True),
                                    LinearOrAbs(s2, a2, b2, self.x, True)]
                    random.seed(self.seed) #Don't know why this is needed---but seems to be needed at this precise spot: what does Python do on the first run of the class that it doesn't do on subsequent run in same session???
                    abs_val_terms = sorted(abs_val_terms, key=lambda term: term.zero)
                    s1 = abs_val_terms[0].sign
                    a1 = abs_val_terms[0].a
                    b1 = abs_val_terms[0].b
                    s2 = abs_val_terms[1].sign
                    a2 = abs_val_terms[1].a
                    b2 = abs_val_terms[1].b
                    # random.seed(self.seed)
                    where = random.choice([0, 1, 2])
                    # print('where:', where)
                    if where == 0:
                        a3 = s1*a1 + s2*a2
                        b3 = s1*b1 + s2*b2
                    elif where == 1:
                        a3 = -s1*a1 + s2*a2
                        b3 = -s1*b1 + s2*b2
                    elif where == 2:
                        a3 = -s1*a1 - s2*a2
                        b3 = -s1*b1 - s2*b2
                    linear_term = a3*x + b3
                else:
                    a2 = a1
                    s2 = random.choice([-1,1])
                    b2 = random.randint(-9,9)
                    while b2 == b1:
                        b2 = random.randint(-9,9)
                    abs_val_terms = [LinearOrAbs(s1, a1, b1, self.x, True),
                                    LinearOrAbs(s2, a2, b2, self.x, True)]
                    random.seed(self.seed)
                    abs_val_terms = sorted(abs_val_terms, key=lambda term: term.zero)
                    s1 = abs_val_terms[0].sign
                    a1 = abs_val_terms[0].a
                    b1 = abs_val_terms[0].b
                    s2 = abs_val_terms[1].sign
                    a2 = abs_val_terms[1].a
                    b2 = abs_val_terms[1].b
                    if s1*a1 + s2*a2 == 0:
                        self.d = random.choice([-s1*b1-s2*b2, s1*b1 + s2*b2])
                    elif s1*a1 - s2*a2 == 0:
                        self.d = s1*b1-s2*b2
                    linear_term = self.d
            elif self.num_abs_val_terms == 3:
                a2 = random.randint(1,9)
                s2 = random.choice([-1,1])
                b2 = random.randint(-9,9)
                # print(s2, a2, b2)
                # i = 0
                while a1 == a2 and b2 == b1:
                    # print(i)
                    # i += 1
                    b2 = random.randint(-9,9)
                # random.seed(self.seed)
                abs_val_terms = [LinearOrAbs(s1, a1, b1, self.x, True),
                                LinearOrAbs(s2, a2, b2, self.x, True)]
                random.seed(self.seed) #Don't know why this is needed---but seems to be needed at this precise spot: what does Python do on the first run of the class that it doesn't do on subsequent run in same session???
                abs_val_terms = sorted(abs_val_terms, key=lambda term: term.zero)
                s1 = abs_val_terms[0].sign
                a1 = abs_val_terms[0].a
                b1 = abs_val_terms[0].b
                s2 = abs_val_terms[1].sign
                a2 = abs_val_terms[1].a
                b2 = abs_val_terms[1].b
                # random.seed(self.seed)
                where = random.choice([0, 1, 2])
                # print('where:', where)
                if where == 0:
                    a3 = s1*a1 + s2*a2
                    b3 = s1*b1 + s2*b2
                    if a3 < 0:
                        a3, b3 = -a3, -b3
                elif where == 1:
                    a3 = -s1*a1 + s2*a2
                    b3 = -s1*b1 + s2*b2
                    if a3 < 0:
                        a3, b3 = -a3, -b3
                elif where == 2:
                    a3 = -s1*a1 - s2*a2
                    b3 = -s1*b1 - s2*b2
                    if a3 < 0:
                        a3, b3 = -a3, -b3
                last = LinearOrAbs(random.choice([-1,1]), a3, b3, self.x, True)
                random.seed(self.seed)
                abs_val_terms.append(last)
                linear_term = 0
        else:
            coeffs = []
            signs = []
            for i in range(self.num_abs_val_terms):
                # random.seed(self.seed)
                sign = random.choice([-1,1])
                signs.append(sign)
                a = random.randint(1,4)
                b = int(random.triangular(-9,9, 0))
                # print('a, b:', a, b)
                while [a, b] in coeffs:
                    # print('a, b, coeffs:', a, b, coeffs)
                    a = random.randint(1,4)
                    b = int(random.triangular(-9,9, 0))
                coeffs.append([a, b])
            abs_val_terms = []
            for i in range(self.num_abs_val_terms):
                sign = signs[i]
                a, b = coeffs[i]
                abs_val_terms.append(LinearOrAbs(sign, a, b, self.x, True))
                random.seed(self.seed)
            # abs_val_terms = [LinearOrAbs(1, 1, 2, self.x, True), LinearOrAbs(-1, 1, 0, self.x, True)]
            # random.seed(self.seed)
            if self.num_abs_val_terms == 1:
                linear_term = random_non_zero_integer(-5,5)*self.x + self.d
            else:
                linear_term = random.choice([1, 0])*random.randint(-5,5)*self.x + self.d
            # linear_term = 2
        if self.guarantee_solution and not self.force_infinite_solutions:
            # random.seed(self.seed)
            sol = random.randint(-10,10)
            # print('sol', sol)
            terms = [term.term for term in abs_val_terms]
            terms.append(linear_term)
            expr =  sum(terms)
            add_in = -expr.subs(self.x, sol)
            linear_term += add_in

        self.linear_term = linear_term


        solution_set = EmptySet

        abs_val_terms = sorted(abs_val_terms, key=lambda term: term.zero)
        self.abs_val_terms = [term.term for term in abs_val_terms]
        # print('terms', [term.term for term in abs_val_terms])

        i = 0
        r = -oo
        while i < len(abs_val_terms):
            zero = abs_val_terms[i].zero
            l, r = r, zero
            # print(i, 'interval:', l, r)
            # print(i, 'zero:', zero)
            expr = 0
            for term in abs_val_terms:
                # print('term:', term.term)
                if zero <= term.zero:
                    addin = -term.sign*term.kern
                    # print('addin', addin)
                    # print('kern', term.kern)
                    # print('a', term.a)
                    # print('sign', term.sign)
                else:
                    addin = term.sign*term.kern
                expr += addin
            expr += linear_term
            # print('expr', i, ':', expr)
            if simplify(expr) == 0:
                solution_set = solution_set.union(Interval(l, r))
            elif simplify(expr).is_number:
                # print('was number')
                pass
            else:
                sol = solve(expr)[0]
                # print('sol', sol)
                if sol in Interval(l, r):
                    print(i, True)
                    solution_set = solution_set.union(FiniteSet(sol))
            i += 1
        l, r = r, oo
        expr = 0
        # print(i, 'interval:', l, r)
        # print(i, 'zero:', zero)
        for term in abs_val_terms:
            addin = term.sign*term.kern
            expr += addin
        expr += linear_term
        # print('expr', 'last:', expr)
        if simplify(expr) == 0:
            solution_set = solution_set.union(Interval(l, r))
        else:
            if solve(expr) != []:
                sol = solve(expr)[0]
                # print('sol', sol)
                if sol in Interval(l, r):
                    solution_set = solution_set.union(FiniteSet(sol))
        self.solution_set = solution_set
        self.format_answer = f'\\({latex(self.solution_set)}\\)'
        print(self.format_answer)

        terms = [term.term for term in abs_val_terms]
        terms.append(linear_term)
        eq = permute_equation(terms, True, seed=self.seed)

        self.given = eq
        self.format_given = f'\\[{latex(eq[0])} = {latex(eq[1])}\\]'

        self.format_given_for_tex = f"""
        {self.prompt_single} \n
        {self.format_given}
        """



    name = 'Equation with Multiple Absolute Value Terms'
    module_name = 'absolute_value_equation_multi'

    prompt_single = 'Solve for \\(x\\).  (Find the solution set.) '
    prompt_multiple = 'For each of the following, solve for \\(x\\).  (Find the solution set.)'

    further_instruction = """Use set notation for your answer, and, specifically, use
    interval notation for all intervals.  Use curly braces surrounding any
    individual, isolated solutions.  Use the union symbol \(\cup\) to join
    together separate pieces of your solution set into a single set.
    For instance, your answer might be
    \\(
        (-\\infty, -8] \\cup \\left\\{\\frac{5}{6}, 8\\right\\} \\cup [10, \\infty)
    \\)
    in which case you would enter

    "
        (-oo, -8] U {5/6, 8} U [10, oo)
    "

    Use capital U for union and 'oo' (little oh-little oh) for infinity.
    """

    # loom_link = "https://www.loom.com/share/4408bcd698d041e9917ba44ed17fbb2e"


    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'




    def checkanswer(self, user_answer):
        if self.solution_set == EmptySet:
            return 'no' in user_answer.lower() or 'null' in user_answer.lower() or 'empty' in user_answer.lower() or user_answer.replace(' ', '') == '{}'
        else:
            user_solution_set = EmptySet
            # user_answer = user_answer.replace('x', ' ')
            # user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            # user_answer = user_answer.replace('or', ',')
            user_answers = user_answer.split('U')
            i = 0
            while i < len(user_answers):
                user_answers[i] = user_answers[i].replace(' ', '')
                part = user_answers[i]
                if part == '{}':
                    pass
                elif part[0] == '{' and part[-1] == '}':
                    part = part.replace('{', '')
                    part = part.replace('}', '')
                    part = part.split(',')
                    for item in part:
                        item = parse_expr(item, transformations=transformations)
                        user_solution_set = user_solution_set.union(FiniteSet(item))
                elif (part[0] == '[' or part[0:3] == '(-oo') and (part[-1] == ']' or part[-3:-1] == 'oo)'):
                    part = part.replace('(', '')
                    part = part.replace('[', '')
                    part = part.replace(']', '')
                    part = part.replace(')', '')
                    part = part.split(',')
                    l = parse_expr(part[0], transformations=transformations)
                    r = parse_expr(part[1], transformations=transformations)
                    user_solution_set = user_solution_set.union(Interval(l, r))
                elif (part[0] == '[' or part[0:3] == '(-oo') and part[-1] == ')' and part[-3:-1] != 'oo)':
                    part = part.replace('(', '')
                    part = part.replace('[', '')
                    part = part.replace(']', '')
                    part = part.replace(')', '')
                    part = part.split(',')
                    l = parse_expr(part[0], transformations=transformations)
                    r = parse_expr(part[1], transformations=transformations)
                    user_solution_set = user_solution_set.union(Interval.Ropen(l, r))
                elif part[0] == '(' and part[0:3] != '(-oo' and part[-1] == ')' and part[-3:-1] != 'oo)':
                    part = part.replace('(', '')
                    part = part.replace('[', '')
                    part = part.replace(']', '')
                    part = part.replace(')', '')
                    part = part.split(',')
                    l = parse_expr(part[0], transformations=transformations)
                    r = parse_expr(part[1], transformations=transformations)
                    user_solution_set = user_solution_set.union(Interval.open(l, r))
                elif part[0] == '(' and part[0:3] != '(-oo' and (part[-1] == ']' or part[-3:-1] == 'oo)'):
                    part = part.replace('(', '')
                    part = part.replace('[', '')
                    part = part.replace(']', '')
                    part = part.replace(')', '')
                    part = part.split(',')
                    l = parse_expr(part[0], transformations=transformations)
                    r = parse_expr(part[1], transformations=transformations)
                    user_solution_set = user_solution_set.union(Interval.Lopen(l, r))
                i += 1
            # user_answers = set(user_answers)
            # if self.num_solutions == oo:
            #     if len(user_answers) == 1:
            #         user_answer = list(user_answers)[0]
            #         cong = AbsoluteValueEquationPlusLinear.congruent
            #         print(type(user_answer))
            #         return cong(user_answer, self.ineq_answer)
            #     else:
            #         return False
            return self.solution_set == user_solution_set

    @staticmethod
    def congruent(ineq1, ineq2):
        try:
            return ineq1.equals(ineq2)
        except TypeError:
            return False

    def format_useranswer(self, user_answer, display=False):
        if 'no' in user_answer.lower() or 'null' in user_answer.lower() or 'empty' in user_answer.lower():
            return user_answer
        else:
            user_solution_set = EmptySet
            # user_answer = user_answer.replace('x', ' ')
            # user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            # user_answer = user_answer.replace('or', ',')
            user_answers = user_answer.split('U')
            i = 0
            while i < len(user_answers):
                user_answers[i] = user_answers[i].replace(' ', '')
                part = user_answers[i]
                if part == '{}':
                    pass
                elif part[0] == '{' and part[-1] == '}':
                    part = part.replace('{', '')
                    part = part.replace('}', '')
                    part = part.split(',')
                    for item in part:
                        item = parse_expr(item, transformations=transformations)
                        user_solution_set = user_solution_set.union(FiniteSet(item))
                elif (part[0] == '[' or part[0:3] == '(-oo') and (part[-1] == ']' or part[-3:-1] == 'oo)'):
                    part = part.replace('(', '')
                    part = part.replace('[', '')
                    part = part.replace(']', '')
                    part = part.replace(')', '')
                    part = part.split(',')
                    l = parse_expr(part[0], transformations=transformations)
                    r = parse_expr(part[1], transformations=transformations)
                    user_solution_set = user_solution_set.union(Interval(l, r))
                elif (part[0] == '[' or part[0:3] == '(-oo') and part[-1] == ')' and part[-3:-1] != 'oo)':
                    part = part.replace('(', '')
                    part = part.replace('[', '')
                    part = part.replace(']', '')
                    part = part.replace(')', '')
                    part = part.split(',')
                    l = parse_expr(part[0], transformations=transformations)
                    r = parse_expr(part[1], transformations=transformations)
                    user_solution_set = user_solution_set.union(Interval.Ropen(l, r))
                elif part[0] == '(' and part[0:3] != '(-oo' and part[-1] == ')' and part[-3:-1] != 'oo)':
                    part = part.replace('(', '')
                    part = part.replace('[', '')
                    part = part.replace(']', '')
                    part = part.replace(')', '')
                    part = part.split(',')
                    l = parse_expr(part[0], transformations=transformations)
                    r = parse_expr(part[1], transformations=transformations)
                    user_solution_set = user_solution_set.union(Interval.open(l, r))
                elif part[0] == '(' and part[0:3] != '(-oo' and (part[-1] == ']' or part[-3:-1] == 'oo)'):
                    part = part.replace('(', '')
                    part = part.replace('[', '')
                    part = part.replace(']', '')
                    part = part.replace(')', '')
                    part = part.split(',')
                    l = parse_expr(part[0], transformations=transformations)
                    r = parse_expr(part[1], transformations=transformations)
                    user_solution_set = user_solution_set.union(Interval.Lopen(l, r))
                i += 1
            return f'\({latex(user_solution_set)}\)'

    @classmethod
    def validator(self, user_answer):
        try:
            if user_answer.strip()[0].isnumeric():
                raise SyntaxError
            if 'no' in user_answer.lower() or 'null' in user_answer.lower() or 'empty' in user_answer.lower() or user_answer.replace(' ', '') == '{}':
                pass
            else:
                user_solution_set = EmptySet
                # user_answer = user_answer.replace('x', ' ')
                # user_answer = user_answer.replace('=', ' ')
                user_answer = user_answer.replace('^', '**')
                # user_answer = user_answer.replace('or', ',')
                user_answers = user_answer.split('U')
                i = 0
                while i < len(user_answers):
                    user_answers[i] = user_answers[i].replace(' ', '')
                    part = user_answers[i]
                    if part == '{}':
                        pass
                    elif part[0] == '{' and part[-1] == '}':
                        part = part.replace('{', '')
                        part = part.replace('}', '')
                        part = part.split(',')
                        for item in part:
                            item = parse_expr(item, transformations=transformations)
                            user_solution_set = user_solution_set.union(FiniteSet(item))
                    elif (part[0] == '[' or part[0:3] == '(-oo') and (part[-1] == ']' or part[-3:-1] == 'oo)'):
                        part = part.replace('(', '')
                        part = part.replace('[', '')
                        part = part.replace(']', '')
                        part = part.replace(')', '')
                        part = part.split(',')
                        l = parse_expr(part[0], transformations=transformations)
                        r = parse_expr(part[1], transformations=transformations)
                        user_solution_set = user_solution_set.union(Interval(l, r))
                    elif (part[0] == '[' or part[0:3] == '(-oo') and part[-1] == ')' and part[-3:-1] != 'oo)':
                        part = part.replace('(', '')
                        part = part.replace('[', '')
                        part = part.replace(']', '')
                        part = part.replace(')', '')
                        part = part.split(',')
                        l = parse_expr(part[0], transformations=transformations)
                        r = parse_expr(part[1], transformations=transformations)
                        user_solution_set = user_solution_set.union(Interval.Ropen(l, r))
                    elif part[0] == '(' and part[0:3] != '(-oo' and part[-1] == ')' and part[-3:-1] != 'oo)':
                        part = part.replace('(', '')
                        part = part.replace('[', '')
                        part = part.replace(']', '')
                        part = part.replace(')', '')
                        part = part.split(',')
                        l = parse_expr(part[0], transformations=transformations)
                        r = parse_expr(part[1], transformations=transformations)
                        user_solution_set = user_solution_set.union(Interval.open(l, r))
                    elif part[0] == '(' and part[0:3] != '(-oo' and (part[-1] == ']' or part[-3:-1] == 'oo)'):
                        part = part.replace('(', '')
                        part = part.replace('[', '')
                        part = part.replace(']', '')
                        part = part.replace(')', '')
                        part = part.split(',')
                        l = parse_expr(part[0], transformations=transformations)
                        r = parse_expr(part[1], transformations=transformations)
                        user_solution_set = user_solution_set.union(Interval.Lopen(l, r))
                    i += 1
        except:
            raise SyntaxError


Question_Class = AbsoluteValueEquationMulti
