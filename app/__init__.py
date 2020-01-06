from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
import os

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
app._static_folder = os.path.abspath("static/")

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

from app import views
