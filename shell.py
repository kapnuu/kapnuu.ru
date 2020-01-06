from app import app, db
from app.models import Cat, Guest


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Cat': Cat, 'Guest': Guest}

# set FLASK_APP=shell.py
