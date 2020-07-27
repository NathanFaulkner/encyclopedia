from app import app, db
from app.models import Student, StudentAnswer, UserGradeInfo

@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Student': Student,
            'StudentAnswer': StudentAnswer,
            'UserGradeInfo': UserGradeInfo}
