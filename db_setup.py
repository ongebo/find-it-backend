import sys
import os


def setup_tables():
    if len(sys.argv) == 2 and sys.argv[1] == 'testdb':
        print('Setting up test database...')
        os.environ['DATABASE_URL'] = os.getenv('TEST_DATABASE', '')

    # import db only after setting os.environ['DATABASE_URL'] above
    from app.models.user import db
    db.create_all()


if __name__ == "__main__":
    setup_tables()
