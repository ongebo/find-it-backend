from app.utils.persister import db, User
from ..test_utils import clean_database


def test_api_returns_error_given_incorrect_signup_data(test_client, invalid_signup_data):
    response = test_client.post('/users', json=invalid_signup_data)
    assert response.status_code == 400
    assert 'errors' in response.get_json()


def test_api_returns_signup_info_given_correct_signup_data(test_client, correct_signup_data):
    response = test_client.post('/users', json=correct_signup_data)
    assert response.status_code == 201
    response_body = response.get_json()
    assert correct_signup_data['username'] == response_body['username']
    assert correct_signup_data['email'] == response_body['email']
    assert correct_signup_data['phone_number'] == response_body['phone_number']
    assert response_body['id']

    clean_database()


def test_api_returns_error_given_wrong_login_information(test_client, invalid_login_data):
    response = test_client.post('/login', json=invalid_login_data)
    assert response.status_code == 400
    assert 'errors' in response.get_json()


def test_api_returns_tokens_given_correct_login_information(test_client, correct_signup_data):
    test_client.post('/users', json=correct_signup_data)
    login_data = {
        'email': correct_signup_data['email'],
        'password': correct_signup_data['password']
    }
    response = test_client.post('/login', json=login_data)

    assert response.status_code == 200
    assert 'access_token' in response.get_json()
    assert 'refresh_token' in response.get_json()

    clean_database()
