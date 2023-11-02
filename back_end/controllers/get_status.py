from datetime import datetime
from back_end.models import Attendance


def get_status(id):
    try:
        today_date = datetime.now().date()

        sign_in_record = Attendance.query.filter_by(id=id, date=today_date).first()

        if sign_in_record:
            sign_in_time = sign_in_record.sign_in_time
            current_time = datetime.now().time()

            sign_in_datetime = datetime.combine(today_date, sign_in_time)
            current_datetime = datetime.combine(today_date, current_time)
            duration = current_datetime - sign_in_datetime

            return {
                'sign_in_time': sign_in_time.strftime('%H:%M:%S'),
                'time_in_shop': str(duration)
            }
        else:
            return {
                'message': 'You did not sing in yet. Please sign in.'
            }
    except Exception as e:
        return f"Error: {str(e)}"
