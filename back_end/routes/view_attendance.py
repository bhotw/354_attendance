from flask import Blueprint, request, jsonify
from models.attendance import Attendance
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required
from datetime import datetime

view_attendance_bp = Blueprint("view_attendance", __name__, url_prefix="/api/view")


@view_attendance_bp.route("/view_attendance", methods=["GET"])
@jwt_required()
def get_attendance():
    attendance_records = Attendance.query.all()
    attendance_list = [
        {
            "id": record.id,
            "user_id": record.user_id,
            "user_name": User.query.get(record.user_id).name,  # Fetch user name
            "date": record.date.strftime("%Y-%m-%d"),
            "sign_in_time": record.sign_in_time.strftime("%H:%M") if record.sign_in_time else None,
            "sign_out_time": record.sign_out_time.strftime("%H:%M") if record.sign_out_time else None,
            "days_hours": record.days_hours,
        }
        for record in attendance_records
    ]
    return jsonify(attendance_list), 200


@view_attendance_bp.route("/view_attendance/<int:id>", methods=["PUT"])
@jwt_required()
def update_attendance(id):
    data = request.json
    attendance = Attendance.query.get(id)

    sign_in_time = attendance.sign_in_time
    sign_out_time = attendance.sign_out_time

    if not attendance:
        return jsonify({"error": "Attendance record not found"}), 404

    if "sign_in_time" in data:
        sign_in_time = data["sign_in_time"]
    if "sign_out_time" in data:
        sign_out_time = data["sign_out_time"]
    
    sign_in_time = datetime.strptime(sign_in_time, "%H:%M").time()
    sign_out_time = datetime.strptime(sign_out_time, "%H:%M").time()

    # Calculate total hours without combining date and time
    sign_in_seconds = sign_in_time.hour * 3600 + sign_in_time.minute * 60
    sign_out_seconds = sign_out_time.hour * 3600 + sign_out_time.minute * 60

    days_hours = round((sign_out_seconds - sign_in_seconds) / 3600, 2)

    attendance.sign_in_time = sign_in_time
    attendance.sign_out_time = sign_out_time
    attendance.days_hours = days_hours

    db.session.commit()
    return jsonify({"message": "Attendance updated successfully"}), 200
