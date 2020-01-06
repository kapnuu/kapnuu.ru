import os

__author__ = 'pav'

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
# SECRET_KEY = 'everybody-love-cats:)'
SECRET_KEY = os.urandom(16)

database_uri = os.environ.get('DATABASE_URL')
if database_uri is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = database_uri

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
