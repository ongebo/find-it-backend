from app.utils.validator import SignupValidator, LoginValidator
from app.utils.persister import db, UserPersister
from app.models.user import User
from .conftest import Request


def test_validator_returns_invalid_if_request_not_json():
    validator = SignupValidator(Request('non-JSON string'))
    assert validator.request_invalid()
    assert validator.errors['error'] == 'Request not specified in JSON format!'


def test_validator_returns_invalid_if_redundant_fields_in_request_with_all_required_string_fields(redundant_request):
    validator = SignupValidator(redundant_request)
    assert validator.request_invalid()
    assert validator.errors['school'] == '"school" not required!'


def test_validator_returns_invalid_given_invalid_required_fields(invalid_fields_request):
    validator = SignupValidator(invalid_fields_request)
    assert validator.request_invalid()
    assert validator.errors['username'] == (
        'A username can only contain letters. First, middle, and last names are '
        'separated by single spaces, each name containing atleast three characters.'
    )
    assert validator.errors['phone_number'] == 'Specify phone number in this format: +xxx-xxx-xxxxxx'
    assert validator.errors['email'] == 'Invalid email address!'
    assert validator.errors['password'] == (
        'Password must contain atleast one lowercase letter, one uppercase letter,'
        ' a digit and be 6 to 12 characters long!'
    )


def test_login_validator_returns_invalid_given_incorrect_email():
    invalid_login_credentials = Request({
        'email': 'AnastasiaSteele@gmail.com', 'password': 'ShadesOfGrey'
    })
    login_validator = LoginValidator(invalid_login_credentials)
    assert login_validator.request_invalid()
    assert login_validator.errors['email'] == 'Incorrect email address!'


def test_login_validator_returns_invalid_given_incorrect_password():
    # register a user to database
    user = {
        'username': 'John Doe',
        'phone_number': '+1-111-274654',
        'email': 'johndoe@gmail.com',
        'password': 'JohnDoe2019'
    }
    UserPersister(user).persist()

    # attempt to login with wrong password
    invalid_login_password = Request({
        'email': 'johndoe@gmail.com', 'password': 'Johnathan Doe'
    })
    login_validator = LoginValidator(invalid_login_password)
    assert login_validator.request_invalid()
    assert login_validator.errors['password'] == 'Incorrect password!'

    # delete registered user from database
    db.session.delete(User.query.filter_by(
        username=user['username'], email=user['email']
    ).first())
    db.session.commit()
