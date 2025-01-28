# routes/team_member.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity

team_member_bp = Blueprint('team_member', __name__, url_prefix='/api')

@team_member_bp.route('/register-team-member', methods=['POST'])
@jwt_required()
def register_team_member():
    # Get the ID of the admin from the JWT
    admin_id = get_jwt_identity()

    # Fetch the admin user from the database
    admin_user = User.query.get(admin_id)

    # Check if the user is an admin
    if not admin_user or admin_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403

    data = request.get_json()

    # Extract and validate data
    name = data.get('name')
    role = data.get('role')
    email = data.get('email')
    phone_number = data.get('phone_number')
    emergency_contact_name = data.get('emergency_contact_name')
    emergency_contact_phone = data.get('emergency_contact_phone')
    parents_email = data.get('parents_email')

    # Perform server-side validation (you can enhance this)
    if not name or not role or not email or not phone_number:
        return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

    # Check if the email already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'status': 'error', 'message': 'Email already registered'}), 400

    # Create a new User object
    new_user = User(
        name=name,
        role=role,
        email=email,
        phone_number=phone_number,
        emergency_contact_name=emergency_contact_name,
        emergency_contact_phone=emergency_contact_phone,
        parents_email=parents_email
    )

    try:
        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Team member registered successfully'}), 201
    except Exception as e:
        # Handle any errors
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Failed to register team member'}), 500