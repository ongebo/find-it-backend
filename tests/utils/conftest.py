import os
import pytest


class Request:
    """A dummy class representing an HTTP request."""

    def __init__(self, body):
        self.body = body
        self.files = {}

    def get_json(self):
        return self.body if isinstance(self.body, dict) else None


class File:
    """A dummy class representing a file in an HTTP request."""

    def __init__(self, filename):
        self.filename = filename


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
def invalid_signup_data():
    return Request({
        'username': '12',
        'phone_number': '076',
        'email': 'John Doe',
        'password': 'JoDoe'
    })


@pytest.fixture
def valid_signup_data():
    return Request({
        'username': 'Tony Stark',
        'phone_number': '+1-456-209194',
        'email': 'tony.stark@avengers.marvel',
        'password': 'IronM4n'
    })


@pytest.fixture
def invalid_item_data():
    # invalid lost and found item request, item_name should contain atleast
    # 3 characters and description atleast 12 characters
    return Request({
        'item_name': '1',
        'description': '< 12',
        'image_url': '',
    })


@pytest.fixture
def valid_item_data():
    return Request({
        'item_name': 'iPhone X',
        'description': 'I found this phone misplaced at the cafeteria.',
        'image_url': 'http://somehost.com/some-image.png',
    })


@pytest.fixture
def request_without_image():
    return Request(None)


@pytest.fixture
def unsupported_image_format_request():
    request = Request(None)
    request.files = {
        'image': File('lost_and_found_item.mp4')
    }
    return request
