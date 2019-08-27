from flask import request, jsonify
from .. import app
from ..utils.validator import SignupValidator
from ..utils.persister import UserPersister


@app.route('/users', methods=['POST'])
def register_user():
    validator = SignupValidator(request)
    if validator.request_invalid():
        return jsonify({'errors': validator.errors}), 400
    persister = UserPersister(request.get_json())
    created_data = persister.persist_user()
    return jsonify(created_data), 201
