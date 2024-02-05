#!/usr/bin/python3
""" States API
"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort
from flask import jsonify
from markupsafe import escape
from flask import request
from flask import make_response


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieves the list of all State object """
    states = storage.all(State)
    all_states = []
    for state in states.values():
        state_ = state.to_dict()
        all_states.append(state_)
    return make_response(jsonify(all_states))


@app_views.route('/states', methods=['POST'])
def create_state():
    """Creates a new State object"""
    data = request.get_json()
    name = data.get('name')
    if not data:
        abort(404, 'Not a JSON')
    if not name:
        abort(404, 'Missing name')

    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a State object"""
    state = storage.get(State, escape(state_id))
    if state is None:
        abort(404)
    return make_response(jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['PUT'])
def edit_state(state_id):
    """Modifies a State object"""
    state = storage.get(State, escape(state_id))
    data = request.get_json()
    if state is None:
        abort(404)
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, escape(state_id))
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)
