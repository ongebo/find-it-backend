from app.utils.validator import SignupValidator
from .conftest import Request


def test_validator_returns_false_if_request_not_json():
    validator = SignupValidator(Request('non-JSON string'))
    assert validator.request_invalid()
    assert validator.errors['error'] == 'Request not specified in JSON format!'


def test_validator_returns_false_if_redundant_fields_in_request_with_all_required_string_fields(redundant_request):
    validator = SignupValidator(redundant_request)
    assert validator.request_invalid()
    assert validator.errors['redundancy'] == 'Excess data specified in request!'


def test_validator_returns_false_given_invalid_required_fields(invalid_fields_request):
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
