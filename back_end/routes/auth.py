# routes/auth.py
from flask import Blueprint, request, jsonify
from extensions import db
from models.adminUser import AdminUser
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# routes/auth.py
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

    # Query the AdminUser table for the provided username
    admin_user = AdminUser.query.filter_by(username=username).first()

    if admin_user and admin_user.check_password(password):
        # Password is correct; proceed to generate token
        access_token = create_access_token(identity=str(admin_user.id))


        return jsonify({
            'status': 'success',
            'message': 'Authentication successful',
            'token_type': 'Bearer',
            'token': access_token,
            'user': {
                'id': admin_user.id,
                'username': admin_user.username
            }
        }), 200
    else:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Get the unique identifier for the JWT
    revoked_tokens.add(jti)  # Store it in a blacklist
    return jsonify({'status': 'success', 'message': 'Successfully logged out'}), 200

    # Optional: Middleware to block blacklisted tokens

