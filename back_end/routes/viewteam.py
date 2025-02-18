from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from extensions import db
from models.user import User

viewteam_bp = Blueprint("viewteam", __name__, url_prefix='/api/team')

# Get all team members
@viewteam_bp.route("/viewteam", methods=["GET"])
@jwt_required()
def get_team_members():
    try:
        team_members = User.query.all()
        team_list = [
            {
                "id": user.id,
                "card_id": user.card_id,
                "name": user.name,
                "role": user.role,
                "email": user.email,
                "phone_number": user.phone_number,
                "emergency_contact_name": user.emergency_contact_name,
                "emergency_contact_phone": user.emergency_contact_phone,
                "parents_email": user.parents_email,
            }
            for user in team_members
        ]
        return jsonify({"status": "success", "team_members": team_list}), 200
    except Exception as e:
        print(f"Error fetching team members: {e}")
        return jsonify({"status": "error", "message": "Failed to retrieve team members"}), 500


# Update team member details
@viewteam_bp.route("/viewteam/<int:user_id>", methods=["PUT"])
@jwt_required()
def update_team_member(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        data = request.get_json()

        # Update only provided fields
        user.card_id = data.get("card_id", user.card_id)
        user.name = data.get("name", user.name)
        user.role = data.get("role", user.role)
        user.email = data.get("email", user.email)
        user.phone_number = data.get("phone_number", user.phone_number)
        user.emergency_contact_name = data.get("emergency_contact_name", user.emergency_contact_name)
        user.emergency_contact_phone = data.get("emergency_contact_phone", user.emergency_contact_phone)
        user.parents_email = data.get("parents_email", user.parents_email)

        db.session.flush()
        db.session.commit()

        return jsonify({"status": "success", "message": "User updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        print(f"Error updating user: {e}")
        return jsonify({"status": "error", "message": "Failed to update user"}), 500
