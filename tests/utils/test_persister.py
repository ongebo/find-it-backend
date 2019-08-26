from app.utils.persister import db, Persister
from app.models.user import User


def test_persister_saves_user_to_database_and_returns_saved_information():
    user = {
        'username': 'John Doe',
        'phone_number': '+1-111-274654',
        'email': 'johndoe@gmail.com',
        'password': 'JohnDoe2019'
    }
    persisted_data = Persister(user).persist_user()

    # ensure user was saved to database
    saved_user = User.query.filter_by(
        username=user['username'],
        phone_number=user['phone_number'],
        email=user['email']
    ).first()
    assert saved_user

    # persister returns saved user data with an id and no password
    user['id'] = persisted_data['id']
    del user['password']
    assert user == persisted_data

    # delete saved user from database
    db.session.delete(saved_user)
    db.session.commit()
