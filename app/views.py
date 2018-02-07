from app import app
from flask import request

@app.route('/')
@app.route('/index')
def index():
    html = '<h3>kapnuu.ru</h3><pre>'
    for h in request.headers:
        html += h + ': ' + request.headers[h] + '\n'
    html += '</pre>this will be <strong>kapnuu</strong> personal site'
    return html
