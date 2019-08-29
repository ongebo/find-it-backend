import pytest
import io
from app.routes.routes import app


@pytest.fixture
def test_client():
    return app.test_client()


@pytest.fixture
def invalid_signup_data():
    return {
        'username': 1234,
        'password': 'this is a very long password beyond 12 characters'
    }


@pytest.fixture
def correct_signup_data():
    return {
        'username': 'Ragnar Lothbrok',
        'phone_number': '+61-659-283021',
        'email': 'pirate@vikings.kat',
        'password': 'V1kingKing'
    }


@pytest.fixture
def invalid_login_data():
    return {
        'email': 22222,
        'password': ''
    }


@pytest.fixture
def invalid_lost_item_report():
    return {
        'item_name': '',
        'description': '22',
        'image_url': ''
    }


@pytest.fixture
def valid_lost_item_report():
    return {
        'item_name': 'Laptop',
        'description': 'Found unattended in the lecture room.',
        'image_url': 'http://hostname.domain/unattended-laptop.jpg'
    }


@pytest.fixture
def invalid_upload_file():
    return (io.BytesIO(b'binary-file-content'), 'lost-and-found.mp4')


@pytest.fixture
def valid_upload_file():
    return (io.BytesIO(b'binary-file-content'), 'lost-and-found.png')
