from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from extensions import db
from models.user import User
from models.attendance import Attendance
from app import app


with app.app_context():
    db.create_all()

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()