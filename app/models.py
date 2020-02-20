from app import db

__author__ = 'pav'


class Cat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, index=True)
    url = db.Column(db.String(320))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    t_check = db.Column(db.DateTime)
    disabled = db.Column(db.Boolean)
    comment = db.Column(db.String(512))


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cookie = db.Column(db.String(32), index=True)
    t_seen = db.Column(db.DateTime)
    last_cat_id = db.Column(db.Integer)
    deleted = db.Column(db.Boolean)
