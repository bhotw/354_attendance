from datetime import date, datetime
from back_end.models import Attendance, db

def auto_sing_out():
    
    today_date = date.today()
    