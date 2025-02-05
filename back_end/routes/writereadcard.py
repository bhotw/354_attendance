from flask import Blueprint, request, jsonify
from readerClass import ReaderClass
from extensions import db
from models.user import User
from flask_jwt_extended import jwt_required

card_bp = Blueprint("card", __name__, url_prefix="/api/card")

reader = ReaderClass()


@card_bp.route("/write", methods=["POST"])
@jwt_required()
def write_card():
    try:
        data = request.get_json()
        name = data.get("name")

        if not name:
            return jsonify({"status": "error", "message": "Name is required"}), 400

        card_id, card_name = reader.write(name)
        reader.destroy()

        if card_id and card_name:
            return jsonify({"status": "success", "card_id": card_id, "card_name": card_name}), 200
        else:
            return jsonify({"status": "error", "message": message}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@card_bp.route("/read", methods=["GET"])
@jwt_required()
def read_card():
    try:
        card_id, card_name = reader.read()
        reader.destroy()

        if not card_id:
            return jsonify({"status": "error", "message": ""}), 400
        if not card_name:
            return jsonify({"status": "error", "message": "Name is required"}), 400
        if card_id and card_name:
            return jsonify({"status": "success", "card_id": card_id, "name": card_name})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@card_bp.route("/read_user", methods=["GET"])
@jwt_required()
def read_user():
    try:
        card_id = reader.read_id()
        reader.destroy()
        if not card_id:
            return jsonify({"status": "error", "message": "Need a valid card id."}), 400
        user = User.query.filter_by(card_id=card_id).first()

        if not user:
            return jsonify({"status": "error", "message": "Card is not in our team."}), 400
        print(user.id)

        user_data = {
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

        return jsonify({"status": "success", "team_members": user_data}), 200

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500
