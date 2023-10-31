import os
import secrets

SQLALCHEMY_DATABASE_URI = "postgresql://pitest:pi_test@localhost/attendance_test"
SQLALCHEMY_TRACK_MODIFICATION = False

SECRET_KEY = secrets.token_hex(16)



