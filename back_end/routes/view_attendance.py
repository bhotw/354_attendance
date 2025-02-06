from flask import Blueprint, request, jsonify
from models.attendance import Attendance
from models.user import User
from extensions import db
from flask_jwt_extended import jwt_required
from datetime import datetime, timedelta

view_attendance_bp = Blueprint("view_attendance", __name__, url_prefix="/api/view")


@view_attendance_bp.route("/view_attendance", methods=["GET"])
@jwt_required()
def get_attendance():
    attendance_records = (
        db.session.query(
            Attendance.id,
            Attendance.user_id,
            User.name.label("user_name"),
            Attendance.date,
            Attendance.sign_in_time,
            Attendance.sign_out_time,
            Attendance.days_hours,
        )
        .join(User, Attendance.user_id == User.id)
        .all()
    )

    attendance_list = [
        {
            "id": record.id,
            "user_id": record.user_id,
            "user_name": record.user_name,
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

    sign_in_time = attendance.sign_in_time
    sign_out_time = attendance.sign_out_time

    if "sign_in_time" in data:
        try:
            sign_in_time = datetime.strptime(data["sign_in_time"], "%H:%M").time()
        except ValueError:
            return jsonify({"error": "Invalid sign-in time format"}), 400

    if "sign_out_time" in data:
        try:
            sign_out_time = datetime.strptime(data["sign_out_time"], "%H:%M").time()
        except ValueError:
            return jsonify({"error": "Invalid sign-out time format"}), 400

    # Ensure both times exist before calculating hours
    if sign_in_time and sign_out_time:
        sign_in_dt = datetime.combine(attendance.date, sign_in_time)
        sign_out_dt = datetime.combine(attendance.date, sign_out_time)

        if sign_out_dt < sign_in_dt:
            return jsonify({"error": "Sign-out time cannot be before sign-in time"}), 400

        # Calculate total hours as a float rounded to 2 decimal places
        days_hours = round((sign_out_dt - sign_in_dt) / timedelta(hours=1), 2)
    else:
        days_hours = None  # Don't update if one value is missing

    # Update values in the database
    attendance.sign_in_time = sign_in_time
    attendance.sign_out_time = sign_out_time
    attendance.days_hours = days_hours

    db.session.commit()
    return jsonify({"message": "Attendance updated successfully"}), 200


@view_attendance_bp.route("/user_attendance/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user_attendance(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    attendance_records = Attendance.query.filter_by(user_id=user_id).all()

    attendance_list = [
        {
            "id": record.id,
            "user_id": record.user_id,
            "user_name": user.name,
            "date": record.date.strftime("%Y-%m-%d"),
            "sign_in_time": record.sign_in_time.strftime("%H:%M") if record.sign_in_time else None,
            "sign_out_time": record.sign_out_time.strftime("%H:%M") if record.sign_out_time else None,
            "days_hours": record.days_hours,
        }
        for record in attendance_records
    ]

    return jsonify(attendance_list), 200


@view_attendance_bp.route("/user_attendance/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_user_attendance(user_id):
    data = request.json

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    attendance = Attendance.query.filter_by(user_id=user_id, date=data.get("date")).first()

    if not attendance:
        return jsonify({"error": "Attendance record for the specified date not found"}), 404

    sign_in_time = attendance.sign_in_time
    sign_out_time = attendance.sign_out_time

    if "sign_in_time" in data:
        try:
            sign_in_time = datetime.strptime(data["sign_in_time"], "%H:%M").time()
        except ValueError:
            return jsonify({"error": "Invalid sign-in time format"}), 400

    if "sign_out_time" in data:
        try:
            sign_out_time = datetime.strptime(data["sign_out_time"], "%H:%M").time()
        except ValueError:
            return jsonify({"error": "Invalid sign-out time format"}), 400

    # Ensure both times exist before calculating hours
    if sign_in_time and sign_out_time:
        sign_in_dt = datetime.combine(attendance.date, sign_in_time)
        sign_out_dt = datetime.combine(attendance.date, sign_out_time)

        if sign_out_dt < sign_in_dt:
            return jsonify({"error": "Sign-out time cannot be before sign-in time"}), 400

        # Calculate total hours as a float rounded to 2 decimal places
        days_hours = round((sign_out_dt - sign_in_dt) / timedelta(hours=1), 2)
    else:
        days_hours = None  # Don't update if one value is missing

    # Update values in the database
    attendance.sign_in_time = sign_in_time
    attendance.sign_out_time = sign_out_time
    attendance.days_hours = days_hours

    db.session.commit()

    return jsonify({"message": "User attendance updated successfully"}), 200


@view_attendance_bp.route("/view_attendance/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_attendance(id):
    # Find the attendance record by ID
    attendance = Attendance.query.get(id)
    if not attendance:
        return jsonify({"error": "Attendance record not found"}), 404

    # Delete the attendance record
    db.session.delete(attendance)
    db.session.commit()

    return jsonify({"message": "Attendance record deleted successfully"}), 200


