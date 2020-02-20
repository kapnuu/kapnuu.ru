import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

__author__ = 'pav'

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, verbose=True)

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

ROOT = os.getenv('ROOT')
if ROOT:
    ROOT_PASSWORD = generate_password_hash(os.getenv('ROOT_PASSWORD'))
else:
    ROOT_PASSWORD = None
