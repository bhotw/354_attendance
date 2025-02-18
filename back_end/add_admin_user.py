# scripts/add_admin_user.py
from extensions import db
# from models.admin_user import AdminUser
from models.adminUser import AdminUser
from app import app  # Adjust the import based on your application structure

with app.app_context():
    username = input("Enter admin username: ")
    email = input("Enter admin email:")
    password = input("Enter admin password: ")

    print(username, email, password)

    if AdminUser.query.filter_by(username=username).first():
        print("Username already exists.")
    else:
        new_admin = AdminUser(username=username, email=email)
        new_admin.set_password(password)
        db.session.add(new_admin)
        db.session.commit()
        print("Admin user created successfully.")