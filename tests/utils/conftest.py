import os


def pytest_configure(config):
    os.environ['DATABASE_URL'] = os.getenv('TEST_DATABASE')
    print(os.getenv('DATABASE_URL'))
