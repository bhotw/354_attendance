# models/admin_user.py
from extensions import db

class AdminUser(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # Store hashed passwords
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<AdminUser {self.username}>'