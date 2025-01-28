from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from functools import wraps
from werkzeug.security import check_password_hash
from back_end.models import User, Attendance
from back_end.extensions import db
from datetime import datetime
from back_end.admin.models import AdminUser
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

admin_bp = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')


# Login form for admin
class AdminLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# Decorator to check if admin is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin.admin_login'))
        return f(*args, **kwargs)

    return decorated_function


# Admin login route
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()  # Use the FlaskForm for validation
    if request.method == 'POST' and form.validate_on_submit():  # Validate form
        email = form.email.data
        password = form.password.data

        admin = AdminUser.query.filter_by(email=email).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_logged_in'] = True
            session['admin_email'] = admin.email
            flash("Login successful!", "success")
            return redirect(url_for('admin.admin_home'))
        else:
            flash("Invalid username or password. Please try again.", "error")
            return redirect(url_for('admin.admin_login'))

    return render_template('admin_login.html', form=form)


# Admin home route (dashboard)
@admin_bp.route('/')
@login_required
def admin_home():
    return render_template('admin_base.html')


# Members Management Route
@admin_bp.route('/members', methods=['GET'])
@login_required
def manage_members():
    mentors = User.query.filter_by(role='mentor').all()
    students = User.query.filter_by(role='student').all()
    return render_template('members.html', mentors=mentors, students=students)


# Attendance Records Management Route
@admin_bp.route('/attendance', methods=['GET', 'POST'])
@login_required
def manage_attendance():
    attendance_records = Attendance.query.all()
    return render_template('attendance.html', records=attendance_records)


# Manual Sign-In/Sign-Out Route
@admin_bp.route('/manual', methods=['GET', 'POST'])
@login_required
def manual_sign_in_out():
    members = User.query.all()
    if request.method == 'POST':
        member_id = request.form['member']
        sign_in_time = request.form['sign_in_time']
        sign_out_time = request.form['sign_out_time']

        # Validate and process attendance records (check and store)
        if not sign_in_time or not sign_out_time:
            flash("Please provide both sign-in and sign-out times.", "error")
        else:
            # Create or update attendance record here
            flash("Manual sign-in/out recorded successfully.", "success")
            return redirect(url_for('admin.manual_sign_in_out'))

    return render_template('manual.html', members=members)


# Active Members Route
@admin_bp.route('/activemembers')
@login_required
def active_members():
    active_members = Attendance.query.filter_by(sign_out_time=None).all()
    return render_template('activemembers.html', members=active_members)


# Timesheet Management Route
@admin_bp.route('/timesheet', methods=['GET', 'POST'])
@login_required
def timesheet():
    if request.method == 'POST':
        member_id = request.form.get('member')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        # Filter attendance records based on dates and member
        timesheet_records = Attendance.query.filter(
            Attendance.date.between(start_date, end_date),
            Attendance.member_id == member_id
        ).all()

        return render_template('timesheet.html', records=timesheet_records)

    members = User.query.all()
    return render_template('timesheet.html', members=members)
