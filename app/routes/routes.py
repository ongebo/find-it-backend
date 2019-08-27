from flask import request, jsonify
from .. import app
from ..utils.validator import SignupValidator, LoginValidator
from ..utils.persister import UserPersister
from flask_jwt_extended import create_access_token, create_refresh_token


@app.route('/users', methods=['POST'])
def register_user():
    validator = SignupValidator(request)
    if validator.request_invalid():
        return jsonify({'errors': validator.errors}), 400
    persister = UserPersister(request.get_json())
    created_data = persister.persist_user()
    return jsonify(created_data), 201


@app.route('/login', methods=['POST'])
def login_user():
    validator = LoginValidator(request)
    if validator.request_invalid():
        return jsonify({'errors': validator.errors}), 400
    credentials = request.get_json()
    return jsonify({
        'access_token': create_access_token(identity=credentials['email']),
        'refresh_token': create_refresh_token(identity=credentials['email']),
    })
