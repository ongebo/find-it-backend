import os
from flask import request, jsonify
from .. import app
from ..utils.validator import SignupValidator, LoginValidator, LostAndFoundItemValidator
from ..utils.persister import UserPersister, LostAndFoundItemPersister
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)
from werkzeug.utils import secure_filename


@app.route('/users', methods=['POST'])
def register_user():
    validator = SignupValidator(request)
    if validator.request_invalid():
        return jsonify({'errors': validator.errors}), 400
    persister = UserPersister(request.get_json())
    created_data = persister.persist()
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


@app.route('/items', methods=['POST'])
@jwt_required
def report_lost_and_found_item():
    validator = LostAndFoundItemValidator(request)
    if validator.request_invalid():
        return jsonify({'errors': validator.errors}), 400
    persister = LostAndFoundItemPersister(
        request.get_json(), get_jwt_identity()
    )
    reported_item = persister.persist()
    return jsonify(reported_item), 201


@app.route('/items/images', methods=['POST'])
@jwt_required
def post_item_image():
    validator = LostAndFoundItemValidator(request)
    if validator.uploaded_image_invalid():
        return jsonify({'errors': validator.uploaded_image_errors}), 400
    image_file = request.files['image']
    secure_name = secure_filename(image_file.filename)
    image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_name))
    return jsonify({
        'image_url': os.path.join(
            request.base_url, secure_name
        )
    }), 200


@app.errorhandler(413)
def display_file_too_large_error(error):
    return jsonify({'error': 'Image larger than 5 megabytes!'}), 413


@app.errorhandler(404)
def display_404_error(error):
    return jsonify({'error': 'The requested resource does not exist!'}), 404
