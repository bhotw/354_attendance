from flask import Flask
from routes import my_blueprint
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()


from back_end.controllers.registration import Registration

db = SQLAlchemy(app)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(my_blueprint)


    # app.config.from_object('config')
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # Set the configuration
    app.config['SECRET_KEY'] = SECRET_KEY

    csrf = CSRFProtect(app)

    db.init_app(app)

    return app



