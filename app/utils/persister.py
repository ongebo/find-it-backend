from ..models import User, LostAndFoundItem, db
from werkzeug.security import generate_password_hash


class Persister:
    def __init__(self, json_data):
        self.json_data = json_data

    def persist(self):
        self.strip_spaces()
        model_instance = self.get_model_instance()
        db.session.add(model_instance)
        db.session.commit()
        return self.get_persisted_data_as_json()

    def strip_spaces(self):
        for k, v in self.json_data.items():
            self.json_data[k] = v.strip()

    # override this method in a subclass to create a model instance
    # to be persisted to the database
    def get_model_instance(self):
        pass

    # override this method in a subclass to retrieve data persisted
    # persisted to database
    def get_persisted_data_as_json(self):
        pass


class UserPersister(Persister):
    def __init__(self, json_data):
        super().__init__(json_data)

    def get_model_instance(self):
        return User(
            username=self.json_data['username'],
            phone_number=self.json_data['phone_number'],
            email=self.json_data['email'],
            password=generate_password_hash(
                self.json_data['password'], method='sha256'
            )
        )

    def get_persisted_data_as_json(self):
        registered_user = User.query.filter_by(
            username=self.json_data['username'],
            email=self.json_data['email']
        ).first()
        return {
            'id': registered_user.id,
            'username': registered_user.username,
            'phone_number': registered_user.phone_number,
            'email': registered_user.email
        }


class LostAndFoundItemPersister(Persister):
    def __init__(self, json_data, reporter_email):
        super().__init__(json_data)
        self.reporting_user = User.query.filter_by(
            email=reporter_email
        ).first()
        self.kwargs = {
            'name': self.json_data['item_name'],
            'description': self.json_data['description'],
            'image_path': self.json_data['image_url'],
            'reporter_id': self.reporting_user.id
        }

    def get_model_instance(self):
        return LostAndFoundItem(**self.kwargs)

    def get_persisted_data_as_json(self):
        reported_item = LostAndFoundItem.query.filter_by(**self.kwargs).first()
        return {
            'id': reported_item.id,
            'item_name': reported_item.name,
            'description': reported_item.description,
            'image_url': reported_item.image_path,
            'report_date': reported_item.report_date,
            'reported_by': self.reporting_user.username
        }
