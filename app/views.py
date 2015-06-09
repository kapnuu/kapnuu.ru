from app import app

@app.route('/')
@app.route('/index')
def index():
    return "This will be a kapnuu personal site:)"
