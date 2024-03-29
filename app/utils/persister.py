from ..models import User, LostAndFoundItem, db
from werkzeug.security import generate_password_hash


class Persister:
    def __init__(self, json_data):
        self.json_data = json_data

    def persist(self):
        model_instance = self.get_model_instance()
        db.session.add(model_instance)
        db.session.commit()
        return self.get_persisted_data_as_json()

    # override this method in a subclass to create model instance
    # to be persisted to database
    def get_model_instance(self):
        pass

    # override this method in a subclass to retrieve data
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
            **self.json_data,
            'reporter_id': self.reporting_user.id
        }

    def get_model_instance(self):
        return LostAndFoundItem(**self.kwargs)

    def get_persisted_data_as_json(self):
        reported_item = LostAndFoundItem.query.filter_by(**self.kwargs).first()
        return {
            'id': reported_item.id,
            'item_name': reported_item.item_name,
            'description': reported_item.description,
            'image_url': reported_item.image_url,
            'report_date': reported_item.report_date,
            'reported_by': self.reporting_user.username
        }
