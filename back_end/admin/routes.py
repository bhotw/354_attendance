
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.security import check_password_hash
from back_end.models import User, Attendance
from back_end.database import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)
    return decorated_function
@admin_bp.route('/')
def admin_home():
    return render_template('admin_base.html')

# Members Management
@admin_bp.route('/members', methods=['GET'])
@login_required
def manage_members():
    mentors = User.query.filter_by(role='mentor').all()
    students = User.query.filter_by(role='student').all()
    return render_template('members.html', mentors=mentors, students=students)

# Attendance Records Management
@admin_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def manage_attendance():
    attendance_records = Attendance.query.all()
    return render_template('attendance.html', records=attendance_records)

# Manual Sign-In/Sign-Out Form
@admin_bp.route('/manual', methods=['GET', 'POST'])
@login_required
def manual_sign_in_out():
    members = User.query.all()
    if request.method == 'POST':
        member_id = request.form['member']
        sign_in_time = request.form['sign_in_time']
        sign_out_time = request.form['sign_out_time']
        # Logic to manually insert or update attendance records
        flash("Manual sign-in/out recorded successfully.", "success")
        return redirect(url_for('admin.manual_sign_in_out'))
    return render_template('manual.html', members=members)

# Active Members View
@admin_bp.route('/activemembers')
@login_required
def active_members():
    active_members = Attendance.query.filter_by(sign_out_time=None).all()
    return render_template('activemembers.html', members=active_members)

# Timesheet Management
@admin_bp.route('/timesheet', methods=['GET', 'POST'])
@login_required
def timesheet():
    if request.method == 'POST':
        member_id = request.form.get('member')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        # Filter and calculate attendance hours
        timesheet_records = Attendance.query.filter(
            Attendance.date.between(start_date, end_date),
            Attendance.member_id == member_id
        ).all()
        return render_template('timesheet.html', records=timesheet_records)
    members = User.query.all()
    return render_template('timesheet.html', members=members)
