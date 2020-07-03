#from app.sections import *

#alphabet = 'abcdefghijklmnopqrstuvwxyz'


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


    def get_division_into(self):
        if subdivisions is not None:
            return subdivisions[0].category
        else:
            return None

#########################
# Free Sections -- not "bound" in a book
algebra2 = Section('algebra2', "Algebra 2", '/sections/algebra2')
factoring1 = Section('factoring1', "Factoring - Level 1", '/sections/factoring-coeff-of-one')
polynomials_intro = Section('polynomials', "Polynomials", '/sections/polynomials-intro')
quadraticpattern = Section('quadraticpattern', "Quadratic Pattern", '/sections/quadratic-pattern')
#
#############################

##############################
# Construction of book, Algebra 2 -- collecting, "binding" sections, frontpages, etc.
polynomials = Division('chapter', 'Polynomials', [factoring1, quadraticpattern])
#polynomials.intro = polynomials_intro
polynomials.set_frontpage(polynomials_intro)

main = Division('main', 'Main Matter', [polynomials])

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
