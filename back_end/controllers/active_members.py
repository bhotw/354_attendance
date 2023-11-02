from datetime import date
from back_end.models import User, Attendance, db

def active_members():

    today_date = date.today()

    active_members = db.session.query(User).join(Attendance, (User.id == Attendance.id) & (Attendance.date == today_date)).filter(Attendance.sign_out_time == None).all()

    return active_members