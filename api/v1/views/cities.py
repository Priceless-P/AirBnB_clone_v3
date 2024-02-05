#!/usr/bin/python3
""" Cities API
"""

from flask import abort
from api.v1.views import app_views
from models.city import City
from markupsafe import escape
from flask import jsonify
from flask import make_response
from flask import request
from models.state import State
from models import storage


@app_views.route('/states/<string:state_id>/cities', methods=['GET', 'POST'])
def get_create_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, escape(state_id))
    all_cities = []
    if request.method == 'GET':
        if not state:
            abort(404)
        else:
            for city in state.cities:
                city_ = city.to_dict()
                all_cities.append(city_)
            return make_response(jsonify(all_cities))
    elif request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        print(data)
        if not data:
            abort(404, "Not a JSON")
        if not name:
            abort(404, "Missing name")
        if not state:
            abort(404)

        new_city = City(name=name, state_id=state.id)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['GET', 'DELETE', 'PUT'])
def city(city_id):
    """Retrieves, Modifies or Deletes a City object"""
    city = storage.get(City, escape(city_id))
    if city is None:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(city.to_dict()))
    elif request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        if not data:
            abort(400, "Not a JSON")
        for key, value in data.items():
            if key not in ('id', 'created_at', 'updated_at'):
                setattr(city, key, value)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
