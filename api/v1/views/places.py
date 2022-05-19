#!/usr/bin/python3

"""
Place controler file
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def httpGetUserPlaceByCityID(city_id):
    """
    GET /api/v1/cities/<city_id>/places
    Get all the place from a city, based on its ID
    If the ID do not match with any cities, error 404 is
        raised
    Return: All places through json object
    """
    cityInstance = storage.get(City, city_id)
    if cityInstance is None:
        abort(404)
    allPlaces = []
    for place in cityInstance.places:
        allPlaces.append(place.to_dict())
    return jsonify(allPlaces), 200


@app_views.route('/places/<string:place_id>',
                 methods=['GET'],
                 strict_slashes=False)
def httpGetPlaceByID(place_id):
    """
    GET /api/v1/places/<place_id>
    Get a place based on given ID
    If the ID do not match with any place, error 404 is
        raised
    Return: The matched place through json object
    """
    placeInstance = storage.get(Place, place_id)
    if placeInstance is not None:
        return jsonify(placeInstance.to_dict()), 200
    abort(404)


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def httpDeletePlaceByID(place_id):
    """
    DELETE /api/v1/places/<place_id>
    Delete a place based on given ID
    If the ID do not match with any place, error 404 is
        raised
    Return: A empty json object
    """
    placeInstance = storage.get(Place, place_id)
    if placeInstance is not None:
        storage.delete(placeInstance)
        storage.save()
        return jsonify({}), 200
    abort(404)


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'],
                 strict_slashes=False)
def httpAddNewPlace(city_id):
    """
    POST /api/v1/places
    Post a new place to the database, user_id and name
        required
    Return: Return the new created place through json object
    """
    if storage.get(City, city_id) is None:
        return jsonify({"error": "City id doesn't match"}), 404
    dataFromRequest = request.get_json()
    if not dataFromRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in dataFromRequest:
        return jsonify({'error': 'Missing user_id'}), 400
    if storage.get(User, dataFromRequest['user_id']) is None:
        return jsonify({'error': "User id doesn't match"}), 404
    if 'name' not in dataFromRequest:
        return jsonify({'error': 'Missing name'}), 400
    dataFromRequest['city_id'] = city_id
    newPlace = Place(**dataFromRequest)
    newPlace.save()
    return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def httpModifyPlaceByID(place_id):
    """
    PUT /api/v1/places/<place_id>
    Update a place based on given ID
    If the ID do not match with any place, error 404 is
        raised
    Return: The place through a json object
    """
    placeInstance = storage.get(Place, place_id)
    if placeInstance is None:
        abort(404)
    dataFromRequest = request.get_json()
    if not dataFromRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    for key, value in dataFromRequest.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(placeInstance, key, value)
    placeInstance.save()
    return jsonify(placeInstance.to_dict()), 200
