#!/usr/bin/python3
"""amenity_routes.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity as Amt


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def fetch_amenities():
    """Retrieve all amenities information"""
    amenities_info = []
    for amty in storage.all("Amenity").values():
        amenities_info.append(amty.to_dict())
    return jsonify(amenities_info)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def fetch_single_amenity(amenity_id):
    """Retrieve information for a single amenity"""
    amty = storage.get("Amenity", amenity_id)
    if amty is None:
        abort(404)
    return jsonify(amty.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def remove_amenity(amenity_id):
    """Remove an amenity based on its ID"""
    amty = storage.get("Amenity", amenity_id)
    if amty is None:
        abort(404)
    amty.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Add a new amenity"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Data not in JSON format'}),
                             400)
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Name field missing'}), 400)
    amty = Amt(**request.get_json())
    amty.save()
    return make_response(jsonify(amty.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Modify an existing amenity"""
    amty = storage.get("Amenity", amenity_id)
    if amty is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Data not in JSON format'}),
                             400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amty, attr, val)
    amty.save()
    return jsonify(amty.to_dict())
