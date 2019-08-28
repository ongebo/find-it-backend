import sys
import os


def setup_tables():
    if len(sys.argv) == 2 and sys.argv[1] == 'testdb':
        print('Setting up test database...')
        os.environ['FINDIT_PROJECT_MODE'] = 'test_mode'

    # import db only after setting os.environ['FINDIT_PROJECT_MODE'] above
    from app.models import db
    db.create_all()


if __name__ == "__main__":
    setup_tables()
