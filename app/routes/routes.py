import os
from flask import request, jsonify, send_file
from .. import app
from ..utils.validator import SignupValidator, LoginValidator, LostAndFoundItemValidator
from ..utils.persister import UserPersister, LostAndFoundItemPersister
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity,
    jwt_refresh_token_required
)
from werkzeug.utils import secure_filename
from ..models import LostAndFoundItem, User, get_item_as_json, db, user_not_item_owner


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


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_access_token():
    return jsonify({
        'access_token': create_access_token(identity=get_jwt_identity())
    }), 200


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


@app.route('/items', methods=['GET'])
@jwt_required
def get_lost_and_found_items():
    response = {'items': []}
    for item in LostAndFoundItem.query.all():
        response['items'].append(get_item_as_json(item))
    if not response['items']:
        return jsonify({'error': 'No lost and found items!'}), 404
    return jsonify(response), 200


@app.route('/items/<int:item_id>', methods=['GET'])
@jwt_required
def get_specific_lost_and_found_item(item_id):
    item = LostAndFoundItem.query.filter_by(id=item_id).first()
    if not item:
        return jsonify({'error': f'No item with id {item_id}'}), 404
    return jsonify(get_item_as_json(item)), 200


@app.route('/items/<int:item_id>', methods=['PUT'])
@jwt_required
def update_specific_lost_and_found_item(item_id):
    validator = LostAndFoundItemValidator(request, updating=True)
    if validator.request_invalid():
        return jsonify({'errors': validator.errors}), 400
    item = LostAndFoundItem.query.filter_by(id=item_id).first()
    if not item:
        return jsonify({'error': f'No item with id {item_id}'}), 404

    if user_not_item_owner(get_jwt_identity(), item):
        return jsonify({'forbidden': 'You are not the owner of this item report!'}), 403

    item.item_name = request.get_json()['item_name']
    item.description = request.get_json()['description']
    item.image_url = request.get_json()['image_url']
    db.session.commit()
    return jsonify(get_item_as_json(item)), 200


@app.route('/items/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete_specific_lost_and_found_item(item_id):
    item = LostAndFoundItem.query.filter_by(id=item_id).first()
    if not item:
        return jsonify({'error': f'No item with id {item_id}'}), 404

    if user_not_item_owner(get_jwt_identity(), item):
        return jsonify({'forbidden': 'You are not the owner of this item report!'}), 403

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 200


@app.route('/items/images', methods=['POST'])
@jwt_required
def post_item_image():
    validator = LostAndFoundItemValidator(request)
    if validator.uploaded_image_invalid():
        return jsonify({'errors': validator.uploaded_image_errors}), 400
    image_file = request.files['image']
    secure_name = secure_filename(image_file.filename)

    # set up directory for saving uploaded image
    username = User.query.filter_by(email=get_jwt_identity()).first().username
    save_directory = os.path.join(app.config['UPLOAD_FOLDER'], username)
    if not os.path.exists(save_directory):
        os.mkdir(save_directory)

    image_file.save(os.path.join(save_directory, secure_name))
    return jsonify({
        'image_url': os.path.join(
            request.base_url, username, secure_name
        )
    }), 201


@app.route('/items/images/<username>/<image_name>')
@jwt_required
def get_item_image(username, image_name):
    filename = os.path.join(app.config['UPLOAD_FOLDER'], username, image_name)
    try:
        file = open(filename, 'r')
        return send_file(file.name), 200
    except FileNotFoundError:
        return jsonify({'error': 'Requested file not found!'}), 404


@app.errorhandler(413)
def display_file_too_large_error(error):
    return jsonify({'error': 'Image larger than 5 megabytes!'}), 413


@app.errorhandler(404)
def display_404_error(error):
    return jsonify({'error': 'The requested resource does not exist!'}), 404
