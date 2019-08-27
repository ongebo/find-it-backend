import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# change to test database url in test mode
if os.getenv('FINDIT_PROJECT_MODE') == 'test_mode':
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')

SQLALCHEMY_TRACK_MODIFICATIONS = False
