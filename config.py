import os

DB_USERNAME = ''
DB_PASSWORD = ''
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = '354_attendance'

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

SQLALCHEMY_TRACK_MODIFICATION = False

SECRE_KEY = 'This_is_a_secret_key'
