import os
import secrets

from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URI = os.getenv("DB_URL")
SQLALCHEMY_TRACK_MODIFICATION = False

SECRET_KEY = secrets.token_hex(16)



