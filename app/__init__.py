from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

from app import views
