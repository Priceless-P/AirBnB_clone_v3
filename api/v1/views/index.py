#!/usr/bin/python3
""" Index API
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
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
    stats = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    }
    return jsonify(stats)
