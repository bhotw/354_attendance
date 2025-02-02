# models/user.py
from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    card_id = db.Column(db.BigInteger, unique=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    parents_email = db.Column(db.String(120), nullable=True)

    # Relationship with Attendance
    attendance_records = db.relationship("Attendance", backref="user", lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'