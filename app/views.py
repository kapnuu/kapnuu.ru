from app import app, db, models
from werkzeug.security import check_password_hash
from flask import redirect, render_template, flash, request, make_response, send_from_directory, session
from sqlalchemy import and_
import logging
import random
import string
from datetime import datetime

COOKIE_NAME = 'kapnuu-cat'


def verify_password(username, password):
    print(app.config['ROOT'])
    print(app.config['ROOT_PASSWORD'])
    if username == app.config['ROOT']:
        if check_password_hash(app.config['ROOT_PASSWORD'], password):
            session['logged_in'] = True
            return True
    return False


def get_cookie(req):
    cookie = req.cookies.get(COOKIE_NAME)
    return cookie


def new_cookie():
    cookie_length = 32

    while True:
        new_c = ''.join(random.sample(string.ascii_letters + string.digits, cookie_length))

        existing_guest = models.Guest.query.filter(models.Guest.cookie == new_c).first()
        if existing_guest is None:
            break

    return new_c


def print_cats():
    cats = models.Cat.query.filter(models.Cat.disabled == False).order_by(models.Cat.index).all()

    for c in cats:
        logging.debug('%s %s' % (c.index, c.url))


def get_guest(create_new=True):
    guest = None
    cookie = get_cookie(request)
    if cookie is not None:
        logging.debug('cookie is %s' % cookie)
        guest = models.Guest.query.filter(cookie == models.Guest.cookie).first()
        if guest is not None:
            logging.debug('guest found, last viewed = %s' % guest.last_cat_id)
        else:
            guest = models.Guest(cookie=cookie, last_cat_id=-1)
    elif create_new:
        cookie = new_cookie()
        logging.debug('new cookie is %s' % cookie)
        guest = models.Guest(cookie=cookie, last_cat_id=-1)
    return guest, cookie


def create_db():
    engine = db.get_engine(app)
    try:
        engine.execute('TRUNCATE TABLE cat;')
    except Exception as ex:
        logging.error('Truncate `cat` table failed: %s' % ex)
        engine.execute('DELETE FROM cat;')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect('/')
    if request.form:
        username = request.form.get('username')
        password = request.form.get('password')
        if verify_password(username, password):
            session['logged_in'] = True
            return redirect('/cat')
        else:
            flash('invalid username or password', category='error')
    return render_template('login.htm')


@app.route('/')
@app.route('/index')
def index():
    print_cats()

    guest, cookie = get_guest()

    if guest.last_cat_id == -1:
        cat = models.Cat.query.filter(and_(models.Cat.disabled == False, models.Cat.index >= 0)).first()
    else:
        last_seen = guest.last_cat_id if guest.last_cat_id is not None else -1
        cat = models.Cat.query.filter(and_(models.Cat.disabled == False, models.Cat.index >= last_seen)).order_by(models.Cat.index).first()
    if cat is None:
        cat = models.Cat.query.filter(models.Cat.disabled == False).order_by(models.Cat.index).first()
    if cat is None:
        flash('there is nobody here :-(')
        return redirect('/login')

    guest.t_seen = datetime.utcnow()
    guest.last_cat_id = cat.index
    db.session.add(guest)
    db.session.commit()

    resp = make_response(render_template('index.htm', cat=cat, cookie=cookie, logged_in=session.get('logged_in')))
    resp.set_cookie(COOKIE_NAME, cookie)
    return resp


@app.route('/cat/next', methods=['GET'])
def next_cat_get():
    logging.debug('next cat requested by GET')
    return redirect('/', 302)


@app.route('/cat/next', methods=['POST'])
def next_cat():
    logging.debug('next cat requested')

    print_cats()

    guest, cookie = get_guest(create_new=False)
    if guest:
        guest.last_cat_id += 1
        db.session.add(guest)
        db.session.commit()

    return redirect('/')


@app.route('/cat', methods=['GET'])
def list_cats():
    if not session.get('logged_in'):
        return redirect('/login')

    cats = models.Cat.query.order_by(models.Cat.index).all()
    return render_template('list.htm', cats=cats, logged_in=session.get('logged_in'))


@app.route('/cat', methods=['POST'])
def update_cats():
    if not session.get('logged_in'):
        return redirect('/login')

    cats = {}
    data = request.values
    indices = [x for x in data if x.startswith('cat_idx')]
    for datum in indices:
        cat_id = datum[7:]
        cat = {
            'comment': data.get('cat_comment' + cat_id),
            'idx': int(data[datum]),
            'enabled': bool(data.get('cat_enable' + cat_id))
        }
        cats[int(cat_id)] = cat

    new_cat = data.get('cat_new')
    if new_cat:
        cat = {
            'comment': '',
            'idx': max([int(data[x]) for x in indices]) + 1,
            'enabled': True,
            'url': new_cat,
        }
        cats[0] = cat

    # logging.debug([x + ' -> ' + data[x] for x in data])
    logging.debug(cats)
    return redirect('/cat')


@app.route('/create')
def create_new_db():
    if not session.get('logged_in'):
        return redirect('/login')

    create_db()

    logging.debug('New DB created')

    flash('new db created')
    return redirect('/cat')


@app.route('/create-test')
def create_test_db():
    if not session.get('logged_in'):
        return redirect('/login')

    create_db()

    cat = models.Cat(url='/static/DSC_0407.jpg', index=0,
                     width=415, height=620, disabled=False, comment='cat #0')
    db.session.add(cat)
    cat = models.Cat(url='/static/DSC_0389.jpg', index=1,
                     width=415, height=620, disabled=False, comment='cat #1')
    db.session.add(cat)
    cat = models.Cat(url='/static/DSC_0424.jpg', index=2,
                     width=415, height=620, disabled=False, comment='cat #2')
    db.session.add(cat)
    cat = models.Cat(url='/static/DSC_2105.jpg', index=3,
                     width=620, height=415, disabled=False, comment='cat #3')
    db.session.add(cat)
    db.session.commit()

    logging.debug('Test DB created')

    flash('test db created')
    return redirect('/')
