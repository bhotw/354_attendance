from flask import Flask
from your_app.routes import your_blueprint

from config import SQLALCHEMY_DATABASE_URI, SECRE_KEY
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()


from back_end.controllers.registration import Registration



app = Flask(__name__)
app.register_blueprint(your_blueprint)


# app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # Set the configuration
# app.config['SQLALCHEMY_DATABASE_URL'] = SQLALCHEMY_DATABASE_URL
# app.config['SECRE_KEY'] = SECRE_KEY

db = SQLAlchemy(app)

