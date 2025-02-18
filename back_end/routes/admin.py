from flask import Blueprint, request, jsonify
import jwt
from datetime import datetime
from extensions import db
from models.attendance import Attendance
from models.user import User
from flask_jwt_extended import jwt_required
from .auth import login

admin_bp = Blueprint('admin', __name__, url_prefix="/api/admin")

@admin_bp.route("/")
def admin_home():
    return login()

# Middleware to authenticate token
# def authenticate_token(func):
#     def wrapper(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({"message": "Access denied"}), 401
#
#         try:
#             decoded = jwt.decode(token, 'your-secret-key', algorithms=["HS256"])
#             request.user_id = decoded['user_id']
#         except jwt.ExpiredSignatureError:
#             return jsonify({"message": "Token has expired"}), 403
#         except jwt.InvalidTokenError:
#             return jsonify({"message": "Invalid token"}), 403
#
#         return func(*args, **kwargs)
#
#     wrapper.__name__ = func.__name__
#     return wrapper

@admin_bp.route('/viewattendance', methods=['GET'])
@jwt_required()
def view_attendance():
    user_id = request.user_id
    attendances = Attendance.query.filter_by(user_id=user_id).all()

    attendance_list = []
    for attendance in attendances:
        attendance_list.append({
            "id": attendance.id,
            "date": attendance.date.isoformat(),
            "sign_in_time": attendance.sign_in_time.isoformat() if attendance.sign_in_time else None,
            "sign_out_time": attendance.sign_out_time.isoformat() if attendance.sign_out_time else None,
            "days_hours": attendance.days_hours
        })

    return jsonify(attendance_list)

@admin_bp.route('/mark-attendance', methods=['POST'])
@jwt_required()
def mark_attendance():
    user_id = request.user_id
    data = request.get_json()
    date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
    sign_in_time = datetime.strptime(data.get('sign_in_time'), '%H:%M:%S').time() if data.get('sign_in_time') else None
    sign_out_time = datetime.strptime(data.get('sign_out_time'), '%H:%M:%S').time() if data.get('sign_out_time') else None
    days_hours = data.get('days_hours')

    new_attendance = Attendance(
        user_id=user_id,
        date=date,
        sign_in_time=sign_in_time,
        sign_out_time=sign_out_time,
        days_hours=days_hours
    )
    db.session.add(new_attendance)
    db.session.commit()

    return jsonify({"message": "Attendance marked successfully"}), 201