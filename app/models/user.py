import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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
