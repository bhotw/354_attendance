# routes/addadminuser.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.adminUser import AdminUser
from flask_jwt_extended import jwt_required, get_jwt_identity

add_admin_user_bp = Blueprint('add_admin_user', __name__, url_prefix='/api/admin')

@add_admin_user_bp.route('/add_admin_user', methods=['POST'])
@jwt_required()
def add_admin_user():
    try:
        token = get_jwt_identity()
        if not token:
            return jsonify({'status': 'error', 'message': 'Invalid token'}), 401

        # Extract data from request
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not username or not email or not password:
            return jsonify({'status': 'error', 'message': 'Missing required fields'}), 400

        # Check if username or email already exists
        existing_user = AdminUser.query.filter((AdminUser.username == username) | (AdminUser.email == email)).first()
        if existing_user:
            return jsonify({'status': 'error', 'message': 'Username or email already exists'}), 400

        # Create new admin user
        new_admin_user = AdminUser(
            username=username,
            email=email
        )
        new_admin_user.set_password(password)

        # Save to database
        db.session.add(new_admin_user)
        db.session.commit()

        return jsonify({'status': 'success', 'message': 'Admin user created successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"Error creating admin user: {e}")
        return jsonify({'status': 'error', 'message': 'Server error'}), 500
