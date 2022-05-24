#!/usr/bin/python3
"""cities views"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State
from models.city import City
from flasgger import Swagger, swag_from


@app_views.route('/states/<string:state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/cities/cities_by_states_get.yml')
def cities_get(state_id):
    """all cities information"""
    state_dict = storage.get("State", state_id)
    if state_dict is None:
        abort(404)
    cities_dict = []
    for city in state_dict.cities:
        cities_dict.append(city.to_dict())
    return jsonify(cities_dict)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/cities/cities_id_get.yml')
def city_get(city_id):
    """cities specific information"""
    city_dict = storage.get("City", city_id)
    if city_dict is None:
        abort(404)
    return (jsonify(city_dict.to_dict()))


@app_views.route('/cities/<string:city_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/cities/cities_id_delete.yml')
def city_delete(city_id):
    """delete a city"""
    city_dict = storage.get("City", city_id)
    if city_dict is None:
        abort(404)
    city_dict.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/<string:state_id>/cities/',
                 methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/cities/cities_by_states_post.yml')
def city_post(state_id):
    """create a city"""
    state_dict = storage.get("State", state_id)
    if state_dict is None:
        abort(404)
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if 'name' not in request.get_json():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    arguments = request.get_json()
    arguments['state_id'] = state_id
    city_dict = City(**arguments)
    city_dict.save()
    return (make_response(jsonify(city_dict.to_dict()), 201))


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
@swag_from('documentation/cities/cities_id_put.yml')
def city_put(city_id):
    """update a city"""
    city_dict = storage.get("City", city_id)
    if city_dict is None:
        abort(404)
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for attributes, value in request.get_json().items():
        if attributes not in ['id',
                              'state_id',
                              'created_at',
                              'updated_at']:
            setattr(city_dict, attributes, value)
    city_dict.save()
    return (jsonify(city_dict.to_dict()))
