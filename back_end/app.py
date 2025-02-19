# app.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY
from datetime import timedelta
from flask_socketio import SocketIO

from extensions import db

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.registration import team_member_bp
from routes.attendance import attendance_bp
from routes.viewteam import viewteam_bp
from routes.addadminuser import add_admin_user_bp
from routes.view_admin_users import view_admin_user_bp
from routes.add_attendance import add_attendance_bp
from routes.view_attendance import view_attendance_bp
from routes.writereadcard import card_bp
from routes.add_card import add_card_bp

import os
from flask import send_from_directory


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # Set the configuration
app.config['SECRET_KEY'] = SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
socketio = SocketIO(app, cors_allowed_origins="*")

db.init_app(app)


# JWT Configuration
app.config["JWT_SECRET_KEY"] = "i like to eat milk"  # Change this to a secure key
jwt = JWTManager(app)
CORS(app, supports_credentials=True)



# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(add_admin_user_bp, url_prefix="/api/admin")
app.register_blueprint(view_admin_user_bp, url_prefix="/api/admin")
app.register_blueprint(viewteam_bp, url_prefix="/api/team")
app.register_blueprint(add_attendance_bp, url_prefix="/api/manual", endpoint="add_attendance")
app.register_blueprint(view_attendance_bp, url_prefix="/api/view")
app.register_blueprint(team_member_bp, url_prefix="/api")
app.register_blueprint(attendance_bp, url_prefix="/api/attendance")
app.register_blueprint(card_bp, url_prefix="/api/card")
app.register_blueprint(add_card_bp, url_prefix="/api/add_card")



if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    socketio.run(app, host='0.0.0.0', port=5000)
