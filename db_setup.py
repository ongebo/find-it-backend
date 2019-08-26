from app.models.user import db
import sys
import os


def setup_tables():
    if len(sys.argv) == 2 and sys.argv[1] == 'testdb':
        os.environ['DATABASE_URL'] = os.getenv['TEST_DATABASE']
    db.create_all()
