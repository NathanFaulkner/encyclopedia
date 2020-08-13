from app import app, db
from app.models import Student, StudentAnswer, BugReport, UserGradeInfo
from app.books import Algebra2, SevenTest

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Student': Student,
            'StudentAnswer': StudentAnswer,
            'BugReport': BugReport,
            'UserGradeInfo': UserGradeInfo,
            'Algebra2': Algebra2,
            'SevenTest': SevenTest}
