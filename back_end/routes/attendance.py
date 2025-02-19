# routes/attendance.py
from flask import Blueprint, request, jsonify, session
from extensions import db
from models.user import User
from models.attendance import Attendance
from datetime import datetime, date, timedelta
from sqlalchemy.exc import SQLAlchemyError
from threading import Lock
from readerClass import ReaderClass
from flask_socketio import emit
from flask import current_app
from extensions import socketio


reader = ReaderClass()

attendance_bp = Blueprint('attendance', __name__, url_prefix='/api/attendance')

# Global state for bulk sign-out mode
bulk_sign_out_state = {
    'active': False,
    'last_activity': None,
    'lock': Lock()
}

BULK_SIGN_OUT_TIMEOUT = timedelta(seconds=60)

@attendance_bp.route('/sign-in', methods=['POST'])
def sign_in():

    card_id = reader.read_only_id()
    reader.destroy()

    if not card_id:
        return jsonify({'status': 'error', 'message': 'RFID card ID is required'}), 400

    # Find the user with the given RFID card ID
    user = User.query.filter_by(card_id=card_id).first()

    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    # Check if the user has already signed in today
    today = date.today()
    existing_record = Attendance.query.filter_by(user_id=user.id, date=today).first()

    if existing_record:
        return jsonify({'status': 'Message', 'message': 'Already signed in today'}), 400

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
        reader.destroy()
        return jsonify({'status': 'success', 'message': f'{user.name} signed in successfully'}), 200
    except SQLAlchemyError:
        db.session.rollback()
        reader.destroy()
        return jsonify({'status': 'error', 'message': 'Database error occurred'}), 500


@attendance_bp.route('/mentor-auth', methods=['POST'])
def mentor_auth():
    mentor_card_id = reader.read_only_id()
    reader.destroy()

    if not mentor_card_id:
        return jsonify({'status': 'error', 'message': 'Mentor RFID card ID is required'}), 400
    mentor = User.query.filter_by(card_id=mentor_card_id, role='mentor').first()
    if not mentor:
        return jsonify({'status': 'error', 'message': 'Not a Mentor !!!'}), 404

    session['mentor_authenticated'] = True

    return jsonify({'status': 'success', 'message': 'Mentor authenticated. Student can now sign out.'})


### Sign-Out Route ###
@attendance_bp.route('/sign-out', methods=['POST'])
def sign_out():
    # print(f"Session: {session}")
    # if not session.get('mentor_authenticated'):
    #     return jsonify({'status': 'error', 'message': 'Mentor authentication required before signing out'}), 403

    card_id = reader.read_only_id()
    reader.destroy()

    if not card_id:
        return jsonify({'status': 'error', 'message': 'User RFID card ID is required'}), 400

    # Verify user
    user = User.query.filter_by(card_id=card_id).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 404

    # Proceed to sign out the user
    return process_sign_out(user)

@attendance_bp.route('/bulk-sign-out', methods=['POST'])
def bulk_sign_out():
    now = datetime.now()
    with bulk_sign_out_state['lock']:
        if bulk_sign_out_state['active'] and (now - bulk_sign_out_state['last_activity'] <= BULK_SIGN_OUT_TIMEOUT):
            bulk_sign_out_state['last_activity'] = now
        else:
            bulk_sign_out_state['active'] = True
            bulk_sign_out_state['last_activity'] = datetime.now()


            while bulk_sign_out_state['active']:
                user_card_id = reader.read_only_id(timeout=20)
                reader.destroy()

                if not user_card_id:
                    break

                user = User.query.filter_by(card_id=user_card_id).first()
                if not user:
                    emit('sign_out_error', {'status': 'error', 'message': 'User not found'})
                    continue

                response, status_code = process_sign_out(user)  # Process the sign-out
                if status_code == 200:
                    socketio.emit('bulk_sign_out_update', {'status': 'success', 'user': user.name, 'message': f'{user.name} signed out successfully'})
                elif status_code == 400:
                    socketio.emit('bulk_sign_out_update', {'status': 'failure', 'user': user.name, 'message': f'{response["message"]}'})
                else:
                    socketio.emit('bulk_sign_out_error', {'status': 'error', 'message': response.json['message']})

            bulk_sign_out_state['active'] = False
            socketio.emit('bulk_sign_out_complete', {'status': 'success', 'message': 'Bulk sign-out session closed.'})

    return jsonify({'status': 'success', 'message': 'Bulk Sign-Out is Done!'}), 200


### Helper Function to Process Sign-Out ###
def process_sign_out(user):
    today = date.today()
    attendance_record = Attendance.query.filter_by(user_id=user.id, date=today).first()

    if not attendance_record:
        return jsonify({'status': 'error', 'message': 'No sign-in record found for today'}), 400

    if attendance_record.sign_out_time is not None:
        print("Already Singed out today.")
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

@attendance_bp.route('/status', methods=['GET'])
def check_status():
    user_card_id = reader.read_only_id()
    reader.destroy()

    if not user_card_id:
        return jsonify({'status': 'error', 'message': 'RFID card is required'}), 400

    user = User.query.filter_by(card_id=user_card_id).first()
    if not user:
        return jsonify({'status': 'error', 'message': 'User not found'}), 400

    today = datetime.now().date()
    sign_in_record = Attendance.query.filter_by(user_id=user.id, date=today).first()

    if sign_in_record:
        return jsonify({
            'status': 'success',
            'message': f"{user.name} signed in at {sign_in_record.sign_in_time.strftime('%I:%M %p')}"
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f"{user.name}, you have not signed in today. Speak to a mentor for correct sign-in."
        })

@attendance_bp.route("/clear", methods=["POST"])
def clear():
    reader.destroy()
    return jsonify({'status': 'success', 'message': "Reader is clean now."}), 200