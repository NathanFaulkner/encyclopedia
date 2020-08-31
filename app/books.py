import datetime
import os
import random

from app import questions


class Book(): #Not used at this time
    def __init__(self, name, front, main, end):
        self.name = name
        self.front = front
        self.main = main
        self.end = end

class Section():
    def __init__(self, view_name, display_name, template_path):
        self.view_name = view_name
        self.display_name = display_name
        self.template_path = template_path
        self.questions = []
        self.due_date = None

    def add_to_questions(self, question_name, *args):
        self.questions.append(question_name)
        for question in args:
            self.questions.append(question)

# class Section():
#     def __init__(self, category, free_section, numbered=True):
#         self.category = category
#         self.display_name = free_section.display_name
#         self.section = free_section
#         self.numbered = numbered
#         self.view_name = free_section.view_name
#         self.template_path = free_section.template_path

class Division():
    def __init__(self, category, display_name, subdivisions, template_path=None):
        self.category = category
        self.display_name = display_name
        self.subdivisions = subdivisions
        self.template_path = template_path

    def set_frontpage(self, frontpage): #frontpage can be a FreeSection or Section
        self.frontpage = frontpage
        self.view_name = frontpage.view_name
        self.template_path = frontpage.template_path
        self.questions = frontpage.questions


    def get_division_into(self):
        if self.subdivisions is not None:
            return self.subdivisions[0].category
        else:
            return None


    @staticmethod
    def list_bottom_elements(subdivisions):
        bottom = []
        if type(subdivisions) == dict:
            subdivisions = [subdivisions[i] for i in subdivisions]
        for subdivision in subdivisions:
            try:
                subdivision.subdivisions
                bottom += Division.list_bottom_elements(subdivision.subdivisions)
            except AttributeError:
                if subdivision is not None:
                    bottom.append(subdivision)
        return bottom

    def list_all_sections(self):
        return Division.list_bottom_elements(self.subdivisions)

    def get_skill_info(self, question_name):
        """One could generalize this, but this is written only with
        a book --> chapters --> sections --> questions in mind.... come
        to think of it, I should have made questions the lowest level
        elements of these trees. ... then a recursive function
        could be built that ends with questions in the use case...
        """
        if self.category != 'book':
            return None
        info = []
        main = self.subdivisions['main']
        chapters = main.subdivisions
        for i, chapter in enumerate(chapters):
            section = chapter.subdivisions
            for j, section in enumerate(section):
                if question_name in section.questions:
                    info.append([i+1,j+1])
        return info


class SevenTest():
    def __init__(self, book, which_test, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        self.which_test = which_test
        self.book = book
        all_sections = book.list_all_sections()
        l = len(all_sections)
        num_sevens = int(l/7)
        start = num_sevens * (which_test - 1)
        if which_test <= num_sevens:
            test_sections = all_sections[start: start + 7]
            prev_sections = all_sections[0:start]
            random.shuffle(prev_sections)
            test_sections += prev_sections[0:3]
        else:
            num_left = l - start
            test_sections = all_sections[-num_left: -1]
            prev_sections = all_sections[0:start]
            random.shuffle(prev_sections)
            test_sections += prev_sections[0:10 - num_left]
        self.sections = test_sections
        question_sets = []
        for i, section in enumerate(self.sections):
            if section.questions != []:
                question_name = random.choice(section.questions)
                section_info = self.book.get_skill_info(question_name)[0]
                question_module = getattr(questions, question_name)
                question = question_module.Question_Class(seed=self.seed)
                question_set = [question]
                question_name = random.choice(section.questions)
                question_module = getattr(questions, question_name)
                question = question_module.Question_Class(seed=abs(1-self.seed))
                question_set.append(question)
                question_sets.append(question_set)
            else:
                question_sets.append([])
        self.question_sets = question_sets

    preamble = r"""
\documentclass[12pt]{article}
\usepackage{amsmath}% http://ctan.org/pkg/amsmath
\usepackage[
  height=10in,      % height of the text block
  width=7in,       % width of the text block
  top=0.5in,        % distance of the text block from the top of the page
  headheight=48pt, % height for the header block
  headsep=12pt,    % distance from the header block to the text block
  heightrounded,   % ensure an integer number of lines
  %showframe,       % show the main blocks
  verbose,         % show the values of the parameters in the log file
]{geometry}


\pagestyle{empty}



\usepackage{graphicx}


\usepackage{xcolor}

\definecolor{epsilon-blue}{RGB}{0,0,155}


\newcommand{\lt}{<}
\newcommand{\gt}{>}





\pagestyle{empty}

"""


    def make_tex(self, key=False):
        title = f'{self.book.name_for_path}_{self.which_test}_v{self.seed}'
        if key:
            title += '_key'
        file_name_with_path = os.path.join('app', 'for_printing', title, '{a}.tex'.format(a=title))
        # print(os.getcwd())
        try:
            os.chdir('app')
            os.chdir('for_printing')
            # print(os.getcwd())
            os.mkdir(title)
            os.chdir(title)
            f = open('{a}.tex'.format(a=title), 'w+')
        except:
            os.chdir(title)
            # print(os.getcwd())
            f = open('{a}.tex'.format(a=title), 'w+')
        out = self.preamble
        # title_head = f"\\lhead{{\\textbf{{{self.book.display_name} - Test {self.which_test} v. {self.seed} \\\\Printed on \\today}}}}"
        # out += title_head + '\n\n'
        out += '\\begin{document}\n\n'
        # out += '\\thispagestyle{fancy}\n\n'
        header = f"""\\noindent
        \\begin{{tabular}}{{ p{{3.5in}} p{{3.2in}} }}
        \\hspace{{-1ex}}\\textbf{{{self.book.display_name} - Test {self.which_test} }} & \\textbf{{Name: \\underline{{\\hspace{{2.65in}} }}}}\\\\
        \\hspace{{-1ex}}\\textbf{{Version - {self.seed} }} &   \\textbf{{Date: \\hspace{{2in}} }}\\
        \\end{{tabular}}
        \\hrule
        """
        out += header
        out += '\\begin{enumerate}\n'
        for question_set in self.question_sets:
            if question_set != []:
                question = question_set[0]
                section_info = self.book.get_skill_info(question.module_name)[0]
                out += f'\\item {{\color{{gray}}({section_info[0]}.{section_info[1]})}} \n'
                out += '\\begin{enumerate}\n'
                out += f'\\item {question.format_given_for_tex}\n'
                out += '\\vspace{12\\baselineskip}\n'
                question = question_set[1]
                out += f'\\item {question.format_given_for_tex}\n'
                out += '\\vspace{12\\baselineskip}\n'
                out += '\\end{enumerate}\n'
            else:
                out += f'\\item No questions have been constructed for this section.'
        out += '\\end{enumerate}\n'
        if key:
            out += '\\newpage'
            out += '\\textbf{Answers:}\n'
            out += '\\begin{enumerate}\n'
            for question_set in self.question_sets:
                out += '\\item\n'
                if question_set != []:
                    out += '\\begin{enumerate}\n'
                    out += f'\\item {question_set[0].format_answer}\n'
                    out += f'\\item {question_set[1].format_answer}\n'
                    out += '\\end{enumerate}\n'
            out += '\\end{enumerate}\n'
        out += '\\end{document}'

        f.write(out)
        f.close()

        status = os.system('pdflatex {title}'.format(title=title))

        os.chdir('..')
        os.chdir('..')
        os.chdir('..')

        return status





#########################
# Free Sections -- not "bound" in a book
algebra2 = Section('algebra2', "Algebra 2", '/sections/algebra2')

nutsandboltsofalgebra = Section('nutsandboltsofalgebra', "Nuts and Bolts of Algebra", '/sections/nuts-and-bolts-of-algebra')

equationsatthegasstation = Section('equationsatthegasstation', "Equations at the Gas Station", '/sections/equations-at-the-gas-station')

literalequations = Section('literalequations', "Literal Equations", '/sections/literal-equations')

solveforx = Section('solveforx', "Solve for x", '/sections/solve-for-x')
solveforx.add_to_questions('solve_for_x')
solveforx.due_date = datetime.datetime(2020, 8, 25)

relationshipsinatable = Section('relationshipsinatable', "Relationships in a Table", '/sections/relationships-in-a-table')

linearinequalities = Section('linearinequalities', "Linear Inequalities", '/sections/linear-inequalities')
linearinequalities.add_to_questions('linear_inequality')
linearinequalities.due_date = datetime.datetime(2020, 8, 27)

graphsoflinearinequalities = Section('graphsoflinearinequalities', "Graphs of Linear Inequalities", '/sections/graphs-of-linear-inequalities')
graphsoflinearinequalities.add_to_questions('graph_of_linear_inequality')
graphsoflinearinequalities.due_date = datetime.datetime(2020, 8, 29)

solvingcompoundinequalities = Section('solvingcompoundinequalities', "Solving Compound Inequalities", '/sections/solving-compound-inequalities')
solvingcompoundinequalities.add_to_questions('compound_linear_inequality')
solvingcompoundinequalities.add_to_questions('graph_of_compound_linear_inequality')
solvingcompoundinequalities.due_date = datetime.datetime(2020, 9, 1)

# graphsofcompoundinequalities = Section('graphsofcompoundinequalities', "Graphs of Compound Inequalities", '/sections/graphs-of-compound-linear-inequalities')
intervalnotation = Section('intervalnotation', "Interval Notation", '/sections/interval_notation')
intervalnotation.add_to_questions('inequality_to_interval_notation',
                                    'interval_to_inequality_notation',
                                    'interval_notation_to_graph')

absolutevalueequations = Section('absolutevalueequations', "Absolute Value Equations", '/sections/absolute-value-equations')
absolutevalueequations.add_to_questions('absolute_value_equation')

absolutevalueinequalities = Section('absolutevalueinequalities', "Absolute Value Inequalities", '/sections/absolute-value-inequalities')
absolutevalueinequalities.add_to_questions('absolute_value_inequality',
                            'absolute_value_inequality_to_interval_notation',
                            'absolute_value_inequality_to_graph',
                            )

functionsandthecoordinateplane_intro = Section('functionsandthecoordinateplane_intro', "Functions and the Coordinate Plane", '/sections/functions-and-the-coordinate-plane')

basicfunctionsinatableandwords = Section('basicfunctionsinatableandwords', "Basic Functions in a Table and Words", '/sections/basic_functions_in_a_table_and_words')
basicfunctionsinatableandwords.add_to_questions('generic_table_computation',
                                                'pizza_problem_computation',
                                                'plant_problem_computation',
                                                'plant_problem',
                                                'generic_table',
                                                'pizza_problem')

functionnotation = Section('functionnotation', "Function Notation", '/sections/function_notation')
functionnotation.add_to_questions('function_notation',
                                    'function_from_set_notation')

functioncomposition = Section('functioncomposition', "Composition of Functions", '/sections/function_composition')
functioncomposition.add_to_questions('function_composition')

simplegraphing = Section('simplegraphing', "Simple Graphing", '/sections/simple_graphing')

linearfunctions_intro = Section('linear_functions', "Linear Functions", '/sections/linear-functions')

graphpointslope = Section('graphpointslope', "Graph from Point Slope Form", '/sections/graph-point-slope')
graphpointslope.add_to_questions('graph_point_slope')

factoring1 = Section('factoring1', "Factoring - Level 1", '/sections/factoring-coeff-of-one')
# factoring1.due_date = datetime.datetime(2020, 8, 28)

polynomials_intro = Section('polynomials', "Polynomials", '/sections/polynomials-intro')

quadraticpattern = Section('quadraticpattern', "Quadratic Pattern", '/sections/quadratic-pattern')
quadraticpattern.add_to_questions('quadratic_pattern')
# quadraticpattern.due_date = datetime.datetime(2020, 12, 2)
#
#############################

##############################
# Construction of book, Algebra2 -- collecting, "binding" sections, frontpages, etc.
nuts_and_bolts_of_algebra = Division('chapter', 'Nuts and Bolts of Algebra',
                                [solveforx,
                                linearinequalities,
                                graphsoflinearinequalities,
                                solvingcompoundinequalities,
                                intervalnotation,
                                absolutevalueequations,
                                absolutevalueinequalities])
nuts_and_bolts_of_algebra.set_frontpage(nutsandboltsofalgebra)

functions_and_the_coordinate_plane = Division('chapter', "Functions and the Coordinate Plane",
                                    [basicfunctionsinatableandwords,
                                    functionnotation,
                                    functioncomposition,
                                    simplegraphing])
functions_and_the_coordinate_plane.set_frontpage(functionsandthecoordinateplane_intro)

linear_functions = Division('chapter', 'Linear Functions', [graphpointslope])
linear_functions.set_frontpage(linearfunctions_intro)
polynomials = Division('chapter', 'Polynomials', [factoring1, quadraticpattern])
#polynomials.intro = polynomials_intro
polynomials.set_frontpage(polynomials_intro)

main = Division('main', 'Main Matter', [nuts_and_bolts_of_algebra,
                                        functions_and_the_coordinate_plane])

Algebra2 = Division('book', 'Algebra 2', {'front': None, 'main': main, 'end': None})
Algebra2.name_for_path = 'Algebra2'
Algebra2.set_frontpage(algebra2)
#
###################################
####
# Example book could be [foreword, dedication, preface, introduction, chapter1, ..
# ..., chapter n, Appendix A, Appendix B, ...].
####

Library = Division('library', 'Books', [Algebra2])
