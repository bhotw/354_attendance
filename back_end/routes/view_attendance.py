from flask import Blueprint, request, jsonify
from models.attendance import Attendance
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required

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

    if not attendance:
        return jsonify({"error": "Attendance record not found"}), 404

    if "sign_in_time" in data:
        attendance.sign_in_time = data["sign_in_time"]
    if "sign_out_time" in data:
        attendance.sign_out_time = data["sign_out_time"]

    db.session.commit()
    return jsonify({"message": "Attendance updated successfully"}), 200
