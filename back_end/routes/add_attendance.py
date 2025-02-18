from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from models.attendance import Attendance
from datetime import datetime
from flask_jwt_extended import jwt_required

add_attendance_bp = Blueprint("add_attendance", __name__, url_prefix="/api/manual")

# Fetch all users for the dropdown
@add_attendance_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "name": user.name} for user in users]
    return jsonify(user_list)

# Add attendance
@add_attendance_bp.route("/add_attendance", methods=["POST"], endpoint="add_attendance" )
@jwt_required()
def add_attendance():
    data = request.get_json()

    user_id = data.get("user_id")
    date_str = data.get("date")
    sign_in_time = data.get("sign_in_time")
    sign_out_time = data.get("sign_out_time")

    if not user_id or not date_str or not sign_in_time or not sign_out_time:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Convert date and time values
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        sign_in_time = datetime.strptime(sign_in_time, "%H:%M").time()
        sign_out_time = datetime.strptime(sign_out_time, "%H:%M").time()

        # Calculate total hours without combining date and time
        sign_in_seconds = sign_in_time.hour * 3600 + sign_in_time.minute * 60
        sign_out_seconds = sign_out_time.hour * 3600 + sign_out_time.minute * 60

        days_hours = round((sign_out_seconds - sign_in_seconds) / 3600, 2)  # Convert to hours

        # Check if attendance record already exists for the user on that date
        existing_record = Attendance.query.filter_by(user_id=user_id, date=date).first()

        if existing_record:
            return jsonify({"message": "Attendance record already exists for this date. If you want to make changes, please update it in the attendance view."}), 400

        # Add new attendance record if no existing record found
        new_attendance = Attendance(
            user_id=user_id,
            date=date,
            sign_in_time=sign_in_time,
            sign_out_time=sign_out_time,
            days_hours=days_hours,
        )

        db.session.add(new_attendance)
        db.session.commit()

        return jsonify({"message": "Attendance added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500