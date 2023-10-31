import os

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI" )
SQLALCHEMY_TRACK_MODIFICATION = False

SECRE_KEY = "this is a secreate and i will keep that way"



