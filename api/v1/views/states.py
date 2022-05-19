#!/usr/bin/python3
"""states views"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states',
                 methods=['GET'],
                 strict_slashes=False)
def states_get():
    """all states information"""
    states_dict = []
    for state in storage.all("State").values():
        states_dict.append(state.to_dict())
    return (jsonify(states_dict))


@app_views.route('/states/<string:state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def state_get(state_id):
    """state specific information"""
    state_dict = storage.get("State", state_id)
    if state_dict is None:
        abort(404)
    return (jsonify(state_dict.to_dict()))


@app_views.route('/states/<string:state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def state_delete(state_id):
    """delete a state"""
    state_dict = storage.get("State", state_id)
    if state_dict is None:
        abort(404)
    state_dict.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/',
                 methods=['POST'],
                 strict_slashes=False)
def state_post():
    """create a state"""
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    if 'name' not in request.get_json():
        return (make_response(jsonify({'error': 'Missing name'}), 400))
    state = State(**request.get_json())
    state.save()
    return (make_response(jsonify(state.to_dict()), 201))


@app_views.route('/states/<string:state_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def state_put(state_id):
    """update a state"""
    state_dict = storage.get("State", state_id)
    if state_dict is None:
        abort(404)
    if not request.get_json():
        return (make_response(jsonify({'error': 'Not a JSON'}), 400))
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(state_dict, attr, val)
    state_dict.save()
    return (jsonify(state_dict.to_dict()))
