#!/usr/bin/python3

"""
User controler file
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from flasgger import Swagger, swag_from


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/users/GET_ALL_user.yml')
def httpGetAllUsers():
    """
    GET /api/v1/users
    Get all the users from the database
    Return: All the user through json object
    """
    allUser = []
    getAllInstanceUser = storage.all(User)
    for instance in getAllInstanceUser.values():
        allUser.append(instance.to_dict())
    return jsonify(allUser), 200


@app_views.route('/users/<string:user_id>',
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/users/GET_user.yml')
def httpGetUserByID(user_id):
    """
    GET /api/v1/users/<user_id>
    Get a user based on given ID
    If the ID do not match with any user, error 404 is
        raised
    Return: The matched user through json object
    """
    userInstance = storage.get(User, user_id)
    if userInstance is not None:
        return jsonify(userInstance.to_dict()), 200
    abort(404)


@app_views.route('/users/<string:user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/users/DELETE_user.yml')
def httpDeleteUserByID(user_id):
    """
    DELETE /api/v1/users/<user_id>
    Delete a user based on given ID
    If the ID do not match with any user, error 404 is
        raised
    Return: A empty json object
    """
    userInstance = storage.get(User, user_id)
    if userInstance is not None:
        storage.delete(userInstance)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/users',
                 methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/users/POST_user.yml')
def httpAddNewUser():
    """
    POST /api/v1/users
    Post a new user to the database, email and password
        required
    Return: Return the new created user through json object
    """
    dataFromRequest = request.get_json()
    if not dataFromRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in dataFromRequest:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in dataFromRequest:
        return jsonify({'error': 'Missing password'}), 400
    newUser = User(**dataFromRequest)
    newUser.save()
    return jsonify(newUser.to_dict()), 201


@app_views.route('/users/<string:user_id>',
                 methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/users/PUT_user.yml')
def httpModifyUserByID(user_id):
    """
    PUT /api/v1/users/<user_id>
    Update a user based on given ID
    If the ID do not match with any user, error 404 is
        raised
    Return: The user through a json object
    """
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
