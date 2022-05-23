#!/usr/bin/python3

"""
Manage the link of amenities and place
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<string:place_id>/amenities",
                 methods=['GET'],
                 strict_slashes=False)
def httpGetAllAmenitiesFromPlaceByID(place_id):
    """
    GET /places/<place_id>/amenities
    Get all amenities linked to a given place
    If the ID of the place is not linked to a place
        error 404 is raised
    Return: All the amenities in a json format
    """
    placeInstance = storage.get(Place, place_id)
    if placeInstance is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        allAmenities = placeInstance.amenities
    else:
        allAmenities = placeInstance.amenity_ids
    amenitiesList = []
    for amenity in allAmenities:
        amenitiesList.append(amenity.to_dict())
    return jsonify(amenitiesList), 200


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=['DELETE'],
                 strict_slashes=False)
def httpDeleteAmenityLinkedToPlaceByID(place_id, amenity_id):
    """
    DELETE /places/<place_id>/amenities/<amenity_id>
    Delete a given amenity linked to a given place
    If the ID of the place is not linked to a place,
        or the ID of an amenity is not linked to an amenity
        error 404 is raised
    Return: A empty json object
    """
    placeInstance = storage.get(Place, place_id)
    if placeInstance is None:
        abort(404)
    amenityInstance = storage.get(Amenity, amenity_id)
    if amenityInstance is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        allAmenities = placeInstance.amenities
    else:
        allAmenities = placeInstance.amenity_ids
    if amenityInstance not in allAmenities:
        abort(404)
    allAmenities.remove(amenityInstance)
    placeInstance.save()
    return jsonify({}), 200


@app_views.route("/places/<string:place_id>/amenities/<string:amenity_id>",
                 methods=['POST'],
                 strict_slashes=False)
def httpLinkAmenityToPlaceByID(place_id, amenity_id):
    """
    POST /places/<place_id>/amenities/<amenity_id>
    Link a given amenity linked to a given place
    If the ID of the place is not linked to a place,
        or the ID of an amenity is not linked to an amenity
        error 404 is raised
    Return: The json object of the linked amenity
    """
    placeInstance = storage.get(Place, place_id)
    if placeInstance is None:
        abort(404)
    amenityInstance = storage.get(Amenity, amenity_id)
    if amenityInstance is None:
        abort(404)
    if getenv("HBNB_TYPE_STORAGE") == "db":
        allAmenities = placeInstance.amenities
    else:
        allAmenities = placeInstance.amenity_ids
    if amenityInstance in allAmenities:
        return jsonify(amenityInstance.to_dict()), 200
    allAmenities.append(amenityInstance)
    placeInstance.save()
    return jsonify(amenityInstance.to_dict()), 201
