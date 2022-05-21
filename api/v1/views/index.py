#!/usr/bin/python3
"""connect the API with the database"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

stats_list = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    new_dict = {}
    for key, value in stats_list.items():
        new_dict[key] = storage.count(value)
    return jsonify(new_dict)
