from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import jwt_required
from readerClass import ReaderClass

reader = ReaderClass()
add_card_bp = Blueprint("add_card", __name__, url_prefix="/api/add_card")

@add_card_bp.route("/users", methods=["GET"])
@jwt_required()
def get_user():
    users = User.query.all()
    user_list = [{"id":user.id, "name":user.name} for user in users]
    return jsonify(user_list)

@add_card_bp.route("/add_new_card", methods=["POST"])
@jwt_required()
def add_new_card():
    data = request.get_json()

    user_id = data.get("user_id")
    card_id = reader.read_id()

    user = User.query.filter_by(id=user_id).first()
    user_name = user.name
    print(user_name)
    reader.write(user_name)


    if not user_id or not card_id:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        user = User.query.filter_by(id=user_id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user.card_id = card_id

        db.session.commit()
        reader.destroy()
        return jsonify(
            {"status": "success", "message": f"Card ID {card_id} successfully assigned to user {user.name}"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500