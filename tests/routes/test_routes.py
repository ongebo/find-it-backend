from app.utils.persister import db, User
from ..test_utils import clean_database
from app import app
import os


def register_and_login_user(test_client, user_data):
    test_client.post('/users', json=user_data)
    response = test_client.post('/login', json={
        'email': user_data['email'],
        'password': user_data['password']
    })
    return response.get_json()['access_token']


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


def test_api_returns_errors_given_invalid_lost_and_found_item_report(test_client, correct_signup_data, invalid_lost_item_report):
    response = test_client.post(
        '/items', json=invalid_lost_item_report, headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )

    assert response.status_code == 400
    assert response.get_json(
    )['errors']['item_name'] == 'Item name should contain atleast 3 characters!'
    assert response.get_json(
    )['errors']['description'] == 'Item description should contain atleast 12 characters!'

    clean_database()


def test_api_returns_registered_info_given_valid_lost_and_found_item_report(test_client, correct_signup_data, valid_lost_item_report):
    response = test_client.post(
        '/items', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )

    assert response.status_code == 201
    assert response.get_json(
    )['item_name'] == valid_lost_item_report['item_name']
    assert response.get_json(
    )['description'] == valid_lost_item_report['description']
    assert response.get_json(
    )['image_url'] == valid_lost_item_report['image_url']
    assert 'id' in response.get_json()

    clean_database()


def test_api_returns_404_when_fetching_all_items_with_non_in_database(test_client, correct_signup_data):
    response = test_client.get(
        '/items', headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )

    assert response.status_code == 404
    assert response.get_json()['error'] == 'No lost and found items!'

    clean_database()


def test_api_returns_lost_and_found_items_in_database(test_client, correct_signup_data, valid_lost_item_report):
    access_token = register_and_login_user(test_client, correct_signup_data)
    test_client.post(
        '/items', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + access_token
        }
    )
    response = test_client.get(
        '/items', headers={
            'Authorization': 'Bearer ' + access_token
        }
    )

    assert response.status_code == 200
    assert response.get_json()['items']

    clean_database()


def test_api_returns_404_when_fetching_specific_item_which_is_non_existent(test_client, correct_signup_data):
    non_existent_id = 0
    response = test_client.get(
        f'/items/{non_existent_id}', headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )

    assert response.status_code == 404
    assert response.get_json()['error'] == f'No item with id {non_existent_id}'

    clean_database()


def test_api_returns_specific_lost_and_found_item_in_database(test_client, correct_signup_data, valid_lost_item_report):
    access_token = register_and_login_user(test_client, correct_signup_data)
    item_id = test_client.post(
        '/items', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + access_token
        }
    ).get_json()['id']
    response = test_client.get(
        f'/items/{item_id}', headers={
            'Authorization': 'Bearer ' + access_token
        }
    )

    assert response.status_code == 200
    assert response.get_json()['id'] == item_id

    clean_database()


def test_api_returns_error_given_unsupported_image_file_upload(test_client, correct_signup_data, invalid_upload_file):
    response = test_client.post(
        '/items/images', data={'image': invalid_upload_file}, headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )
    assert response.status_code == 400
    assert response.get_json(
    )['errors']['image'] == 'Specify a .png, .jpg, or .jpeg file!'

    clean_database()


def test_api_saves_valid_uploaded_file_and_returns_its_url(test_client, correct_signup_data, valid_upload_file):
    response = test_client.post(
        '/items/images', data={'image': valid_upload_file}, headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )
    assert response.status_code == 201
    assert response.get_json()['image_url']

    clean_database()
    # remove uploaded file
    os.remove(os.path.join(
        app.config['UPLOAD_FOLDER'],
        valid_upload_file[1]
    ))


def test_api_returns_413_given_large_image_file(test_client, correct_signup_data, large_upload_file):
    response = test_client.post(
        '/items/images', data={'image': large_upload_file}, headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )
    assert response.status_code == 413
    assert response.get_json()['error'] == 'Image larger than 5 megabytes!'
    clean_database()


def test_api_returns_404_when_fetching_non_existent_url(test_client):
    response = test_client.get('/undefined/url/')
    assert response.status_code == 404
    assert response.get_json(
    )['error'] == 'The requested resource does not exist!'
