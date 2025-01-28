# routes/auth.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')  # Adjust depending on your login field
    password = data.get('password')  # Assuming you have password fields (not shown in User model)

    # For demonstration, let's assume any user with role 'admin' can log in
    user = User.query.filter_by(name=username, role='admin').first()

    if user:
        # In a real application, verify the password
        access_token = create_access_token(identity=user.id)
        return jsonify({'status': 'success', 'token': access_token}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid credentials'}), 401