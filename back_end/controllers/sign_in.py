from datetime import datetime
from back_end.extensions import db


def sign_in(reader_id, date, sign_in_time):
    from back_end.models import Attendance
    try:
        date = datetime.strftime(date, '%Y-%m-%d')
        sign_in_time = datetime.strftime(sign_in_time, '%H:%M:%S')

        new_record = Attendance(id=reader_id, date=date, sign_in_time=sign_in_time)

        db.session.add(new_record)
        db.commit()

        message = "Sign In Successful!!!"

        return new_record
    except Exception as e:
        return f"Error: {str(e)}"
