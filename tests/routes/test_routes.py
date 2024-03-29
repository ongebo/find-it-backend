from app.utils.persister import db, User
from ..test_utils import clean_database
from app import app
import os


def register_and_login_user(test_client, user_data, refresh=False):
    test_client.post('/users', json=user_data)
    response = test_client.post('/login', json={
        'email': user_data['email'],
        'password': user_data['password']
    })
    access_token = response.get_json()['access_token']
    refresh_token = response.get_json()['refresh_token']
    return refresh_token if refresh else access_token


def remove_test_data(username, filename):
    clean_database()
    os.remove(os.path.join(
        app.config['UPLOAD_FOLDER'],
        username,
        filename
    ))
    os.rmdir(os.path.join(
        app.config['UPLOAD_FOLDER'],
        username
    ))


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


def test_signup_endpoint_cannot_register_same_user_twice(test_client, correct_signup_data):
    test_client.post('/users', json=correct_signup_data)
    response = test_client.post('/users', json=correct_signup_data)
    assert response.status_code == 400
    assert response.get_json(
    )['errors']['username'] == f'{correct_signup_data["username"]} already exists!'
    assert response.get_json(
    )['errors']['phone_number'] == f'{correct_signup_data["phone_number"]} is already taken by another user!'
    assert response.get_json(
    )['errors']['email'] == f'{correct_signup_data["email"]} is already taken by another user!'
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


def test_refresh_endpoint_returns_new_access_token(test_client, correct_signup_data):
    refresh_token = register_and_login_user(
        test_client, correct_signup_data, refresh=True
    )
    response = test_client.post(
        '/refresh', headers={
            'Authorization': 'Bearer ' + refresh_token
        }
    )
    assert response.status_code == 200
    assert 'access_token' in response.get_json()
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


def test_api_returns_errors_given_invalid_item_update_body(test_client, correct_signup_data, invalid_lost_item_report):
    response = test_client.put(
        '/items/1', json=invalid_lost_item_report, headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )
    assert response.status_code == 400
    assert response.get_json()['errors']
    clean_database()


def test_api_returns_404_when_updating_non_existent_item(test_client, correct_signup_data, valid_lost_item_report):
    response = test_client.put(
        '/items/0', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )
    assert response.status_code == 404
    assert response.get_json()['error'] == 'No item with id 0'
    clean_database()


def test_api_returns_403_when_updating_item_reported_by_another_user(test_client, correct_signup_data, valid_lost_item_report):
    access_token_1 = register_and_login_user(test_client, correct_signup_data)
    access_token_2 = register_and_login_user(
        test_client, {
            'username': 'Bjorn Ironside',
            'phone_number': '+61-859-283021',
            'email': 'lothbrokson@vikings.kat',
            'password': 'V1kingKing'
        }
    )
    item_id = test_client.post(
        '/items', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + access_token_1
        }
    ).get_json()['id']
    response = test_client.put(
        f'/items/{item_id}', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + access_token_2
        }
    )

    assert response.status_code == 403
    assert response.get_json(
    )['forbidden'] == 'You are not the owner of this item report!'
    clean_database()


def test_api_updates_item_given_a_valid_update_request(test_client, correct_signup_data, valid_lost_item_report):
    access_token = register_and_login_user(test_client, correct_signup_data)
    item_id = test_client.post(
        '/items', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + access_token
        }
    ).get_json()['id']
    response = test_client.put(
        f'/items/{item_id}', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + access_token
        }
    )
    assert response.status_code == 200
    assert response.get_json()['id'] == item_id
    clean_database()


def test_api_returns_404_when_deleting_non_existent_lost_and_found_item(test_client, correct_signup_data):
    response = test_client.delete(
        '/items/0', headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )
    assert response.status_code == 404
    assert response.get_json()['error'] == 'No item with id 0'
    clean_database()


def test_api_returns_403_when_deleting_existent_item_owned_by_other_user(test_client, correct_signup_data, valid_lost_item_report):
    access_token_1 = register_and_login_user(test_client, correct_signup_data)
    access_token_2 = register_and_login_user(
        test_client, {
            'username': 'Rollo',
            'phone_number': '+61-870-213021',
            'email': 'protector@paris.fr',
            'password': 'Norm4ndy'
        }
    )
    item_id = test_client.post(
        '/items', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + access_token_1
        }
    ).get_json()['id']
    response = test_client.delete(
        f'/items/{item_id}', headers={
            'Authorization': 'Bearer ' + access_token_2
        }
    )

    assert response.status_code == 403
    assert response.get_json(
    )['forbidden'] == 'You are not the owner of this item report!'
    clean_database()


def test_api_deletes_item_given_valid_delete_request(test_client, correct_signup_data, valid_lost_item_report):
    access_token = register_and_login_user(test_client, correct_signup_data)
    item_id = test_client.post(
        '/items', json=valid_lost_item_report, headers={
            'Authorization': 'Bearer ' + access_token
        }
    ).get_json()['id']
    response = test_client.delete(
        f'/items/{item_id}', headers={
            'Authorization': 'Bearer ' + access_token
        }
    )
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Item deleted'
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

    remove_test_data(correct_signup_data['username'], valid_upload_file[1])


def test_404_returned_when_fetching_non_existent_image_from_api(test_client, correct_signup_data):
    response = test_client.get(
        '/items/images/undefined-username/image.png', headers={
            'Authorization': 'Bearer ' + register_and_login_user(test_client, correct_signup_data)
        }
    )
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Requested file not found!'

    clean_database()


def test_api_returns_existent_item_image_file_for_valid_request(test_client, correct_signup_data, valid_upload_file):
    access_token = register_and_login_user(test_client, correct_signup_data)
    test_client.post(
        '/items/images', data={'image': valid_upload_file}, headers={
            'Authorization': 'Bearer ' + access_token
        }
    )
    response = test_client.get(
        f'/items/images/{correct_signup_data["username"]}/{valid_upload_file[1]}', headers={
            'Authorization': 'Bearer ' + access_token
        }
    )
    assert response.status_code == 200
    assert response.get_data()

    remove_test_data(correct_signup_data['username'], valid_upload_file[1])


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
