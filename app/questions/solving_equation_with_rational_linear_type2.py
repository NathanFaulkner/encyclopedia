#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import sympy as sy

from app.questions import (Question,
                            random_non_zero_integer,
                            list_integer_factors,
                            has_numbers)


# if __name__ == '__main__':
#     import os
#     import sys
#     sys.path.append(os.path.realpath('..'))
#     import questions.general
# else:
#     from .. import general


class SolvingEquationWithRationalLinearType2(Question):
    """
    """
    def __init__(self, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        x = sy.Symbol('x')
        #expr = x**2 + 2*x +3
        #
        #print(coeff(expr, x, 2))
        if 'force' in kwargs:
            self.force = kwargs['force']
        else:
            self.force = random.choice(['no solution', 'par', None])
        force_par_solution = False or self.force == 'par'
        force_no_solution = False or self.force == 'no solution'
        harder = random.choice([False, True])
        b = []
        d = []
        for i in range(2):
            # random.seed(self.seed*(i+1) % 1)
            b.append(random.randint(-6,6))
            d.append(random.randint(-6,6))
        if force_no_solution:
            b[0] = d[0]
            b[1] = d[1]
        elif force_par_solution:
            b[0] = d[0]
        # random.seed(self.seed)
        a = random.choice([-1,-1,1,1,2,-2])
        e = random.choice([[1,1],[0,1],[0,0], [1,1], [1,1]])
        if harder:
            e=[1,1]
        m = random.choice([1,1,1,2])
        N = a*(m*x+b[0])**e[0]*(x+b[1])
        #print(coeff(N, x, 1))
        random.seed(self.seed) #I don't quite know why this needs to go here, but it seems to do the trick! :/
        f = int(random.triangular(-5,5,0))
        c1 = a*(m*x + f)
        c2 = N.coeff(x, 1) - (c1*(x+d[0])**e[1]).coeff(x, 1)
        g = sy.simplify(N - c1*(x+d[0])**e[0] - c2*(x+d[1]))
        #print(g)
        terms = [c1/(x+d[1]), c2/(x+d[0])**e[0], g/sy.expand((x+d[0])**e[0]*(x+d[1]))]
        #print(terms)
        random.seed(self.seed)
        random.shuffle(terms)
        #print(terms)
        case = random.choice([1, 2])
        #if case == 1:
        #    prob = latex(terms[0]) + '=' + latex(-terms[1] - terms[2])
        #else:
        #    prob = latex(terms[0] + terms[1]) + '=' + latex(simplify(-terms[2]))
        #print(prob)
        if case == 1:
            prob = sy.latex(sy.Eq(terms[0]+terms[1], -terms[2]))
        else:
            prob = sy.latex(sy.Eq(terms[0], -terms[1]-terms[2]))

        self.answer = set(sy.solve(terms[0]+terms[1]+terms[2], x))
        # print(self.answer)
        if self.answer == set():
            fmt_ans = 'No solution'
            self.has_solutions = False
        else:
            self.has_solutions = True
            fmt_ans = '\\( '
            for ans in self.answer:
                fmt_ans += f'{sy.latex(ans)}, '
            fmt_ans = fmt_ans[:-2]
            fmt_ans += ' \\)'

        self.format_answer = fmt_ans

        self.format_given = f"\\[{prob}\\]"

        self.format_given_for_tex = f"""
        {self.prompt_single}

        {self.format_given}
        """

    name = 'Rationals: Solving, Type 2'
    module_name = 'solving_equation_with_rational_linear_type2'

    prompt_single = """Find the solution set.  (It is wise to check you answer(s).)"""
    prompt_multiple = """TBA"""

    # further_instruction = """
    # """

    loom_link = "https://www.loom.com/share/d771a2f728a94428a8732851aace4613?sharedAppSource=personal_library"

    # prototype_answer = '\\( (x^r+p)(x^r+q)\\)'


    def checkanswer(self, user_answer):
        if not self.has_solutions:
            return 'no' in user_answer.lower() or 'null' in user_answer.lower() or 'empty' in user_answer.lower()
        else:
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('or', ',')
            user_answers = user_answer.split(',')
            i = 0
            while i < len(user_answers):
                user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
                i += 1
            user_answers = set(user_answers)
            print('user_answers', user_answers)
            print('answer', self.answer)
            return self.answer == user_answers

    @staticmethod
    def format_useranswer(user_answer, display=False):
        user_answer = user_answer.lower()
        if 'no' in user_answer or 'null' in user_answer or 'empty' in user_answer:
            return user_answer
        else:
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('or', ',')
            user_answers = user_answer.split(',')
            i = 0
            while i < len(user_answers):
                user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
                i += 1
            user_answers = set(user_answers)
            format_answer = ''
            for ans in user_answers:
                format_answer += sy.latex(ans) + ' ,'
            format_answer = format_answer[:-2]
            return '\(' + format_answer + '\)'


    @staticmethod
    def validator(user_answer):
        try:
            # pass
            user_answer = user_answer.lower()
            user_answer = user_answer.replace('x', ' ')
            user_answer = user_answer.replace('=', ' ')
            user_answer = user_answer.replace('^', '**')
            user_answer = user_answer.replace('or', ',')
            if not has_numbers(user_answer):
                if 'no' not in user_answer and 'null' not in user_answer and 'empty' not in user_answer:
                    raise SyntaxError
            user_answers = user_answer.split(',')
            i = 0
            while i < len(user_answers):
                user_answers[i] = parse_expr(user_answers[i], transformations=transformations)
                i += 1
            user_answers = set(user_answers)
            format_answer = ''
            for ans in user_answers:
                format_answer += sy.latex(ans) + ' ,'
            format_answer = format_answer[:-2]
        except:
            raise SyntaxError

Question_Class = SolvingEquationWithRationalLinearType2
prob_type = 'math_blank'
