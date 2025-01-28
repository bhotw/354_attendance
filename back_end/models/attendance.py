# models/attendance.py
from extensions import db
from datetime import datetime

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    sign_in_time = db.Column(db.Time, nullable=True)
    sign_out_time = db.Column(db.Time, nullable=True)
    days_hours = db.Column(db.Float, nullable=True)  # Total hours worked

    # Foreign key to User
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f'<Attendance ID {self.id} on {self.date}>'