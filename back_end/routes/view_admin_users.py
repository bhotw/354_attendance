from flask import Blueprint, jsonify
from models.adminUser import AdminUser
from flask_jwt_extended import jwt_required

view_admin_user_bp = Blueprint('view_admin_user', __name__, url_prefix='/api/admin')

@view_admin_user_bp.route('/view_admin_users', methods=['GET'])
@jwt_required()  # Ensure only authorized users can access
def get_admin_users():
    try:
        # Query all admin users
        admin_users = AdminUser.query.all()

        # Format the admin users data
        admin_users_data = []
        for admin in admin_users:
            admin_users_data.append({
                'id': admin.id,
                'username': admin.username,
                'email': admin.email
            })

        return jsonify({'status': 'success', 'admin_users': admin_users_data}), 200

    except Exception as e:
        print(f"Unexpected error in get_admin_users: {e}")
        return jsonify({'status': 'error', 'message': 'Server error'}), 500
