import re
from ..models.user import app, User


class RequestValidator:
    def __init__(self, request):
        self.json_data = request.get_json()
        self.required_fields = {
            'username': 'Username', 'phone_number': 'Phone number',
            'email': 'Email', 'password': 'Password'
        }
        self.errors = {}

    def request_invalid(self):
        if not self.json_data:
            self.errors['error'] = 'Request not specified in JSON format!'
            return True
        if self.not_all_required_fields_present_as_strings():
            return True
        self.ensure_no_redundant_fields_in_request()
        self.validate_username()
        self.validate_phone_number()
        self.validate_email()
        self.validate_password()
        return True if self.errors else False

    def not_all_required_fields_present_as_strings(self):
        for k, v in self.required_fields.items():
            try:
                if not isinstance(self.json_data[k], str):
                    self.errors[k] = f'{v} must be a string!'
            except KeyError:
                self.errors[k] = f'{v} not specified!'
        return True if self.errors else False

    def ensure_no_redundant_fields_in_request(self):
        for key in self.json_data:
            if key not in self.required_fields:
                self.errors['redundancy'] = 'Excess data specified in request!'

    def validate_username(self):
        name = self.json_data['username'].strip()
        name_pattern = re.compile(r'[a-zA-Z]{3,30}( [a-zA-Z]{3,30})*$')
        if not name_pattern.match(name):
            self.errors['username'] = (
                'A username can only contain letters. First, middle, and last names are '
                'separated by single spaces, each name containing atleast three characters.'
            )
            return
        if User.query.filter_by(username=name).first():
            self.errors['username'] = f'{name} already exists!'

    def validate_phone_number(self):
        number = self.json_data['phone_number'].strip()
        number_pattern = re.compile(r'\+[0-9]{1,3}-[0-9]{3}-[0-9]{6}$')
        if not number_pattern.match(number):
            self.errors['phone_number'] = 'Specify phone number in this format: +xxx-xxx-xxxxxx'
            return
        if User.query.filter_by(phone_number=number).first():
            self.errors['phone_number'] = f'{number} is already taken by another user!'

    def validate_email(self):
        email = self.json_data['email'].strip()
        email_pattern = re.compile(
            r'[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,3}((\.[a-zA-Z]{2,3})+)?$')
        if not email_pattern.match(email):
            self.errors['email'] = 'Invalid email address!'
            return
        if User.query.filter_by(email=email).first():
            self.errors['email'] = f'{email} is already taken by another user!'

    def validate_password(self):
        password = self.json_data['password'].strip()
        checks = {'a-z': str.islower, 'A-Z': str.isupper, '0-9': str.isdigit}
        for character in password:
            for key, check in checks.items():
                if check(character):
                    del checks[key]
                    break  # move onto the next character
        if len(checks) > 0 and not 6 <= len(password) <= 12:
            self.errors['password'] = (
                'Password must contain atleast one lowercase letter, one uppercase letter,'
                ' a digit and be 6 to 12 characters long!'
            )
