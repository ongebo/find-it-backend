import re
from ..models import User, LostAndFoundItem
from werkzeug.security import check_password_hash


class Validator:
    def __init__(self, request):
        self.json_data = request.get_json()
        self.required_fields = {}  # override this in a subclass
        self.errors = {}

    def request_invalid(self):
        if not self.json_data:
            self.errors['error'] = 'Request not specified in JSON format!'
            return True
        if self.redundant_fields_in_request():
            return True
        if self.not_all_required_fields_present_as_strings():
            return True
        self.validate_required_fields()
        return True if self.errors else False

    def redundant_fields_in_request(self):
        for field in self.json_data:
            if field not in self.required_fields:
                self.errors[field] = f'"{field}" not required!'
        return True if self.errors else False

    def not_all_required_fields_present_as_strings(self):
        specified_required_fields = []

        # log an error if a required field is not specified
        for k, v in self.required_fields.items():
            if k not in self.json_data:
                self.errors[k] = f'{v} not specified!'
            else:
                specified_required_fields.append(k)

        # log an error if a required field is not a string
        for field in specified_required_fields:
            if not isinstance(self.json_data[field], str):
                self.errors[field] = f'{field} must be a string!'

        return True if self.errors else False

    # override this method in a subclass to log errors if specified
    # required fields are invalid (e.g. incorrect password)
    def validate_required_fields(self):
        pass


class SignupValidator(Validator):
    def __init__(self, request):
        super().__init__(request)
        self.required_fields = {
            'username': 'Username', 'phone_number': 'Phone number',
            'email': 'Email', 'password': 'Password'
        }

    def validate_required_fields(self):
        self.validate_field(
            'username', r'[a-zA-Z]{3,30}( [a-zA-Z]{3,30})*$',
            (
                'A username can only contain letters. First, middle, and last names are '
                'separated by single spaces, each name containing atleast three characters.'
            )
        )
        self.validate_field(
            'phone_number', r'\+[0-9]{1,3}-[0-9]{3}-[0-9]{6}$',
            'Specify phone number in this format: +xxx-xxx-xxxxxx'
        )
        self.validate_field(
            'email', r'[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]{2,3}((\.[a-zA-Z]{2,3})+)?$',
            'Invalid email address!'
        )
        self.validate_password()

    def validate_field(self, field, regex, error_message):
        field_value = self.json_data[field].strip()
        field_pattern = re.compile(regex)
        if not field_pattern.match(field_value):
            self.errors[field] = error_message
            return
        self.ensure_field_value_not_in_database(field, field_value)

    def ensure_field_value_not_in_database(self, field, field_value):
        if field == 'username' and User.query.filter_by(username=field_value).first():
            self.errors['username'] = f'{field_value} already exists!'
        elif field == 'phone_number' and User.query.filter_by(phone_number=field_value).first():
            self.errors['phone_number'] = f'{field_value} is already taken by another user!'
        elif field == 'email' and User.query.filter_by(email=field_value).first():
            self.errors['email'] = f'{field_value} is already taken by another user!'

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


class LoginValidator(Validator):
    def __init__(self, request):
        super().__init__(request)
        self.required_fields = {'email': 'Email', 'password': 'Password'}

    def validate_required_fields(self):
        user = User.query.filter_by(email=self.json_data['email']).first()
        if not user:
            self.errors['email'] = 'Incorrect email address!'
            return
        if not check_password_hash(user.password, self.json_data['password']):
            self.errors['password'] = 'Incorrect password!'


class LostAndFoundItemValidator(Validator):
    def __init__(self, request):
        super().__init__(request)
        self.required_fields = {
            'item_name': 'Item name', 'description': 'Description', 'image_url': 'Image url'
        }
        self.request = request

    def validate_required_fields(self):
        if len(self.json_data['item_name'].strip()) < 3:
            self.errors['item_name'] = 'Item name should contain atleast 3 characters!'
        if len(self.json_data['description'].strip()) < 12:
            self.errors['description'] = 'Item description should contain atleast 12 characters!'
        if LostAndFoundItem.query.filter_by(
            name=self.json_data['item_name'].strip(),
            description=self.json_data['description'].strip(),
            image_path=self.json_data['image_url'].strip()
        ).first():
            self.errors['error'] = 'This item has already been reported!'

    def uploaded_image_invalid(self):
        self.accepted_file_extensions = ('png', 'jpg', 'jpeg')
        self.uploaded_image_errors = {}
        self.validate_uploaded_image()
        return True if self.uploaded_image_errors else False

    def validate_uploaded_image(self):
        try:
            item_image = self.request.files['image']
            if not self.image_filename_valid(item_image.filename):
                self.uploaded_image_errors['image'] = 'Specify a .png, .jpg, or .jpeg file!'
        except KeyError:
            self.uploaded_image_errors['image'] = 'Image file not specified!'

    def image_filename_valid(self, filename):
        if '.' in filename:
            return filename.rsplit('.', 1)[1].lower() in self.accepted_file_extensions
        return False
