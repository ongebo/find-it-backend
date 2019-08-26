from ..models.user import User, db
from werkzeug.security import generate_password_hash


class Persister:
    def __init__(self, json_data):
        self.json_data = json_data

    def persist_user(self):
        self.strip_spaces()
        user = User(
            username=self.json_data['username'],
            phone_number=self.json_data['phone_number'],
            email=self.json_data['email'],
            password=generate_password_hash(
                self.json_data['password'], method='sha256'
            )
        )
        db.session.add(user)
        db.session.commit()
        return self.get_created_record_as_json()

    def strip_spaces(self):
        for k, v in self.json_data.items():
            self.json_data[k] = v.strip()

    def get_created_record_as_json(self):
        created_record = User.query.filter_by(
            username=self.json_data['username'],
            email=self.json_data['email']
        ).first()
        json_format = {
            'id': created_record.id,
            'username': created_record.username,
            'phone_number': created_record.phone_number,
            'email': created_record.email
        }
        return json_format
