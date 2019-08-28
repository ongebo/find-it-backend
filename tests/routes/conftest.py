import pytest
from app.routes.routes import app


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
def test_client():
    return app.test_client()
