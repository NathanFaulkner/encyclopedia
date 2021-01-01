from app import app, db
from app.models import (Student,
                        StudentAnswer,
                        BugReport,
                        UserGradeInfo,
                        UserSectionStatus)
from app.books import Algebra2, SevenTest

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
            # 'emily': emily,
            # 'section_status': section_status,
            }
