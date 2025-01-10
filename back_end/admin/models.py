from back_end.database import db
from werkzeug.security import generate_password_hash

class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    @staticmethod
    def create_admin(email, password):
        hashed_password = generate_password_hash(password)
        admin = AdminUser(email=email, password=hashed_password)
        db.session.add(admin)
        db.session.commit()
