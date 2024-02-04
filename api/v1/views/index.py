#!/usr/bin/python3
""" Index API
"""

from models.amenity import Amenity
from api.v1.views import app_views
from models.city import City
from flask import jsonify
from models.place import Place
from models.state import State
from models import storage
from models.review import Review
from models.user import User


@app_views.route('/status')
def status():
    """Returns the status of the app"""
    response = {
        'status': 'OK'
    }
    return jsonify(response)


@app_views.route('/stats')
def get_stats():
    """Retrieves the number of each objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]
    stats = {}
    for i in range(len(classes)):
        stats[names[i]] = storage.count(classes[i])
    return jsonify(stats)
