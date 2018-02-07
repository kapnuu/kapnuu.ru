from app import app
from flask import request

@app.route('/')
@app.route('/index')
def index():
    html = '<h3>kapnuu.ru</h3>'
    try:
        html += '<pre>'
        html += str(request.headers)
        #for h in request.headers:
        #    html += '%s: %s\n' % (h, request.headers[h])
        html += '</pre>this will be <strong>kapnuu</strong> personal site'       
    except Exception as ex:
        print('%s' % ex)
    return html
