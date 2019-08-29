from app.utils.persister import UserPersister, LostAndFoundItemPersister
from app.models import User, LostAndFoundItem
from ..test_utils import clean_database


def test_persister_saves_user_to_database_and_returns_saved_information():
    user = {
        'username': 'John Doe',
        'phone_number': '+1-111-274654',
        'email': 'johndoe@gmail.com',
        'password': 'JohnDoe2019'
    }
    persisted_data = UserPersister(user).persist()

    # ensure user was saved to database
    assert User.query.filter_by(
        username=user['username'],
        phone_number=user['phone_number'],
        email=user['email']
    ).first()

    # persister returns saved user data with an id and no password
    user['id'] = persisted_data['id']
    del user['password']
    assert user == persisted_data

    clean_database()


def test_persister_saves_lost_and_found_item_and_returns_saved_information():
    user = {
        'username': 'John Doe',
        'phone_number': '+1-111-274654',
        'email': 'johndoe@gmail.com',
        'password': 'JohnDoe2019'
    }
    UserPersister(user).persist()
    lost_item = {
        'item_name': 'Black Jacket',
        'description': 'Found at the cafeteria.',
        'image_url': 'http://somedomain.com/some-image.png'
    }
    persisted_data = LostAndFoundItemPersister(lost_item, user['email']).persist()

    assert persisted_data['item_name'] == lost_item['item_name']
    assert persisted_data['description'] == lost_item['description']
    assert persisted_data['image_url'] == lost_item['image_url']
    assert 'id' in persisted_data
    assert 'report_date' in persisted_data
    assert 'reported_by' in persisted_data

    clean_database()
