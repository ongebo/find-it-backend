import os
import pytest


class Request:
    """A dummy class representing an HTTP request."""

    def __init__(self, body):
        self.body = body

    def get_json(self):
        return self.body if isinstance(self.body, dict) else None


def pytest_configure(config):
    os.environ['FINDIT_PROJECT_MODE'] = 'test_mode'


@pytest.fixture
def redundant_request():
    return Request({
        'username': 'John Doe',
        'phone_number': 'John Doe',
        'email': 'John Doe',
        'password': 'JohnDoe',
        'school': 'not required in request'
    })


@pytest.fixture
def invalid_fields_request():
    return Request({
        'username': '12',
        'phone_number': '076',
        'email': 'John Doe',
        'password': 'JoDoe'
    })
