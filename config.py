import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI" )
SQLALCHEMY_TRACK_MODIFICATION = False

SECRE_KEY = os.getenv('SECRE_KEY')
