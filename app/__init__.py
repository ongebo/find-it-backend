from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)

# load app configuration from 'config.py'
app.config.from_object('app.config')

db = SQLAlchemy(app)

JWTManager(app)
