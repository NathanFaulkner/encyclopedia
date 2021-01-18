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
    def __init__(self, view_name, display_name, template_path, challenge=False):
        self.view_name = view_name
        self.display_name = display_name
        self.template_path = template_path
        self.questions = []
        self.due_date = None
        self.challenge = challenge

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
    def list_bottom_elements(subdivisions, include_challenge=False):
        bottom = []
        if type(subdivisions) == dict:
            subdivisions = [subdivisions[i] for i in subdivisions]
        for subdivision in subdivisions:
            try:
                subdivision.subdivisions
                bottom += Division.list_bottom_elements(subdivision.subdivisions)
            except AttributeError:
                if include_challenge:
                    if subdivision is not None:
                        bottom.append(subdivision)
                else:
                    if subdivision is not None and not subdivision.challenge:
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

    def get_section_and_chapter_numbers(self, section_name):
        if self.category != 'book':
            return None
        info = []
        main = self.subdivisions['main']
        chapters = main.subdivisions
        for i, chapter in enumerate(chapters):
            section = chapter.subdivisions
            for j, section in enumerate(section):
                if section_name == section.view_name:
                    return [i+1,j+1]


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
        # for section in all_sections:
        #     print(section.display_name)
        l = len(all_sections)
        num_sevens = int(l/7)
        # print(num_sevens)
        start = 7 * (which_test - 1)
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
                if len(set(section.questions)) > 1:
                    question_names = random.sample(set(section.questions), 2)
                else:
                    question_names = [section.questions[0], section.questions[0]]
                section_info = self.book.get_skill_info(question_names[0])[0]
                question_module = getattr(questions, question_names[0])
                seed = (self.seed * (i+1)) % 1
                question = question_module.Question_Class(seed=seed)
                question_set = [question]
                question_module = getattr(questions, question_names[1])
                question = question_module.Question_Class(seed=abs(1-seed))
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
        # all_img_names = []
        for question_set in self.question_sets:
            i = 0
            # img_names = []
            for question in question_set:
                try:
                    if question.has_img:
                        img_name = '{qname}{i}'.format(qname=question.module_name, i=i)
                        question.save_img(img_name)
                    # img_names.append(img_name)
                except AttributeError:
                    pass
                if key:
                    try:
                        if question.has_img_in_key:
                            img_name = 'ans_for_{qname}{i}'.format(qname=question.module_name, i=i)
                            question.save_img(img_name)
                        # img_names.append(img_name)
                    except AttributeError:
                        pass
                i += 1
                # all_img_names.append(img_names)
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
                out += f"""\\item {{\color{{gray}}({section_info[0]}.{section_info[1]})}}
                For both problems, completely document the process by which you come to our answer.
                If there is no work to show, verbally explain how you arrived at your answer.
                This explanation does not need to be duplicated for each problem if
                the same process applies to each.
                (You will only receive half credit, otherwise.)\n"""
                out += '\\begin{enumerate}\n'
                out += f'\\item {question.format_given_for_tex}\n'
                try:
                    question.has_img
                    out += """
                    \\begin{{flushright}}
                        \\includegraphics[scale=0.6]{{{img_name}}}
                    \\end{{flushright}}
                    \\vspace{{-9\\baselineskip}}
                    """.format(img_name=question.module_name + '0')
                except AttributeError:
                    pass
                out += '\\vspace{12\\baselineskip}\n'
                question = question_set[1]
                out += f'\\item {question.format_given_for_tex}\n'
                try:
                    question.has_img
                    out += """
                    \\begin{{flushright}}
                        \\includegraphics[scale=0.6]{{{img_name}}}
                    \\end{{flushright}}
                    \\vspace{{-9\\baselineskip}}
                    """.format(img_name=question.module_name + '1')
                except AttributeError:
                    pass
                out += '\\vspace{12\\baselineskip}\n'
                out += '\\end{enumerate}\n'
            else:
                out += f'\\item No questions have been constructed for this section.\n'
            out += '\\newpage\n'
        out += '\\end{enumerate}\n'
        if key:
            out += '\\newpage'
            out += f'\\textbf{{Answers}} for Test {self.which_test}, Version - {self.seed}\n'
            out += '\\begin{enumerate}\n'
            for question_set in self.question_sets:
                out += '\\item\n'
                if question_set != []:
                    out += '\\begin{enumerate}\n'
                    out += f'\\item {question_set[0].format_answer}\n'
                    try:
                        if question_set[0].has_img_in_key:
                            out += """\\includegraphics[scale=0.6]{{{img_name}}}""".format(img_name='ans_for_' + question_set[0].module_name + '0')
                    except AttributeError:
                        pass
                    out += f'\\item {question_set[1].format_answer}\n'
                    try:
                        if question_set[1].has_img_in_key:
                            out += """\\includegraphics[scale=0.6]{{{img_name}}}""".format(img_name='ans_for_' + question_set[1].module_name + '1')
                    except AttributeError:
                        pass
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


class ProblemSet():
    def __init__(self, question_names, title, **kwargs):
        if 'seed' in kwargs:
            self.seed = kwargs['seed']
        else:
            self.seed = random.random()
        random.seed(self.seed)
        self.question_names = question_names
        question_set = []
        i = 1
        for question_name in question_names:
            question_module = getattr(questions, question_name)
            new_seed = (self.seed * i) % 1
            q = question_module.Question_Class(seed=new_seed)
            question_set.append(q)
        self.question_sets = [question_set]
        self.title = title

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
        title = self.title.replace(' ', '') + f'_v{self.seed}'
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
        # all_img_names = []
        for question_set in self.question_sets:
            i = 0
            # img_names = []
            for question in question_set:
                try:
                    if question.has_img:
                        img_name = '{qname}{i}'.format(qname=question.module_name, i=i)
                        question.save_img(img_name)
                    # img_names.append(img_name)
                except AttributeError:
                    pass
                if key:
                    try:
                        if question.has_img_in_key:
                            img_name = 'ans_for_{qname}{i}'.format(qname=question.module_name, i=i)
                            question.save_img(img_name)
                        # img_names.append(img_name)
                    except AttributeError:
                        pass
                i += 1
                # all_img_names.append(img_names)
        out = self.preamble
        # title_head = f"\\lhead{{\\textbf{{{self.book.display_name} - Test {self.which_test} v. {self.seed} \\\\Printed on \\today}}}}"
        # out += title_head + '\n\n'
        out += '\\begin{document}\n\n'
        # out += '\\thispagestyle{fancy}\n\n'
        header = f"""\\noindent
        \\begin{{tabular}}{{ p{{3.5in}} p{{3.2in}} }}
        \\hspace{{-1ex}}{{{self.title} }} & \\textbf{{Name: \\underline{{\\hspace{{2.65in}} }}}}\\\\
        \\hspace{{-1ex}}\\textbf{{Version - {self.seed} }} &   \\textbf{{Date: \\hspace{{2in}} }}\\
        \\end{{tabular}}
        \\hrule
        """
        out += header
        out += '\\begin{enumerate}\n'
        for question_set in self.question_sets:
            if question_set != []:
                for i in range(len(question_set)):
                    question = question_set[i]
                    # section_info = self.book.get_skill_info(question.module_name)[0]
                    # out += f'\\item {{\color{{gray}}({section_info[0]}.{section_info[1]})}} \n'
                    # out += '\\item \n'
                    # out += '\\begin{enumerate}\n'
                    out += f'\\item {question.format_given_for_tex}\n'
                    out += f"""Completely document the process by which you come to our answer.
                    (You will only receive half credit, otherwise.)"""
                    try:
                        question.has_img
                        out += """
                        \\begin{{flushright}}
                            \\includegraphics[scale=0.6]{{{img_name}}}
                        \\end{{flushright}}
                        \\vspace{{-9\\baselineskip}}
                        """.format(img_name=question.module_name + f'{i}')
                    except AttributeError:
                        pass
                    out += '\\vspace{12\\baselineskip}\n'
            else:
                out += f'\\item No questions have been constructed for this section.\n'
            out += '\\newpage\n'
        out += '\\end{enumerate}\n'
        if key:
            out += '\\newpage'
            out += '\\textbf{Answers:}\n'
            out += '\\begin{enumerate}\n'
            for question_set in self.question_sets:
                # out += '\\item\n'
                if question_set != []:
                    # out += '\\begin{enumerate}\n'
                    for i in range(len(question_set)):
                        out += f'\\item {question_set[i].format_answer}\n'
                        try:
                            if question_set[i].has_img_in_key:
                                out += """\\includegraphics[scale=0.6]{{{img_name}}}""".format(img_name='ans_for_' + question_set[i].module_name + f'{i}')
                        except AttributeError:
                            pass
                        # out += f'\\item {question_set[i].format_answer}\n'
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
solvingcompoundinequalities.due_date = datetime.datetime(2020, 9, 2)

# graphsofcompoundinequalities = Section('graphsofcompoundinequalities', "Graphs of Compound Inequalities", '/sections/graphs-of-compound-linear-inequalities')
intervalnotation = Section('intervalnotation', "Interval Notation", '/sections/interval_notation')
intervalnotation.add_to_questions('inequality_to_interval_notation',
                                    'interval_to_inequality_notation',
                                    'interval_notation_to_graph')
intervalnotation.due_date = datetime.datetime(2020, 9, 8)

absolutevalueequations = Section('absolutevalueequations', "Absolute Value Equations", '/sections/absolute-value-equations')
absolutevalueequations.add_to_questions('absolute_value_equation')
absolutevalueequations.due_date = datetime.datetime(2020, 9, 10)

absolutevalueinequalities = Section('absolutevalueinequalities', "Absolute Value Inequalities", '/sections/absolute-value-inequalities')
absolutevalueinequalities.add_to_questions('absolute_value_inequality',
                            'absolute_value_inequality_to_interval_notation',
                            'absolute_value_inequality_to_graph',
                            )
absolutevalueinequalities.due_date = datetime.datetime(2020, 9, 14)

absolutevalueequationspart2 = Section('absolutevalueequationspart2', "Absolute Value Equations, Part 2", '/sections/absolute-value-equations-challenge', True)
# print('challenge:', absolutevalueequationspart2.challenge)
absolutevalueequationspart2.add_to_questions(#'absolute_value_equation_plus_linear')
                                    #'absolute_value_equation_multi')
                                    'absolute_value_equation_multi_one_or_two')
#########################

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
simplegraphing.add_to_questions('graph_slope_intercept_from_english',
                                'graph_to_slope_intercept_form',
                                    'graph_slope_intercept')

pointslopeform = Section('pointslopeform', "Graph from Point Slope Form", '/sections/point-slope-form')
pointslopeform.add_to_questions('graph_point_slope_from_english',
                                'graph_point_slope',
                                 'description_to_point_slope_form')

graphfromtwopoints = Section('graphfromtwopoints', "Graph from Two Points", '/sections/graph-from-two-points')
graphfromtwopoints.add_to_questions('graph_to_point_slope_form',
                                    'two_points_to_equation')

linearfunctionsfromatable = Section('linearfunctionsfromatable', "Linear Functions From a Table", '/sections/linear_functions_from_a_table')
linearfunctionsfromatable.add_to_questions('altitude_temperature_problem',
                                            'altitude_temperature_problem_computation',
                                            'generic_table_hard',
                                            'generic_table_hard_computation')

###
standardformlines = Section('standardformlines', "Lines in Standard Form", '/sections/standard-form-lines')
standardformlines.add_to_questions('graph_standard_form_line')

verticalorhorizontal = Section('verticalorhorizontal', "Horizontal and Vertical Lines", '/sections/vertical-or-horizontal')
verticalorhorizontal.add_to_questions('vertical_or_horizontal_graph_to_equation',
                                    'vertical_or_horizontal')

parallelorperpendicular = Section('parallelorperpendicular', "Parallel and Perpendicular Lines", '/sections/parallel-and-perpendicular')
parallelorperpendicular.add_to_questions('parallel_perpendicular_to_point_slope_form',
                                        'parallel_perpendicular_to_point_slope_form',
                                         'vertical_or_horizontal_info_to_equation',
                                        'vertical_or_horizontal_graph_from_description')

systemsofequations = Section('systemsofequations', "Systems of Equations", '/sections/systems-of-equations')
systemsofequations.add_to_questions('how_many_solutions_to_system')

solvingbyelimination = Section('solvingbyelimination', "Solving by Elimination", '/sections/solving-by-elimination')
solvingbyelimination.add_to_questions('solve_by_elimination')

solvebysubstitution = Section('solvebysubstitution', 'Solving by Substitution', '/sections/solving-by-substitution')
solvebysubstitution.add_to_questions('solve_by_substitution')

applicationsoflinearsystems = Section('applicationsoflinearsystems', "Applications of Linear Systems", '/sections/applications-of-linear-systems')
applicationsoflinearsystems.add_to_questions('we_lost_the_receipts',
                                                'air_travel',
                                                'gold_alloy')

solvingbyeliminationthreeequationsonesolution = Section('solvingbyeliminationthreeequationsonesolution', "Solving By Elimination: Intro to Three Unknowns", '/sections/solving-by-elimination-three-equations-intro', True)
solvingbyeliminationthreeequationsonesolution.add_to_questions('solve_by_elimination_three',)
                                                                # 'vertex_form_from_three_points')
#########
graphofabsolutevaluebasic = Section('graphofabsolutevaluebasic', "Graphs of Absolute Value Functions: Basic Transformations", '/sections/graph-of-absolute-value')
graphofabsolutevaluebasic.add_to_questions('graph_absolute_value_basic',
                                    'graph_absolute_value_basic_to_equation')

graphofabsolutevaluefull = Section('graphofabsolutevaluefull', "Graphs of Absolute Value Functions: The Full Treatment", '/sections/graph-of-absolute-value-scaled')
graphofabsolutevaluefull.add_to_questions('graph_absolute_value',
                                        'graph_absolute_value_to_equation')
#########

quadratics_intro = Section('quadratics_intro', "Introduction to Quadratics", '/sections/quadratics_intro')

warmupwithquadratics = Section('warmupwithquadratics', 'Warm-up with Quadratics', '/sections/warm-up-with-quadratics')
warmupwithquadratics.add_to_questions('vertex_form_to_standard_form',
                                'intercept_form_to_standard_form')

vertexform = Section('vertexform', 'Quadratics in Vertex Form', '/sections/vertex-form')
vertexform.add_to_questions('graph_vertex_form',
                            'graph_vertex_form_to_equation')

interceptform = Section('interceptform', 'Quadratics in Intercept Form', '/sections/intercept-form')
interceptform.add_to_questions('graph_intercept_form',
                             'graph_intercept_form_to_equation')

standardform = Section('standardform', 'Quadratics in Standard Form', '/sections/standard-form')
standardform.add_to_questions('standard_form_to_vertex_form',
                                'graph_standard_form')

maxmin = Section('maxmin', "Max/Min Problems", '/sections/max-min-problems')
maxmin.add_to_questions('generic_max_min',
                        'cannonball_problem',
                         'max_revenue_problem')

factoringtrinomialslevel1 = Section('factoringtrinomialslevel1', "Factoring Trinomials, Part 1", '/sections/factoring-trinomials-part1')
factoringtrinomialslevel1.add_to_questions('factor_trinomials_level1',
                                        'factor_trinomials_level1',
                                            'factoring_warm_up')

solvingquadraticspart1 = Section('solvingquadraticspart1', "Solving by Factoring, Part 1", '/sections/solving-quadratics-part1')
solvingquadraticspart1.add_to_questions('solving_by_factoring_level1')

specialpatterns = Section('specialpatterns', "Special Patterns", '/sections/special-patterns')
specialpatterns.add_to_questions('factor_special_patterns')

factoringbygrouping = Section('factoringbygrouping', "Factoring by Grouping", '/sections/factoring-by-grouping')
factoringbygrouping.add_to_questions('factoring_by_grouping')

factoringtrinomialslevel2 = Section('factoringtrinomialslevel2', "Factoring Trinomials, Part 2", '/sections/factoring-trinomials-part2')
factoringtrinomialslevel2.add_to_questions('factor_trinomials_level2')

quadraticpattern = Section('quadraticpattern', "Quadratic Pattern", '/sections/quadratic-pattern')
quadraticpattern.add_to_questions('quadratic_pattern')

mixedpracticeplusgcf = Section('mixedpracticeplusgcf', "Putting It All Together", '/sections/putting-it-all-together-factoring')
mixedpracticeplusgcf.add_to_questions('mixed_practice_plus_gcf')

solvingquadraticspart2 = Section('solvingquadraticspart2', "Solving by Factoring, Part 2", '/sections/solving-quadratics-part2')
solvingquadraticspart2.add_to_questions('solving_by_factoring_level2')

solvingquadraticsonlyonex = Section('solvingquadraticsonlyonex', "Solving Quadratics: Only One x", '/sections/solving-quadratics-only-one-x')
solvingquadraticsonlyonex.add_to_questions('quadratic_only_one_x')

solvingbycompletingthesquare = Section('solvingbycompletingthesquare', "Solving by Completing the Square", '/sections/solving-by-completing-the-square')
solvingbycompletingthesquare.add_to_questions('solve_by_completing_the_square')

solvingbythequadraticformula = Section('solvingbythequadraticformula', "Solving by the Quadratic Formula", '/sections/solving-by-the-quadratic-formula')
solvingbythequadraticformula.add_to_questions('solve_by_quadratic_formula')

solvingquadraticsapplications = Section('solvingquadraticsapplications', "Solving Quadratics: Applications", '/sections/solving-quadratics-applications')
solvingquadraticsapplications.add_to_questions('cannonball_hits_target',
                                                'celebratory_gunfire')
#######################################
polynomials_intro = Section('polynomials', "Polynomials", '/sections/polynomials-intro')

polynomialsaddingandsubtracting = Section('polynomialsaddingandsubtracting', "Adding and Subtracting Polynomials", '/sections/polynomials-adding-and-subtracting')
polynomialsaddingandsubtracting.add_to_questions('adding_or_subtracting_polynomials')

polynomialsmultiplying = Section('polynomialsmultiplying', "Multiplying Polynomials", '/sections/polynomials-multiplying')
polynomialsmultiplying.add_to_questions('multiplying_polynomials')


polynomialsdividing = Section('polynomialsdividing', "Dividing Polynomials", '/sections/polynomials-dividing')
polynomialsdividing.add_to_questions('long_division_of_polynomials',
                                        'long_division_of_polynomials_harder',)

syntheticdivision = Section('syntheticdivision', "Synthetic Division", '/sections/polynomials-synthetic-division')
syntheticdivision.add_to_questions('synthetic_division_of_polynomials',
                                    'synthetic_division_of_polynomials_harder')

completefactorizationpart1 = Section('completefactorizationpart1', "Complete Factorization: Part 1", '/sections/complete-factorization-part1')
completefactorizationpart1.add_to_questions('complete_factorization_level1_three_factors',
                                            'complete_factorization_level1_three_nice_factors')

imaginaryelementpart1 = Section('imaginaryelementpart1', "Imaginary Element, Part 1", '/sections/imaginary-element-part1')
imaginaryelementpart1.add_to_questions('imaginary_element_level1',
                                        'imaginary_element_level2',
                                        'imaginary_element_level3',
                                        'imaginary_element_level4',
                                        )

imaginaryelementpart2 = Section('imaginaryelementpart2', "Imaginary Element, Part 2", '/sections/imaginary-element-part2')
imaginaryelementpart2.add_to_questions('quadratic_can_be_imaginary',
                                        'quadratic_force_imaginary')
#######################################
linearfunctions_intro = Section('linear_functions', "Linear Functions", '/sections/linear-functions')



factoring1 = Section('factoring1', "Factoring - Level 1", '/sections/factoring-coeff-of-one')
# factoring1.due_date = datetime.datetime(2020, 8, 28)



# quadraticpattern.due_date = datetime.datetime(2020, 12, 2)
#
#############################


challenge_intro = Section('challenge_intro', "Challenge Intro", '/sections/challenge_intro')
##############################
# Construction of book, Algebra2 -- collecting, "binding" sections, frontpages, etc.
nuts_and_bolts_of_algebra = Division('chapter', 'Nuts and Bolts of Algebra',
                                [solveforx,
                                linearinequalities,
                                graphsoflinearinequalities,
                                solvingcompoundinequalities,
                                intervalnotation,
                                absolutevalueequations,
                                absolutevalueinequalities,])
nuts_and_bolts_of_algebra.set_frontpage(nutsandboltsofalgebra)

functions_and_the_coordinate_plane = Division('chapter', "Functions and the Coordinate Plane",
                                    [basicfunctionsinatableandwords,
                                    functionnotation,
                                    functioncomposition,
                                    simplegraphing,
                                    pointslopeform,
                                    graphfromtwopoints,
                                    linearfunctionsfromatable,
                                    standardformlines,
                                    verticalorhorizontal,
                                    parallelorperpendicular,
                                    systemsofequations,
                                    solvingbyelimination,
                                    solvebysubstitution,
                                    applicationsoflinearsystems,
                                    graphofabsolutevaluebasic,
                                    graphofabsolutevaluefull,
                                    ])
functions_and_the_coordinate_plane.set_frontpage(functionsandthecoordinateplane_intro)



quadratics = Division('chapter', "Quadratic Functions",
                                [warmupwithquadratics,
                                vertexform,
                                interceptform,
                                standardform,
                                maxmin,
                                factoringtrinomialslevel1,
                                solvingquadraticspart1,
                                specialpatterns,
                                factoringbygrouping,
                                factoringtrinomialslevel2,
                                quadraticpattern,
                                mixedpracticeplusgcf,
                                solvingquadraticspart2,
                                solvingquadraticsonlyonex,
                                solvingbycompletingthesquare,
                                solvingbythequadraticformula,
                                solvingquadraticsapplications,
                                ])
quadratics.set_frontpage(quadratics_intro)

polynomials = Division('chapter', 'Polynomials',
                                [polynomialsaddingandsubtracting,
                                polynomialsmultiplying,
                                polynomialsdividing,
                                syntheticdivision,
                                completefactorizationpart1,
                                imaginaryelementpart1,
                                imaginaryelementpart2,
                                ])
polynomials.set_frontpage(polynomials_intro)

algebra2_challenge = Division('chapter', "Challenge Sections",
                                    [absolutevalueequationspart2,
                                    solvingbyeliminationthreeequationsonesolution])
algebra2_challenge.set_frontpage(challenge_intro)



main = Division('main', 'Main Matter', [nuts_and_bolts_of_algebra,
                                        functions_and_the_coordinate_plane,
                                        quadratics,
                                        polynomials,
                                        algebra2_challenge])

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
