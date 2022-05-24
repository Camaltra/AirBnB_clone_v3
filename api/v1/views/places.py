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
from models.state import State
from models.amenity import Amenity
from flasgger import Swagger, swag_from


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/places/places_by_city_get.yml')
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
@swag_from('documentation/places/places_id_get.yml')
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
@swag_from('documentation/places/places_id_delete.yml')
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
@swag_from('documentation/places/places_by_city_post.yml')
def httpAddNewPlace(city_id):
    """
    POST /api/v1/places
    Post a new place to the database, user_id and name
        required
    Return: Return the new created place through json object
    """
    if storage.get(City, city_id) is None:
        abort(404)
    dataFromRequest = request.get_json()
    if not dataFromRequest:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in dataFromRequest:
        return jsonify({'error': 'Missing user_id'}), 400
    if storage.get(User, dataFromRequest['user_id']) is None:
        abort(404)
    if 'name' not in dataFromRequest:
        return jsonify({'error': 'Missing name'}), 400
    dataFromRequest['city_id'] = city_id
    newPlace = Place(**dataFromRequest)
    newPlace.save()
    return jsonify(newPlace.to_dict()), 201


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/places/places_id_put.yml')
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


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
@swag_from('documentation/places/places_by_city_post.yml')
def httpSearchPlaceFromCriteria():
    """
    GEt all Place through some criteria
    If states list is not empty, results should include
        all Place objects for each State id listed
    If cities list is not empty, results should include
        all Place objects for each City id listed
    Keys states and cities are inclusive. Search results
        should include all Place objects in storage related
        to each City in every State listed in states, plus
        every City listed individually in cities, unless that
        City was already included by states.
    If amenities list is not empty, limit search results to only
        Place objects having all Amenity ids listed
    """
    body = request.get_json()
    if type(body) != dict:
        abort(400, description="Not a JSON")
    statesId = body.get("states", [])
    citiesId = body.get("cities", [])
    amenitiesId = body.get("amenities", [])
    places = []
    states = []
    cities = []
    amenities = []

    for idAmenity in amenitiesId:
        amenityInstance = storage.get(Amenity, idAmenity)
        if amenityInstance:
            amenities.append(amenityInstance)

    if statesId == citiesId == []:
        places = storage.all(Place).values()

    else:
        for idState in statesId:
            stateInstance = storage.get(State, idState)
            if stateInstance:
                states.append(stateInstance)

        for state in states:
            for city in state.cities:
                cities.append(city)

        for idCity in citiesId:
            cityInstance = storage.get(City, idCity)
            if cityInstance:
                if cityInstance not in cities:
                    cities.append(cityInstance)

        for city in cities:
            for place in city.places:
                places.append(place)

    outputPlace = []
    for place in places:
        outputPlace.append(place.to_dict())
        for amenity in amenities:
            if amenity not in place.amenities:
                outputPlace.pop()
                break

    return jsonify(outputPlace), 200
