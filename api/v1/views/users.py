#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def httpGetAllUsers():
    allUser = []
    getAllInstanceUser = storage.all(User)
    for instance in getAllInstanceUser.values():
        allUser.append(instance.to_dict())
    return jsonify(allUser), 200

@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def httpGetUserByID(user_id):
    userInstance = storage.get(User, user_id)
    if userInstance is not None:
        return jsonify(userInstance.to_dict()), 200
    abort(404)

@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def httpDeleteUserByID(user_id):
    userInstance = storage.get(User, user_id)
    if userInstance is not None:
        storage.delete(userInstance)
        storage.save()
        return jsonify({}), 200
    abort(404)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def httpAddNewUser():
    dataFromRequest = request.get_json()
    if not dataFromRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in dataFromRequest:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in dataFromRequest:
        return jsonify({'error': 'Missing password'}), 400
    newUser = User(**dataFromRequest)
    newUser.save()
    return jsonify(newUser.to_dict()), 200

@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def httpModifyUserByID(user_id):
    userInstance = storage.get(User, user_id)
    if userInstance is None:
        abort(404)
    dataFromRequest = request.get_json()
    if not dataFromRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in dataFromRequest.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(userInstance, key, value)
    userInstance.save()
    return jsonify(userInstance.to_dict()), 200

