from app import app, db, models
from flask import redirect, render_template, flash, url_for, request, make_response
import logging
import random
import string
from datetime import datetime

COOKIE_NAME = 'kapnuu-cat'


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
    cats = models.Cat.query.all()

    for c in cats:
        logging.debug('%s %s' % (c.id, c.url))


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


@app.route('/')
@app.route('/index')
def index():
    logging.debug('index requested')

    print_cats()

    guest, cookie = get_guest()

    if guest.last_cat_id == -1:
        cat = models.Cat.query.filter(models.Cat.id >= 0).first()
    else:
        cat = models.Cat.query.filter(models.Cat.id >= guest.last_cat_id).first()
    if cat is None:
        cat = models.Cat.query.order_by(models.Cat.id).first()
    if cat is None:
        return redirect('/create', 302)

    guest.t_seen = datetime.utcnow()
    guest.last_cat_id = cat.id
    db.session.add(guest)
    db.session.commit()

    resp = make_response(render_template('index.htm', cat=cat, cookie=cookie))
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


@app.route('/create')
def create_test_db():
    for x in models.Cat.query.all():
        db.session.delete(x)

    cat = models.Cat(url='/static/DSC_0407.jpg',
                     width=415, height=620, disabled=False, comment='cat #0')
    db.session.add(cat)
    cat = models.Cat(url='/static/DSC_0389.jpg',
                     width=415, height=620, disabled=False, comment='cat #1')
    db.session.add(cat)
    cat = models.Cat(url='/static/DSC_0424.jpg',
                     width=415, height=620, disabled=False, comment='cat #2')
    db.session.add(cat)
    cat = models.Cat(url='/static/DSC_2105.jpg',
                     width=620, height=415, disabled=False, comment='cat #3')
    db.session.add(cat)
    db.session.commit()
    logging.debug('New test DB created')

    flash('New test DB created')
    return redirect('/')
