#!/usr/bin/python3
""" Index API
"""

from models.amenity import Amenity
from api.v1.views import app_views
from models.city import City
from flask import jsonify, make_response
from models.place import Place
from models.review import Review
from models.state import State
from models import storage
from models.user import User


@app_views.route('/status')
def status():
    """Returns the status of the app"""
    response = {
        'status': 'OK'
    }
    return jsonify(response)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """Retrieves the number of each objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    stats = {}
    for i in range(len(classes)):
        stats[names[i]] = storage.count(classes[i])
    return make_response(jsonify(stats))
