from app.sections import *

alphabet = 'abcdefghijklmnopqrstuvwxyz'


class Book():
    def __init__(self, name, front, main, end):
        self.name = name
        self.front = front
        self.main = main
        self.end = end

class Section():
    def __init__(self, category, section, numbered=True):
        self.category = category
        self.display_name = section.d.get('name')
        self.section = section
        self.numbered=numbered
        self.view_name = section.d.get('view_name')
        self.template_path = section.d.get('template_path')

class Division():
    def __init__(self, category, display_name, subdivisions, template_path=None):
        self.category = category
        self.display_name = display_name
        self.subdivisions = subdivisions
        self.template_path = template_path


    def get_division_into(self):
        if subdivisions is not None:
            return subdivisions[0].category
        else:
            return None




factoring1 = Section('section', factoring1, numbered=True)
quadraticpattern = Section('section', quadraticpattern, numbered=True)
polynomials_intro = Section('intro', polynomials, numbered=False)
polynomials = Division('chapter', 'Polynomials', [factoring1, quadraticpattern])
#polynomials.intro = polynomials_intro
polynomials.template_path=polynomials_intro.template_path
polynomials.view_name = polynomials_intro.view_name
polynomials.frontpage = polynomials_intro

main = Division('main', 'Main Matter', [polynomials])
Algebra2 = Division('book', 'Algebra 2', {'front': None, 'main': main, 'end': None})
Algebra2.name_for_path = 'Algebra2'
Algebra2.view_name = algebra2.d['view_name']

Library = Division('library', 'Books', [Algebra2])
####
# Example book could be [foreword, dedication, preface, introduction, chapter1, ..
# ..., chapter n, Appendix A, Appendix B, ...].
####
