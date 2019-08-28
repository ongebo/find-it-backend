from ..models import User, LostAndFoundItem, db
from werkzeug.security import generate_password_hash


class UserPersister:
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


class LostAndFoundItemPersister:
    def __init__(self, json_data):
        self.json_data = json_data

    def persist_item(self, reporter_email):
        self.strip_spaces()
        self.reporting_user = User.query.filter_by(
            email=reporter_email
        ).first()
        lost_and_found_item = LostAndFoundItem(
            name=self.json_data['item_name'],
            description=self.json_data['description'],
            image_path=self.json_data['image_url'],
            reporter_id=self.reporting_user.id
        )
        db.session.add(lost_and_found_item)
        db.session.commit()
        return self.get_reported_item_as_json()

    def strip_spaces(self):
        for k, v in self.json_data.items():
            self.json_data[k] = v.strip()

    def get_reported_item_as_json(self):
        reported_item = LostAndFoundItem.query.filter_by(
            name=self.json_data['item_name'],
            description=self.json_data['description'],
            image_path=self.json_data['image_url'],
            reporter_id=self.reporting_user.id
        ).first()
        return {
            'id': reported_item.id,
            'item_name': reported_item.name,
            'description': reported_item.description,
            'image_url': reported_item.image_path,
            'report_date': reported_item.report_date,
            'reported_by': self.reporting_user.username
        }
