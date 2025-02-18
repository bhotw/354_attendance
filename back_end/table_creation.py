
from extensions import db
from models.user import User
from models.attendance import Attendance
from app import app
from sqlalchemy import inspect


with app.app_context():
    db.create_all()

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()