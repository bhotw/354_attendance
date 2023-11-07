import csv 
from datetime import date
from back_end.models import Attendance, User, db

def file_generator():

    today_date = date.today()

    Attendance_data = db.query(Attendance, User).filter(Attendance.data == today_date, Attendance.id == User.id).all()

    if not Attendance_data:
        return
    
    csv_filename = f"attendance_{today_date}.csv"

    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Name", "Role", "Date", "Sign In Time", "Sign Out Time", "Days Hours"])

        for entry, user in Attendance_data:
            writer.writerow([entry.id, user.name, user.role, entry.date, entry.sign_in_time, entry.sign_out_time, entry.days_hours])

    return csv_filename
