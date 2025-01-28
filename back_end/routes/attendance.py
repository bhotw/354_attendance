# routes/attendance.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.attendance import Attendance
from datetime import datetime, date, timedelta
from sqlalchemy.exc import SQLAlchemyError
from threading import Lock
from readerClass import ReaderClass

reader = ReaderClass()

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

# Global state for bulk sign-out mode
bulk_sign_out_state = {
    'active': False,
    'last_activity': None,
    'lock': Lock()
}

BULK_SIGN_OUT_TIMEOUT = timedelta(seconds=40)

@attendance_bp.route('/sign-in', methods=['POST'])
def sign_in():
    data = request.get_json()
    card_id, card_name = reader.read()

    if not rfid_card_id:
        return jsonify({'status': 'error', 'message': 'RFID card ID is required'}), 400

    # Find the user with the given RFID card ID
    user = User.query.filter_by(id=card_id).first()

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    # Check if the user has already signed in today
    today = date.today()
    existing_record = Attendance.query.filter_by(user_id=user.id, date=today).first()

    if existing_record:
        return jsonify({'status': 'error', 'message': 'Already signed in today'}), 400

    # Create a new attendance record with sign-in time
    now = datetime.now()
    new_attendance = Attendance(
        date=today,
        sign_in_time=now.time(),
        user_id=user.id
    )

    try:
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'{user.name} signed in successfully'}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Database error occurred'}), 500


### Sign-Out Route ###
@attendance_bp.route('/sign-out', methods=['POST'])
def sign_out():
    data = request.get_json()
    mentor_card_id = reader.read_id()

    if not mentor_rfid_card_id:
        return jsonify({'status': 'error', 'message': 'Mentor RFID card ID is required'}), 400

    # Verify mentor
    mentor = User.query.filter_by(id=mentor_card_id, role='mentor').first()
    if not mentor:
        return jsonify({'status': 'error', 'message': 'Mentor not found or invalid mentor RFID card'}), 404

    card_id, name = reader.read()
    if not user_rfid_card_id:
        return jsonify({'status': 'error', 'message': 'User RFID card ID is required'}), 400

    # Verify user
    user = User.query.filter_by(id=card_id).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    # Proceed to sign out the user
    return process_sign_out(user)


### Bulk Sign-Out Route ###
@attendance_bp.route('/bulk-sign-out', methods=['POST'])
def bulk_sign_out():
    data = request.get_json()
    user_rfid_card_id = data.get('user_rfid_card_id')
    mentor_rfid_card_id = data.get('mentor_rfid_card_id')

    if not user_rfid_card_id:
        return jsonify({'status': 'error', 'message': 'User RFID card ID is required'}), 400

    now = datetime.now()
    with bulk_sign_out_state['lock']:
        # Check if bulk sign-out mode is active and not timed out
        if bulk_sign_out_state['active'] and (now - bulk_sign_out_state['last_activity'] <= BULK_SIGN_OUT_TIMEOUT):
            # Update last activity timestamp
            bulk_sign_out_state['last_activity'] = now
            mentor_verified = True
        else:
            # Need mentor authorization
            if not mentor_rfid_card_id:
                return jsonify({'status': 'error', 'message': 'Mentor RFID card ID is required'}), 400

            # Verify mentor
            mentor = User.query.filter_by(rfid_card_id=mentor_rfid_card_id, role='mentor').first()
            if not mentor:
                return jsonify({'status': 'error', 'message': 'Mentor not found or invalid mentor RFID card'}), 404

            # Activate bulk sign-out mode
            bulk_sign_out_state['active'] = True
            bulk_sign_out_state['last_activity'] = now

    # Verify user
    user = User.query.filter_by(rfid_card_id=user_rfid_card_id).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    # Proceed to sign out the user
    return process_sign_out(user)


### Helper Function to Process Sign-Out ###
def process_sign_out(user):
    today = date.today()
    attendance_record = Attendance.query.filter_by(user_id=user.id, date=today).first()

    if not attendance_record:
        return jsonify({'status': 'error', 'message': 'No sign-in record found for today'}), 400

    if attendance_record.sign_out_time is not None:
        return jsonify({'status': 'error', 'message': 'Already signed out today'}), 400

    # Update sign-out time and calculate hours worked
    now = datetime.now()
    attendance_record.sign_out_time = now.time()
    sign_in_datetime = datetime.combine(today, attendance_record.sign_in_time)
    sign_out_datetime = datetime.combine(today, attendance_record.sign_out_time)

    # Handle cases where sign-out might be after midnight
    if sign_out_datetime < sign_in_datetime:
        sign_out_datetime += timedelta(days=1)

    total_hours = (sign_out_datetime - sign_in_datetime).total_seconds() / 3600.0
    attendance_record.days_hours = round(total_hours, 2)

    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'{user.name} signed out successfully', 'hours_worked': attendance_record.days_hours}), 200
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Database error occurred'}), 500