import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('app.models.config')  # load configuration from 'config.py'
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
