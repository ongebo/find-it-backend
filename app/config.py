import os
import datetime

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# change to test database url in test mode
if os.getenv('FINDIT_PROJECT_MODE') == 'test_mode':
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')

SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

# authentication tokens should expire after 30 days
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
JWT_ACCESS_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)

# image upload settings
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
MAX_CONTENT_LENGTH = 6 * 1024 * 1024
