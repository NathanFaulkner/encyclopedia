from sympy import*
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import standard_transformations, implicit_multiplication_application
transformations = (standard_transformations + (implicit_multiplication_application,))
import random

from app.questions import Question

class FactoringLevel1Question(Question):
    def __init_(self, seed):
        self.seed = seed
        random.seed(seed)

    self.prototype = 'Answer: \\( (x^e+p)(x^e+q) \\)'
    self.prompt_single = "Completely factor the following: \\(" + latex(expand(expr)) + "\\)"
    self.prompt_multiple = "Completely factor each of the following: "
    self.x = Symbol('x')
    self.p = random.randint(-7, 7)
    self.q = random.randint(-7, 7)
    self.answer = (x**e+p)*(x**e+q)
    self.latex_answer = latex(self.answer)

    def checkanswer(self, user_answer):
        user_answer = user_answer.replace('^', '**')
        user_answer = parse_expr(user_answer, transformations=transformations)
        answer = sympify(str((self.answer)))
        return answer == user_answer
