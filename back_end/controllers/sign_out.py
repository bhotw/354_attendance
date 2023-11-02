from datetime import datetime
from back_end.models import Attendance, WorkshopHours
from attendance import db


def sign_out(id, name):
    try:
        # Get today's date
        today_date = datetime.now().date()
        current_time = datetime.now().time()

        # Check if the user signed in today
        sign_in_record = Attendance.query.filter_by(id=id, date=today_date).first()

        if sign_in_record:
            sign_in_time = sign_in_record.sign_in_time
            sign_in_datetime = datetime.combine(today_date, sign_in_time)
            sign_out_datetime = datetime.combine(today_date, current_time)
            duration = sign_out_datetime - sign_in_datetime
            hours_worked = duration.total_seconds() / 3600

            sign_in_record.sign_out_time = current_time
            sign_in_record.days_hours = hours_worked

            db.session.commit()

            workshop_hours = WorkshopHours.query.filter_by(id=id).first()

            if workshop_hours:
                workshop_hours.total_hours += hours_worked

                db.session.commit()

                return {
                    'sign_out_time': current_time.strftime('%H:%M:%S'),
                    'hours_worked': hours_worked,
                    'total_hours': workshop_hours.total_hours
                }
            else:
                return "WorkshopHours record not found for this user."

        else:
            new_sign_out_record = Attendance(id=id, date=today_date, sign_out_time=current_time)
            db.session.add(new_sign_out_record)
            db.session.commit()
            return "User did not sign in today. A sign-out record has been created."

    except Exception as e:
        return f"Error: {str(e)}"