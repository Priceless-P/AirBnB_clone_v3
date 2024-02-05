#!/usr/bin/python3
"""places vies"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Get place information for all places in a specified city."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places_data = [place.to_dict() for place in city.places]
    return jsonify(places_data)


@app_views.route('/places/<string:place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Get place information for a specified place."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Delete a place based on its place_id."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Create a new place."""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    place_data = request.get_json()
    if 'user_id' not in place_data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get("User", place_data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in place_data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    place_data['city_id'] = city_id
    place = Place(**place_data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Update a place."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    updated_data = request.get_json()
    for attribute, value in updated_data.items():
        if attribute not in ['id', 'user_id',
                             'city_id', 'created_at', 'updated_at']:
            setattr(place, attribute, value)
    place.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """Search for places."""
    if not request.is_json:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    search_params = request.get_json()
    states = search_params.get('states', [])
    cities = search_params.get('cities', [])
    amenities = search_params.get('amenities', [])
    amenity_objects = [storage.get('Amenity', amenity_id)
                       for amenity_id in amenities if amenity_id]

    if not states and not cities:
        all_places = storage.all('Place').values()
    else:
        all_places = []
        for state_id in states:
            state = storage.get('State', state_id)
            if state:
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
        for city_id in cities:
            city = storage.get('City', city_id)
            if city:
                all_places.extend(city.places)

    confirmed_places = []
    for place in all_places:
        place_amenities = place.amenities
        if all(amenity in place_amenities for amenity in amenity_objects):
            confirmed_places.append(place.to_dict())

    return jsonify(confirmed_places)
