from app import app, db
from app.models import (Student,
                        StudentAnswer,
                        BugReport,
                        UserGradeInfo,
                        UserSectionStatus)
from app.books import Algebra2, SevenTest, CustomAssessment

@app.shell_context_processor
def make_shell_context():
    # emily = Student.query.filter_by(username='emilymasten').first()
    # section_status = UserSectionStatus.query.filter_by(user_id=emily.id, section_name='solveforx').first()
    return {'db': db,
            'Student': Student,
            'StudentAnswer': StudentAnswer,
            'BugReport': BugReport,
            'UserGradeInfo': UserGradeInfo,
            'Algebra2': Algebra2,
            'SevenTest': SevenTest,
            'UserSectionStatus': UserSectionStatus,
            'early' : Algebra2.get_sections_by_string('3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14, 3.15, 3.16, 3.17, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9'),
            'new' : Algebra2.get_sections_by_string('5.1, 5.2, 5.3, 5.4, 5.5'),
            'CustomAssessment' : CustomAssessment,
            }
