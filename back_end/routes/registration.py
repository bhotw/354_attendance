# routes/team_member.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.adminUser import AdminUser
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from readerClass import ReaderClass
import random

reader = ReaderClass()

team_member_bp = Blueprint('team_member', __name__, url_prefix='/api')


@team_member_bp.route('/register_team_member', methods=['POST'])
@jwt_required()
def register_team_member():
    try:
        token = get_jwt_identity()
        if not token:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401
        admin_user = AdminUser.query.get(token)
        if not admin_user:
            return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

        data = request.get_json()

        # Extract and validate data
        name = data.get('name')
        role = data.get('role')
        email = str(data.get('email'))
        phone_number = str(data.get('phone_number'))
        emergency_contact_name = data.get('emergency_contact_name')
        emergency_contact_phone = str(data.get('emergency_contact_phone'))
        parents_email = str(data.get('parents_email'))

        # Perform server-side validation
        if not name or not role or not email or not phone_number:
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        allowed_roles = {'student', 'mentor'}
        if role not in allowed_roles:
            return jsonify({'status': 'error', 'message': 'Invalid role'}), 400

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'status': 'error', 'message': 'Email already registered'}), 400

        reader.write_name(name)
        new_card_id = reader.read_only_id()
        print("new_card_id: ", new_card_id)
        existing_card = User.query.filter_by(card_id=new_card_id).first()

        if existing_card:
            print('Card id already registered')
            return jsonify({'status': 'card', 'message': 'Card id already registered. Submit again and try a new card.'}), 201

        # Create a new User object
        new_user = User(
            card_id=new_card_id,
            name=name,
            role=role,
            email=email,
            phone_number=phone_number,
            emergency_contact_name=emergency_contact_name,
            emergency_contact_phone=emergency_contact_phone,
            parents_email=parents_email
        )

        # Commit to the database
        db.session.add(new_user)
        db.session.commit()
        reader.destroy()
        return jsonify({'status': 'success', 'message': 'Team member registered successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Unexpected error in register_team_member: {e}")
        return jsonify({'status': 'error', 'message': 'Server error'}), 500



