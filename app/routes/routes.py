from flask import request, jsonify
from ..utils.validator import app, RequestValidator


@app.route('/users', methods=['POST'])
def register_user():
    validator = RequestValidator(request)
    if validator.request_invalid():
        return jsonify(validator.errors), 400
    return jsonify({'success': 'Request in JSON Format!'}), 201
