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


@app_views.route('/states', methods=['GET', 'POST'])
@app_views.route('/states/', methods=['GET', 'POST'])
def get_states():
    """Retrieves the list of all State object if method is GET
    Create a new State object if the method is POST"""
    if request.method == 'GET':
        states = storage.all(State)
        all_states = []
        for state in states.values():
            state_ = state.to_dict()
            all_states.append(state_)
        return jsonify(all_states)
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            abort(404, 'Not a JSON')
        if 'name' not in data:
            abort(404, 'Missing name')

        new_state = State(**data)
        new_state.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
def state(state_id):
    """Retrieves, Modifies or Deletes a State object"""
    state = storage.get(State, escape(state_id))
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    elif request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, 'Not a JSON')
        for key, value in data.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(state, key, value)
        storage.save()
        return jsonify(state.to_dict()), 200
