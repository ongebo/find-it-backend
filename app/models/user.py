from .. import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column('username', db.String, unique=True, nullable=False)
    phone_number = db.Column(
        'phone_number', db.String,
        unique=True, nullable=False
    )
    email = db.Column('email', db.String, unique=True, nullable=False)
    password = db.Column('password', db.String, nullable=False)
    reporter = db.relationship('LostAndFoundItem', cascade='all,delete')
