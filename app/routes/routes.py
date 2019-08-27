from flask import request, jsonify
from .. import app
from ..utils.validator import RequestValidator
from ..utils.persister import Persister


@app.route('/users', methods=['POST'])
def register_user():
    validator = RequestValidator(request)
    if validator.request_invalid():
        return jsonify({'errors': validator.errors}), 400
    persister = Persister(request.get_json())
    created_data = persister.persist_user()
    return jsonify(created_data), 201
