#!/usr/bin/python3
""" Index API
"""

from api.v1.views import app_views
from flask import jsonify, make_response, request
from models import storage


@app_views.route('/status', methods=['GET'],
                 strict_slashes=False)
def status():
    """Returns the status of the app"""
    response = {
        'status': 'OK'
    }
    return jsonify(response)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each objects by type"""
    if request.method == 'GET':
        stats = {}
        all = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }
        for key, value in all.items():
            stats[value] = storage.count(key)
        return make_response(jsonify(stats))
