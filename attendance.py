from flask import Flask
from config import SQLALCHEMY_DATABASE_URL, SECRE_KEY
from flask_sqlalchem import SQLAlchemy

from back_end.controllers.registration import Registration
from back_end.models import User


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URL'] = SQLALCHEMY_DATABASE_URL
app.config['SECRE_KEY'] = SECRE_KEY

db = SQLAlchemy(app)

