# app.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import SQLALCHEMY_DATABASE_URI, SECRET_KEY

from extensions import db

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.registration import team_member_bp
from routes.attendance import attendance_bp
from routes.viewteam import viewteam_bp


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # Set the configuration
app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)
# JWT Configuration
app.config["JWT_SECRET_KEY"] = "i like to eat milk"  # Change this to a secure key
jwt = JWTManager(app)
CORS(app)
# Register Blueprints
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(viewteam_bp, url_prefix="/api/team")
app.register_blueprint(team_member_bp, url_prefix="/api")
app.register_blueprint(attendance_bp, url_prefix="/api/attendance")


if __name__ == "__main__":
    app.run(debug=True)