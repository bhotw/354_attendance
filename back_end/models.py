from back_end.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    emergency_contact_name = db.Column(db.String(100), nullable=True)
    emergency_contact_phone = db.Column(db.String(20), nullable=True)
    parents_email = db.Column(db.String(120), nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'


class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    sign_in_time = db.Column(db.Time, nullable=True)
    sign_out_time = db.Column(db.Time, nullable=True)
    days_hours = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Attendance ID {self.id} on {self.date}>'


class WorkshopHours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total_hours = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<WorkshopHours ID {self.id} on {self.date}>'
