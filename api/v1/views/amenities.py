#!/usr/bin/python3
"""cities views"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'],
                 strict_slashes=False)
def amenities_get():
    """all amenities information"""
    amenities_dict = []
    for amenity in storage.all("Amenity").values():
        amenities_dict.append(amenity.to_dict())
    return (jsonify(amenities_dict))


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET'],
                 strict_slashes=False)
def amenity_get(amenity_id):
    """amenities specific information"""
    amenity_dict = storage.get("Amenity", amenity_id)
    if amenity_dict is None:
        abort(404)
    return (jsonify(amenity_dict.to_dict()))


@app_views.route('/amenities/<string:amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """delete a amenty"""
    amenity_dict = storage.get("Amenity", amenity_id)
    if amenity_dict is None:
        abort(404)
    amenity_dict.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities',
                 methods=['POST'],
                 strict_slashes=False)
def amenity_post():
    """create a amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    amenity_dict = Amenity(**request.get_json())
    amenity_dict.save()
    return make_response(jsonify(amenity_dict.to_dict()), 201)


@app_views.route('/cities/<string:city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """update a city"""
    amenity_dict = storage.get("Amenity", amenity_id)
    if amenity_dict is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attributes, value in request.get_json().items():
        if attributes not in ['id', 'created_at', 'updated_at']:
            setattr(amenity_dict, attributes, value)
    amenity_dict.save()
    return jsonify(amenity_dict.to_dict())
